"""Read/cache the project bSDD dictionaries (resources/subsea_*_completo.json).

Shared by `modules/analysis` (property-based coloring) and `modules/catalog`
(guided Pset/Property picker in LI Mapping), so both modules navigate the same
class/Pset/property catalog without parsing the JSON twice.
"""

import json
import os
import re
from functools import lru_cache


_DISCIPLINE_DEFS = {
    "flexible_pipes": {
        "label": "Flexible Pipes",
        "description": "Oil & Gas Subsea Flexible Pipes",
        "file": "subsea_flexible_pipes_2.1_completo.json",
    },
    "rigid_pipes": {
        "label": "Rigid Pipes",
        "description": "Oil & Gas Subsea Rigid Pipelines",
        "file": "subsea_rigid_pipes_1.0_completo.json",
    },
}

DICTIONARY_DISCIPLINE_ITEMS = [
    (key, data["label"], data["description"])
    for key, data in _DISCIPLINE_DEFS.items()
]

_DICTIONARY_CACHE = {}

# Caches for lists returned by dynamic `EnumProperty(items=...)` callbacks.
# Blender requires Python to keep a strong reference to tuples/strings returned
# by `items`; if a new list is created and discarded on each call, GC may free
# it between the callback and dropdown drawing, leaving the C array with invalid
# pointers and causing intermittent Blender crashes. Keeping the list here, and
# reusing it while the key is unchanged, avoids that risk.
_OBJECT_TYPE_ITEMS_CACHE = {}
_PSET_ITEMS_CACHE = {}
_PROPERTY_ITEMS_CACHE = {}


def _resources_dir():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "resources",
    )


def _friendly_pset_label(pset_name):
    label = pset_name or ""
    for prefix in ("OGSubPset_", "Pset_", "Qto_"):
        if label.startswith(prefix):
            label = label[len(prefix):]
            break
    label = label.replace("_", " ")
    label = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", label)
    return label.strip() or (pset_name or "Unnamed Pset")


def _iter_class_nodes(nodes):
    for node in nodes or []:
        yield node
        children = node.get("children") or []
        if children:
            yield from _iter_class_nodes(children)


def _collect_class_properties(class_data):
    properties = []

    for prop_data in class_data.get("classProperties") or []:
        properties.append((prop_data.get("propertySet") or "", prop_data))

    for pset_data in class_data.get("propertySets") or []:
        pset_name = pset_data.get("name") or pset_data.get("propertySet") or ""
        for prop_data in pset_data.get("properties") or []:
            properties.append((pset_name, prop_data))

    return properties


def _base_object_type(code):
    if code and code.endswith("Type"):
        return code[:-4]
    return code or ""


def get_dictionary(discipline_key):
    """Load and cache the parsed bSDD dictionary for a discipline.

    Returns a dict with:
      - "object_types": {key: {"label", "description", "psets": {pset_key: {
            "label", "technical_name", "source" ("type"/"occurrence"),
            "properties": {prop_key: {"label","description","data_type","units"}}
        }}}}
      - "parent_types": {object_type_key: parent_object_type_key}

    Occurrence classes (for example "AnchoringCollar") and their "*Type"
    counterparts (for example "AnchoringCollarType") are merged under the same
    key by removing the "Type" suffix, because both describe the same
    ObjectType: one with occurrence Psets and the other with IfcTypeProduct
    Psets.
    """
    if discipline_key not in _DISCIPLINE_DEFS:
        discipline_key = next(iter(_DISCIPLINE_DEFS.keys()))

    cached = _DICTIONARY_CACHE.get(discipline_key)
    if cached is not None:
        return cached

    file_name = _DISCIPLINE_DEFS[discipline_key]["file"]
    file_path = os.path.join(_resources_dir(), file_name)

    with open(file_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    object_types = {}
    parent_types = {}
    raw_classes = payload.get("classes", [])
    class_nodes = list(_iter_class_nodes(raw_classes))

    for class_data in class_nodes:
        raw_code = class_data.get("referenceCode") or class_data.get("code") or class_data.get("name") or ""
        is_type_class = raw_code.endswith("Type")
        object_type_key = _base_object_type(raw_code)
        parent_data = class_data.get("parentClassReference") or {}
        parent_code = parent_data.get("code") or parent_data.get("name") or ""
        parent_key = _base_object_type(parent_code)
        if object_type_key and parent_key and object_type_key != parent_key:
            parent_types[object_type_key] = parent_key

        properties = _collect_class_properties(class_data)
        if not properties:
            continue

        if not object_type_key:
            continue

        # "Material" classes (for example CompositeMaterial, MetallicMaterial)
        # describe materials associated through IfcRelAssociatesMaterial, not
        # scene occurrences. Selecting one would never find an object to color
        # or map, so they are not listed.
        if class_data.get("classType") == "Material":
            continue

        entry = object_types.setdefault(
            object_type_key,
            {
                "label": class_data.get("description") or class_data.get("descriptionPart") or object_type_key,
                "description": class_data.get("definition") or class_data.get("description") or class_data.get("descriptionPart") or object_type_key,
                "psets": {},
            },
        )

        if not raw_code.endswith("Type") and class_data.get("description"):
            entry["label"] = class_data.get("description")
        if class_data.get("definition"):
            entry["description"] = class_data.get("definition")

        for pset_name, prop_data in properties:
            prop_name = prop_data.get("name") or prop_data.get("propertyCode") or prop_data.get("code") or ""
            if not pset_name or not prop_name:
                continue

            pset_entry = entry["psets"].setdefault(
                pset_name,
                {
                    "label": _friendly_pset_label(pset_name),
                    "technical_name": pset_name,
                    # Source class for this Pset: "type" = exists only on the
                    # IfcTypeProduct (same value for every occurrence of that
                    # type); "occurrence" = may vary by occurrence.
                    "source": "type" if is_type_class else "occurrence",
                    "properties": {},
                },
            )
            pset_entry["properties"].setdefault(
                prop_name,
                {
                    "label": prop_data.get("description") or prop_name,
                    "description": prop_data.get("definition") or prop_data.get("description") or prop_name,
                    # Keep the JSON fields separate.  The Properties panel uses
                    # the short bSDD description as its display label, while
                    # other consumers may still need the longer definition.
                    "json_description": prop_data.get("description") or "",
                    "json_definition": prop_data.get("definition") or "",
                    "data_type": prop_data.get("dataType") or "",
                    "units": ", ".join(prop_data.get("units") or []),
                },
            )

    data = {
        "discipline": discipline_key,
        "object_types": object_types,
        "parent_types": parent_types,
    }
    _DICTIONARY_CACHE[discipline_key] = data
    return data


def get_object_type_entry(discipline_key, object_type_key):
    data = get_dictionary(discipline_key)
    return data["object_types"].get(object_type_key)


def get_pset_entry(discipline_key, object_type_key, pset_key):
    entry = get_object_type_entry(discipline_key, object_type_key)
    if not entry:
        return None
    return entry["psets"].get(pset_key)


def _pset_name_variants(pset_name):
    """Return dictionary/IFC spelling variants used by project files."""
    variants = [pset_name]
    if "Occurrence" in pset_name:
        variants.append(pset_name.replace("Occurrence", "Occurence"))
    elif "Occurence" in pset_name:
        variants.append(pset_name.replace("Occurence", "Occurrence"))
    return variants


@lru_cache(maxsize=None)
def _get_property_json_entry(object_type_key, pset_name, prop_name):
    """Find a property's parsed metadata in the bundled dictionary JSON."""
    object_type_key = _base_object_type(object_type_key)
    pset_variants = _pset_name_variants(pset_name or "")

    dictionaries = [get_dictionary(key) for key in _DISCIPLINE_DEFS]

    if object_type_key:
        for data in dictionaries:
            current_key = object_type_key
            visited = set()
            while current_key and current_key not in visited:
                visited.add(current_key)
                object_entry = data["object_types"].get(current_key)
                if object_entry:
                    for pset_variant in pset_variants:
                        pset_entry = object_entry["psets"].get(pset_variant)
                        if pset_entry and prop_name in pset_entry["properties"]:
                            return pset_entry["properties"][prop_name]
                current_key = data["parent_types"].get(current_key)

    for data in dictionaries:
        for object_entry in data["object_types"].values():
            for pset_variant in pset_variants:
                pset_entry = object_entry["psets"].get(pset_variant)
                if pset_entry and prop_name in pset_entry["properties"]:
                    return pset_entry["properties"][prop_name]

    return None


def get_property_json_description(object_type_key, pset_name, prop_name):
    """Find a property's short description in the bundled dictionary JSON.

    The object type is preferred so identically named properties can have
    class-specific descriptions.  Parent classes are also checked because
    their Psets may be inherited.  If the IFC has no usable ObjectType, a
    Pset/property lookup across both dictionaries is used as a final fallback.

    Returns ``None`` when the property is absent from the JSON and an empty
    string when it is present but has no JSON ``description``.
    """
    entry = _get_property_json_entry(object_type_key, pset_name, prop_name)
    return entry["json_description"] if entry is not None else None


def get_property_json_definition(object_type_key, pset_name, prop_name):
    """Find a property's long ``definition`` in the bundled dictionary JSON."""
    entry = _get_property_json_entry(object_type_key, pset_name, prop_name)
    return entry["json_definition"] if entry is not None else None


def get_object_type_items(discipline_key):
    """Cached (key, label, tooltip) list for an ObjectType EnumProperty."""
    cached = _OBJECT_TYPE_ITEMS_CACHE.get(discipline_key)
    if cached is not None:
        return cached

    data = get_dictionary(discipline_key)
    items = []
    for key, entry in sorted(data["object_types"].items(), key=lambda item: item[1]["label"].lower()):
        items.append((key, entry["label"], entry["description"]))
    _OBJECT_TYPE_ITEMS_CACHE[discipline_key] = items
    return items


def get_pset_items(discipline_key, object_type_key):
    """Cached (key, label, tooltip) list for a Pset EnumProperty.

    The label is prefixed with "[Type]"/"[Occurrence]" to make it clear whether
    the value is shared by every ObjectType occurrence (Type) or may vary by
    object (Occurrence).
    """
    key = (discipline_key, object_type_key)
    cached = _PSET_ITEMS_CACHE.get(key)
    if cached is not None:
        return cached

    entry = get_object_type_entry(discipline_key, object_type_key)
    items = []
    if entry:
        for pset_key, pset_data in sorted(entry["psets"].items(), key=lambda item: item[1]["label"].lower()):
            level = "Type" if pset_data.get("source") == "type" else "Occurrence"
            label = f"[{level}] {pset_data['label']}"
            tooltip = (
                f"Level: {level} | technical name: {pset_data['technical_name']}"
                + (" (same value for every occurrence of this Element)" if level == "Type" else "")
            )
            items.append((pset_key, label, tooltip))
    _PSET_ITEMS_CACHE[key] = items
    return items


def get_property_items(discipline_key, object_type_key, pset_key):
    """Cached (key, label, tooltip) list for a Property EnumProperty."""
    key = (discipline_key, object_type_key, pset_key)
    cached = _PROPERTY_ITEMS_CACHE.get(key)
    if cached is not None:
        return cached

    pset_data = get_pset_entry(discipline_key, object_type_key, pset_key)
    items = []
    if pset_data:
        for prop_key, prop_data in sorted(pset_data["properties"].items(), key=lambda item: item[1]["label"].lower()):
            suffix = f" [{prop_data['units']}]" if prop_data["units"] else ""
            tooltip = f"{prop_key} | {prop_data['data_type']}{suffix}".strip()
            items.append((prop_key, prop_data["label"], tooltip))
    _PROPERTY_ITEMS_CACHE[key] = items
    return items
