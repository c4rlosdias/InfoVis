import json
import os


RELATION_PRESETS = [
    {
        "key": "group",
        "label": "Group assignment",
        "element_attribute": "IsGroupedBy",
        "relationship_type": "IfcRelAssignsToGroup",
        "relationship_attribute": "RelatedObjects",
    },
    {
        "key": "spatial_containment",
        "label": "Spatial containment",
        "element_attribute": "ContainsElements",
        "relationship_type": "IfcRelContainedInSpatialStructure",
        "relationship_attribute": "RelatedElements",
    },
    {
        "key": "aggregation",
        "label": "Aggregation",
        "element_attribute": "IsDecomposedBy",
        "relationship_type": "IfcRelAggregates",
        "relationship_attribute": "RelatedObjects",
    },
    {
        "key": "nesting",
        "label": "Nesting",
        "element_attribute": "IsNestedBy",
        "relationship_type": "IfcRelNests",
        "relationship_attribute": "RelatedObjects",
    },
    {
        "key": "control",
        "label": "Control assignment",
        "element_attribute": "Controls",
        "relationship_type": "IfcRelAssignsToControl",
        "relationship_attribute": "RelatedObjects",
    },
]

DEFAULT_VIEWS = [
    {
        "id": "assets",
        "label": "Assets",
        "root_ifc_class": "IfcProject",
        "relations": [
            {
                "element_attribute": "IsGroupedBy",
                "relationship_type": "IfcRelAssignsToGroup",
                "relationship_attribute": "RelatedObjects",
            },
            {
                "element_attribute": "ContainsElements",
                "relationship_type": "IfcRelContainedInSpatialStructure",
                "relationship_attribute": "RelatedElements",
            },
            {
                "element_attribute": "IsDecomposedBy",
                "relationship_type": "IfcRelAggregates",
                "relationship_attribute": "RelatedObjects",
            },
            {
                "element_attribute": "IsNestedBy",
                "relationship_type": "IfcRelNests",
                "relationship_attribute": "RelatedObjects",
            },
        ],
    },
    {
        "id": "contracts",
        "label": "Contracts",
        "root_ifc_class": "IfcProjectOrder",
        "relations": [
            {
                "element_attribute": "Controls",
                "relationship_type": "IfcRelAssignsToControl",
                "relationship_attribute": "RelatedObjects",
            },
            {
                "element_attribute": "IsGroupedBy",
                "relationship_type": "IfcRelAssignsToGroup",
                "relationship_attribute": "RelatedObjects",
            },
            {
                "element_attribute": "IsDecomposedBy",
                "relationship_type": "IfcRelAggregates",
                "relationship_attribute": "RelatedObjects",
            },
            {
                "element_attribute": "IsNestedBy",
                "relationship_type": "IfcRelNests",
                "relationship_attribute": "RelatedObjects",
            },
        ],
    },
    {
        "id": "inventory",
        "label": "Inventory",
        "root_ifc_class": "IfcInventory",
        "relations": [
            {
                "element_attribute": "IsGroupedBy",
                "relationship_type": "IfcRelAssignsToGroup",
                "relationship_attribute": "RelatedObjects",
            },
        ],
    },
]


_DEFAULT_ROOT_CLASSES = {
    "assets": "IfcProject",
    "contracts": "IfcProjectOrder",
    "inventory": "IfcInventory",
}

_RELATION_TYPES_BY_ATTRIBUTES = {
    (preset["element_attribute"], preset["relationship_attribute"]): preset["relationship_type"]
    for preset in RELATION_PRESETS
}


def get_config_path():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "resources", "decomposition_view.json")
    )


def get_preset(key):
    for preset in RELATION_PRESETS:
        if preset["key"] == key:
            return preset.copy()
    return RELATION_PRESETS[0].copy()


def get_relation_attributes(relation):
    if isinstance(relation, dict):
        return (
            relation.get("element_attribute", ""),
            relation.get("relationship_attribute", ""),
        )
    return relation[0], relation[1]


def normalize_relation(relation):
    if isinstance(relation, dict):
        element_attribute = str(
            relation.get("element_attribute") or relation.get("source") or ""
        ).strip()
        relationship_attribute = str(
            relation.get("relationship_attribute") or relation.get("target") or ""
        ).strip()
        relationship_type = str(relation.get("relationship_type") or "").strip()
    elif isinstance(relation, (list, tuple)) and len(relation) >= 2:
        element_attribute = str(relation[0]).strip()
        relationship_attribute = str(relation[1]).strip()
        relationship_type = ""
    else:
        element_attribute = ""
        relationship_attribute = ""
        relationship_type = ""

    if not relationship_type:
        relationship_type = _RELATION_TYPES_BY_ATTRIBUTES.get(
            (element_attribute, relationship_attribute),
            "",
        )

    return {
        "element_attribute": element_attribute,
        "relationship_type": relationship_type,
        "relationship_attribute": relationship_attribute,
    }


def normalize_view(view):
    view_id = str(view.get("id", "")).strip()
    root_ifc_class = str(
        view.get("root_ifc_class") or _DEFAULT_ROOT_CLASSES.get(view_id, "IfcProject")
    ).strip()
    label = str(view.get("label") or view_id.title()).strip()
    relations = [
        normalize_relation(relation)
        for relation in view.get("relations", [])
    ]

    return {
        "id": view_id,
        "label": label,
        "root_ifc_class": root_ifc_class,
        "relations": relations,
    }


def normalize_payload(payload):
    raw_views = payload.get("views", []) if isinstance(payload, dict) else []
    return {
        "views": [
            normalize_view(view)
            for view in raw_views
            if isinstance(view, dict)
        ]
    }


def load_views():
    with open(get_config_path(), encoding="utf-8") as file:
        payload = json.load(file)
    return normalize_payload(payload)["views"]


def default_views():
    return normalize_payload({"views": DEFAULT_VIEWS})["views"]


def payload_from_collection(collection):
    views = []
    for item in collection:
        view = {
            "id": item.id.strip(),
            "label": item.label.strip(),
            "root_ifc_class": item.root_ifc_class.strip(),
            "relations": [],
        }
        for relation in item.relations:
            view["relations"].append(
                {
                    "element_attribute": relation.element_attribute.strip(),
                    "relationship_type": relation.relationship_type.strip(),
                    "relationship_attribute": relation.relationship_attribute.strip(),
                }
            )
        views.append(view)
    return normalize_payload({"views": views})


def validate_payload(payload):
    errors = []
    normalized = normalize_payload(payload)
    seen_ids = set()

    if not normalized["views"]:
        errors.append("At least one decomposition view is required.")

    for view in normalized["views"]:
        view_id = view["id"]
        if not view_id:
            errors.append("Every view needs an id.")
            continue
        if view_id in seen_ids:
            errors.append(f"Duplicated decomposition view id: {view_id}")
        seen_ids.add(view_id)

        if not view["root_ifc_class"]:
            errors.append(f"View '{view_id}' needs a root IFC class.")
        if not view["relations"]:
            errors.append(f"View '{view_id}' needs at least one IFC relation.")

        for index, relation in enumerate(view["relations"], start=1):
            if not relation["element_attribute"]:
                errors.append(f"View '{view_id}', relation {index}: missing element attribute.")
            if not relation["relationship_attribute"]:
                errors.append(f"View '{view_id}', relation {index}: missing relationship attribute.")

    return errors


def save_payload(payload):
    normalized = normalize_payload(payload)
    errors = validate_payload(normalized)
    if errors:
        raise ValueError(errors[0])

    with open(get_config_path(), "w", encoding="utf-8") as file:
        json.dump(normalized, file, indent=2, ensure_ascii=False)
        file.write("\n")
    return normalized
