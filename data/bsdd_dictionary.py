"""Leitura/cache dos dicionários bSDD do projeto (resources/subsea_*_completo.json).

Compartilhado entre `modules/analysis` (coloração por propriedade) e
`modules/catalog` (seletor guiado de Pset/Property na LI mapping), para que
os dois módulos naveguem pelo mesmo catálogo de classes/psets/properties sem
duplicar o parsing do JSON.
"""

import json
import os
import re


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

# Caches para as listas retornadas aos `EnumProperty(items=...)` dinâmicos.
# A API do Blender exige que algo em Python mantenha uma referência forte às
# tuplas/strings devolvidas pelo callback de `items`; se uma lista nova é
# criada e descartada a cada chamada, o GC pode liberá-la entre o callback e
# o desenho do dropdown, deixando o array C com ponteiros inválidos e
# causando travamentos intermitentes do Blender. Guardando a lista aqui (e
# reaproveitando-a enquanto a chave não muda) evitamos esse risco.
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
    """Carrega (com cache) o dicionário bSDD da disciplina, já parseado.

    Retorna um dict com:
      - "object_types": {key: {"label", "description", "psets": {pset_key: {
            "label", "technical_name", "source" ("type"/"occurrence"),
            "properties": {prop_key: {"label","description","data_type","units"}}
        }}}}
      - "parent_types": {object_type_key: parent_object_type_key}

    Classes de ocorrência (ex.: "AnchoringCollar") e sua contraparte "*Type"
    (ex.: "AnchoringCollarType") são mescladas sob a mesma chave (o sufixo
    "Type" é removido), já que ambas descrevem o mesmo ObjectType — uma com
    os psets de ocorrência, outra com os psets do IfcTypeProduct.
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

        # Classes do tipo "Material" (ex.: CompositeMaterial, MetallicMaterial)
        # descrevem materiais associados via IfcRelAssociatesMaterial, não
        # ocorrências próprias na cena. Nenhuma seleção desse tipo jamais
        # encontraria um objeto a colorir/mapear, então não entram na lista.
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
                    # de qual classe esse pset veio: "type" = só existe no
                    # IfcTypeProduct (mesmo valor p/ todas as ocorrências
                    # daquele tipo); "occurrence" = pode variar por ocorrência.
                    "source": "type" if is_type_class else "occurrence",
                    "properties": {},
                },
            )
            pset_entry["properties"].setdefault(
                prop_name,
                {
                    "label": prop_data.get("description") or prop_name,
                    "description": prop_data.get("definition") or prop_data.get("description") or prop_name,
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


def get_object_type_items(discipline_key):
    """Lista cacheada de (key, label, tooltip) para um EnumProperty de ObjectType."""
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
    """Lista cacheada de (key, label, tooltip) para um EnumProperty de Pset.

    O label vem prefixado com "[Type]"/"[Occurrence]" para deixar claro se o
    valor é compartilhado por todas as ocorrências do ObjectType (Type) ou
    pode variar por objeto (Occurrence).
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
                f"Nível: {level} | nome técnico: {pset_data['technical_name']}"
                + (" (mesmo valor em todas as ocorrências deste Element)" if level == "Type" else "")
            )
            items.append((pset_key, label, tooltip))
    _PSET_ITEMS_CACHE[key] = items
    return items


def get_property_items(discipline_key, object_type_key, pset_key):
    """Lista cacheada de (key, label, tooltip) para um EnumProperty de Property."""
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
