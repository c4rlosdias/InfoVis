import colorsys
import json

import bpy
import ifcopenshell.util.element

from ...data.ifc_session import get_entity, get_model
from ...data.bsdd_dictionary import (
    DICTIONARY_DISCIPLINE_ITEMS,
    _base_object_type,
    get_dictionary,
    get_object_type_entry,
    get_object_type_items,
    get_pset_entry,
    get_pset_items,
    get_property_items,
    _pset_name_variants,
)

# Alias kept for compatibility with code that already imported these names from
# this module (for example modules/og_properties.py). The dictionary
# reading/parsing itself lives in data/bsdd_dictionary.py and is shared with the
# catalog module property picker (LI Mapping).
ANALYSIS_DISCIPLINE_ITEMS = DICTIONARY_DISCIPLINE_ITEMS
get_analysis_dictionary = get_dictionary

_VALUE_CACHE = {}

# Cache for the list returned to the value `EnumProperty(items=...)`; see the
# equivalent note in data/bsdd_dictionary.py for why this is necessary.
_VALUE_ITEMS_CACHE = {}

_MUTED_COLOR = (0.35, 0.35, 0.35, 1.0)
_NO_VALUE_COLOR = (0.55, 0.55, 0.55, 1.0)
_MATCH_COLOR = (0.14, 0.72, 0.42, 1.0)


def analysis_get_disciplines(self, context):
    return ANALYSIS_DISCIPLINE_ITEMS


def analysis_get_object_types(self, context):
    return get_object_type_items(getattr(self, "analysis_discipline", "flexible_pipes"))


def analysis_get_psets(self, context):
    discipline = getattr(self, "analysis_discipline", "flexible_pipes")
    object_type = getattr(self, "analysis_object_type", "")
    return get_pset_items(discipline, object_type)


def analysis_get_properties(self, context):
    discipline = getattr(self, "analysis_discipline", "flexible_pipes")
    object_type = getattr(self, "analysis_object_type", "")
    pset = getattr(self, "analysis_pset", "")
    return get_property_items(discipline, object_type, pset)


def _matches_analysis_object_type(discipline_key, selected_object_type, actual_object_type):
    if not selected_object_type or not actual_object_type:
        return False
    if selected_object_type == actual_object_type:
        return True

    parent_types = get_dictionary(discipline_key).get("parent_types", {})
    current_object_type = actual_object_type
    visited = set()

    while current_object_type and current_object_type not in visited:
        visited.add(current_object_type)
        current_object_type = parent_types.get(current_object_type)
        if current_object_type == selected_object_type:
            return True

    return False


def _normalize_value(value):
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=True, sort_keys=True)
    if value is None:
        return ""
    return str(value)


def _coerce_float(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", ".")
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _iter_ifc_scene_objects():
    for obj in bpy.data.objects:
        entity = get_entity(obj)
        if entity is None or entity.is_a("IfcTypeProduct"):
            continue
        yield obj, entity


def _get_entity_object_type(entity):
    object_type = getattr(entity, "ObjectType", "") or ""
    if object_type:
        return object_type

    type_entity = ifcopenshell.util.element.get_type(entity)
    if type_entity is None:
        return ""

    for attribute in ("ObjectType", "ElementType", "Name"):
        value = getattr(type_entity, attribute, "") or ""
        if value:
            return _base_object_type(value)
    return ""


def _lookup_property_in_psets(psets, pset_name, prop_name):
    for variant in _pset_name_variants(pset_name):
        pset = psets.get(variant)
        if pset and prop_name in pset:
            return pset[prop_name]
    return None


def _get_entity_property_value(entity, pset_name, prop_name):
    instance_psets = ifcopenshell.util.element.get_psets(entity, should_inherit=False) or {}
    value = _lookup_property_in_psets(instance_psets, pset_name, prop_name)
    if value is not None:
        return value

    type_entity = ifcopenshell.util.element.get_type(entity)
    if type_entity is not None:
        type_psets = ifcopenshell.util.element.get_psets(type_entity, should_inherit=False) or {}
        value = _lookup_property_in_psets(type_psets, pset_name, prop_name)
        if value is not None:
            return value

    inherited_psets = ifcopenshell.util.element.get_psets(entity) or {}
    return _lookup_property_in_psets(inherited_psets, pset_name, prop_name)


def _selection_key(props):
    return (
        getattr(props, "analysis_discipline", ""),
        getattr(props, "analysis_object_type", ""),
        getattr(props, "analysis_pset", ""),
        getattr(props, "analysis_property", ""),
    )


def collect_analysis_values(props):
    key = _selection_key(props)
    if not all(key):
        return []

    cached = _VALUE_CACHE.get(key)
    if cached is not None:
        return cached

    values = []
    for _obj, entity in _iter_ifc_scene_objects():
        if not _matches_analysis_object_type(
            props.analysis_discipline,
            props.analysis_object_type,
            _get_entity_object_type(entity),
        ):
            continue
        value = _get_entity_property_value(entity, props.analysis_pset, props.analysis_property)
        if value is not None:
            values.append(value)

    _VALUE_CACHE[key] = values
    return values


def invalidate_analysis_value_cache():
    _VALUE_CACHE.clear()
    _VALUE_ITEMS_CACHE.clear()


def analysis_get_values(self, context):
    key = _selection_key(self)
    cached = _VALUE_ITEMS_CACHE.get(key)
    if cached is not None:
        return cached

    counts = {}
    for value in collect_analysis_values(self):
        normalized = _normalize_value(value)
        counts[normalized] = counts.get(normalized, 0) + 1

    items = []
    for normalized in sorted(counts.keys(), key=lambda item: item.lower()):
        items.append((normalized, f"{normalized} ({counts[normalized]})", normalized))
    _VALUE_ITEMS_CACHE[key] = items
    return items


def get_numeric_bounds(props):
    numeric_values = []
    for value in collect_analysis_values(props):
        numeric = _coerce_float(value)
        if numeric is not None:
            numeric_values.append(numeric)

    if not numeric_values:
        return None
    return min(numeric_values), max(numeric_values), len(numeric_values)


def _set_viewport_object_color_mode():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
                    space.shading.color_type = 'OBJECT'


def _set_object_color(obj, rgba):
    obj.color = rgba
    obj.update_tag()


def _redraw_viewports():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _palette_color(index, total):
    if total <= 0:
        return _MATCH_COLOR
    hue = (index / max(total, 1)) % 1.0
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.65, 0.95)
    return (red, green, blue, 1.0)


def _gradient_color(value, min_value, max_value):
    if max_value <= min_value:
        factor = 0.5
    else:
        factor = (value - min_value) / (max_value - min_value)
    factor = max(0.0, min(1.0, factor))
    red = 0.12 + (0.88 * factor)
    green = 0.24 + (0.52 * (1.0 - abs(factor - 0.5) * 2.0))
    blue = 0.88 - (0.62 * factor)
    return (red, green, blue, 1.0)


def _legend_entry(label, rgba):
    return {"label": label, "color": tuple(rgba)}


def _format_number(value):
    return f"{value:.4g}"


def validate_analysis_selection(props):
    if get_model() is None:
        raise ValueError("No Ifc file loaded")
    if not getattr(props, "analysis_object_type", ""):
        raise ValueError("Select an ObjectType")
    if not getattr(props, "analysis_pset", ""):
        raise ValueError("Select a property set")
    if not getattr(props, "analysis_property", ""):
        raise ValueError("Select a property")


def apply_analysis_colors(props):
    validate_analysis_selection(props)
    _set_viewport_object_color_mode()

    targets = []
    others = []
    for obj, entity in _iter_ifc_scene_objects():
        object_type = _get_entity_object_type(entity)
        if _matches_analysis_object_type(props.analysis_discipline, props.analysis_object_type, object_type):
            value = _get_entity_property_value(entity, props.analysis_pset, props.analysis_property)
            targets.append((obj, value))
        else:
            others.append(obj)

    if not targets:
        raise ValueError("No scene objects found for the selected ObjectType")

    for obj in others:
        _set_object_color(obj, _MUTED_COLOR)

    mode = getattr(props, "analysis_color_mode", "distinct")
    matched = 0
    categories = 0
    legend = []

    if mode == "distinct":
        value_counts = {}
        no_value_count = 0
        for _obj, value in targets:
            if value is None:
                no_value_count += 1
                continue
            normalized = _normalize_value(value)
            value_counts[normalized] = value_counts.get(normalized, 0) + 1

        grouped_keys = sorted(value_counts.keys(), key=lambda item: item.lower())
        palette = {key: _palette_color(index, len(grouped_keys)) for index, key in enumerate(grouped_keys)}

        for obj, value in targets:
            if value is None:
                _set_object_color(obj, _NO_VALUE_COLOR)
                continue
            _set_object_color(obj, palette[_normalize_value(value)])
            matched += 1
        categories = len(grouped_keys)
        for key in grouped_keys:
            legend.append(_legend_entry(f"{key} ({value_counts[key]})", palette[key]))
        if no_value_count:
            legend.append(_legend_entry(f"No value ({no_value_count})", _NO_VALUE_COLOR))

    elif mode == "exact":
        selected_value = getattr(props, "analysis_value", "")
        if not selected_value:
            raise ValueError("Select a value")
        for obj, value in targets:
            if value is not None and _normalize_value(value) == selected_value:
                _set_object_color(obj, _MATCH_COLOR)
                matched += 1
            else:
                _set_object_color(obj, _NO_VALUE_COLOR)
        categories = 1
        legend.append(_legend_entry(f"Match: {selected_value} ({matched})", _MATCH_COLOR))
        unmatched_count = len(targets) - matched
        if unmatched_count:
            legend.append(_legend_entry(f"Other values / no value ({unmatched_count})", _NO_VALUE_COLOR))

    else:
        min_value = props.analysis_range_min
        max_value = props.analysis_range_max
        if max_value < min_value:
            raise ValueError("Range max must be greater than or equal to min")

        numeric_matches = []
        for obj, value in targets:
            numeric = _coerce_float(value)
            numeric_matches.append((obj, numeric))

        if not any(value is not None for _obj, value in numeric_matches):
            raise ValueError("The selected property does not have numeric values")

        outside_count = 0
        for obj, numeric in numeric_matches:
            if numeric is None or numeric < min_value or numeric > max_value:
                _set_object_color(obj, _NO_VALUE_COLOR)
                outside_count += 1
                continue
            _set_object_color(obj, _gradient_color(numeric, min_value, max_value))
            matched += 1
        categories = 1
        mid_value = min_value + ((max_value - min_value) / 2.0)
        legend.extend([
            _legend_entry(f"Range min: {_format_number(min_value)}", _gradient_color(min_value, min_value, max_value)),
            _legend_entry(f"Range mid: {_format_number(mid_value)}", _gradient_color(mid_value, min_value, max_value)),
            _legend_entry(f"Range max: {_format_number(max_value)}", _gradient_color(max_value, min_value, max_value)),
        ])
        if outside_count:
            legend.append(_legend_entry(f"Outside range / no numeric value ({outside_count})", _NO_VALUE_COLOR))

    if others:
        legend.append(_legend_entry(f"Other elements ({len(others)})", _MUTED_COLOR))

    _redraw_viewports()

    return {
        "target_count": len(targets),
        "matched_count": matched,
        "category_count": categories,
        "legend": legend,
    }


def reset_analysis_colors():
    for obj, _entity in _iter_ifc_scene_objects():
        _set_object_color(obj, (1.0, 1.0, 1.0, 1.0))
    _redraw_viewports()
