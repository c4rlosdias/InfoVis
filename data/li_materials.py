"""Material value extraction for LI exports.

The helper keeps IFC material structures out of the UI. It accepts both direct
materials and inherited type materials through IfcOpenShell's element utility.
"""


def _entity_id(entity):
    if entity is None:
        return None
    return entity.id() if hasattr(entity, "id") else id(entity)


def _unique_text(values):
    result = []
    seen = set()
    for value in values:
        if value in (None, ""):
            continue
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _get_materials(type_entity, occurrence, element_util):
    materials = []
    seen = set()
    for entity in (occurrence, type_entity):
        if entity is None:
            continue
        try:
            entity_materials = element_util.get_materials(entity, should_inherit=False) or []
        except (AttributeError, RuntimeError, TypeError):
            continue
        for material in entity_materials:
            material_id = _entity_id(material)
            if material is None or material_id in seen:
                continue
            seen.add(material_id)
            materials.append(material)
    return materials


def _get_material_property(material, pset_name, property_name, element_util):
    if not pset_name or not property_name:
        return None
    try:
        pset = element_util.get_pset(material, pset_name) or {}
    except (AttributeError, RuntimeError, TypeError):
        return None
    return pset.get(property_name)


def _format_composition(material):
    name = getattr(material, "Name", None) or "Unnamed material"
    category = getattr(material, "Category", None)
    return f"{name} ({category})" if category else name


def _get_layer_values(type_entity, occurrence, element_util):
    for entity in (occurrence, type_entity):
        if entity is None:
            continue
        try:
            layers = element_util.get_material_layers(entity) or []
        except (AttributeError, RuntimeError, TypeError):
            continue
        if not layers:
            continue

        values = []
        for layer in layers:
            material = getattr(layer, "material", None)
            if material is None and isinstance(layer, (tuple, list)) and len(layer) > 1:
                material = layer[1]
            thickness = getattr(layer, "thickness", None)
            if thickness is None:
                thickness = getattr(layer, "LayerThickness", None)
            if thickness is None and isinstance(layer, (tuple, list)) and len(layer) > 2:
                thickness = layer[2]
            name = getattr(material, "Name", None) or "Unnamed material"
            values.append(f"{name}: {thickness}" if thickness not in (None, "") else name)
        return _unique_text(values)
    return []


def resolve_material_information(
    type_entity,
    occurrence,
    source,
    element_util=None,
):
    """Resolve a user-facing material value for one LI row.

    Supported ``material_field`` values are ``name``, ``category``,
    ``description``, ``composition``, ``layer_thickness`` and ``property``.
    Multiple values are de-duplicated and joined with ``; ``.
    """
    if element_util is None:
        import ifcopenshell.util.element as element_util

    material_field = source.get("material_field", "name")
    if material_field == "layer_thickness":
        return "; ".join(_get_layer_values(type_entity, occurrence, element_util))

    materials = _get_materials(type_entity, occurrence, element_util)
    if material_field == "property":
        values = [
            _get_material_property(
                material,
                source.get("pset"),
                source.get("property"),
                element_util,
            )
            for material in materials
        ]
    elif material_field == "composition":
        values = [_format_composition(material) for material in materials]
    else:
        attribute = {
            "name": "Name",
            "category": "Category",
            "description": "Description",
        }.get(material_field, "Name")
        values = [getattr(material, attribute, None) for material in materials]

    return "; ".join(_unique_text(values))
