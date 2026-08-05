import bpy
import os
import pandas as pd
import json
import openpyxl
import re
import ifcopenshell.util.element as element
import ifcopenshell
from pathlib import Path

from ...data.catalog import Catalog
from ...data.ifc_session import get_model, get_object
from ...data.ifc_utils import build_products
from ...data.ifc_utils import get_unit_symbol
from ...data.li_materials import resolve_material_information
from ...data.tree import refresh_types
from ..common.operators import _open_in_browser


_GUIDED_SOURCE_FIELDS = {
    'ifc_class': 'source_ifc_class',
    'level': 'source_level',
    'attribute': 'source_attribute',
    'fallback_attribute': 'source_fallback_attribute',
    'pset': 'source_pset',
    'property': 'source_property',
    'mapping_table': 'source_mapping_table',
    'quantity_mode': 'source_quantity_mode',
    'selected_by': 'source_selected_by',
    'template_table': 'source_template_table',
    'derived_from': 'source_derived_from',
    'method': 'source_method',
    'format': 'source_format',
    'allowed_values': 'source_allowed_values',
    'material_field': 'source_material_field',
}

# 'quantity_mode' is the only guided field that is an EnumProperty (the others
# are StringProperty fields) and it has no empty option, so it needs special
# handling in _reset_guided_source_fields.
_ENUM_GUIDED_FIELDS_DEFAULTS = {
    'source_quantity_mode': 'mapping',
    'source_material_field': 'name',
}

# Guided fields (keys from _GUIDED_SOURCE_FIELDS) that are meaningful for each
# source_type. This mirrors what modules/catalog/panels.py displays in the UI
# for each type and prevents irrelevant fields (for example quantity_mode in an
# ifc_class column) from being saved just because the Enum is never empty.
_RELEVANT_SOURCE_FIELDS = {
    'ifc_attribute': {'ifc_class', 'attribute', 'fallback_attribute', 'format'},
    'ifc_property': {'ifc_class', 'pset', 'property', 'allowed_values'},
    'manual': {'ifc_class', 'pset', 'property', 'allowed_values'},
    'material': {'material_field', 'pset', 'property'},
    'spatial': {'level', 'attribute'},
    'aggregation_parent': {'level', 'attribute', 'fallback_attribute'},
    'ifc_class': {'attribute', 'mapping_table'},
    'ifc_quantity': {'quantity_mode', 'mapping_table', 'selected_by'},
    'computed': {'selected_by', 'template_table', 'derived_from', 'method', 'format'},
    'not_applicable': set(),
}

LI_MAPPING_RESERVED_KEYS = {'$schema_version', 'description', 'reference_sheet', 'source_types', 'columns'}


def _get_li_mapping_path():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        "resources",
        "li_mapping.json",
    )


def get_li_mapping_path():
    return _get_li_mapping_path()


def load_li_mapping_payload():
    with open(_get_li_mapping_path(), 'r', encoding='utf-8') as file:
        return json.load(file)


def save_li_mapping_payload(data):
    with open(_get_li_mapping_path(), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write('\n')


def _clear_li_mapping(props):
    props.li_mapping_columns.clear()
    props.active_li_mapping_index = 0
    props.li_support_tables.clear()
    props.active_li_support_table_index = 0


def _stringify_mapping_value(value):
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _parse_mapping_value(raw_value):
    text = (raw_value or "").strip()
    if not text:
        return ""

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return raw_value


def _reset_guided_source_fields(column):
    for attr_name in _GUIDED_SOURCE_FIELDS.values():
        if attr_name in _ENUM_GUIDED_FIELDS_DEFAULTS:
            setattr(column, attr_name, _ENUM_GUIDED_FIELDS_DEFAULTS[attr_name])
        else:
            setattr(column, attr_name, '')


def _populate_guided_source_fields(column, source_data):
    _reset_guided_source_fields(column)
    for key, attr_name in _GUIDED_SOURCE_FIELDS.items():
        if key not in source_data or source_data[key] is None:
            continue
        setattr(column, attr_name, _stringify_mapping_value(source_data[key]))


def _build_source_from_column(column):
    source = {}
    relevant_keys = _RELEVANT_SOURCE_FIELDS.get(column.source_type, set(_GUIDED_SOURCE_FIELDS.keys()))

    for key, attr_name in _GUIDED_SOURCE_FIELDS.items():
        if key not in relevant_keys:
            continue
        if (
            column.source_type == 'material'
            and column.source_material_field != 'property'
            and key in {'pset', 'property'}
        ):
            continue
        raw_value = getattr(column, attr_name, '')
        if not raw_value:
            continue
        if key == 'allowed_values':
            source[key] = _parse_mapping_value(raw_value)
        else:
            source[key] = raw_value

    for source_item in column.source_items:
        key = source_item.key.strip()
        if not key:
            continue
        source[key] = _parse_mapping_value(source_item.value)

    if column.source_type == 'not_applicable' and not source:
        return None
    return source


def apply_li_mapping_payload_to_props(props, data):
    _clear_li_mapping(props)
    props.li_mapping_schema_version = str(data.get('$schema_version', '1.0'))
    props.li_mapping_description = data.get('description', '')
    props.li_mapping_reference_sheet = data.get('reference_sheet', '')

    for column_data in data.get('columns', []):
        column = props.li_mapping_columns.add()
        column.column_name = column_data.get('column', '')
        column.source_type = column_data.get('source_type', 'manual')
        column.notes = column_data.get('notes', '')

        source_data = column_data.get('source') or {}
        _populate_guided_source_fields(column, source_data)

        for key, value in source_data.items():
            if key in _GUIDED_SOURCE_FIELDS:
                continue
            source_item = column.source_items.add()
            source_item.key = str(key)
            source_item.value = _stringify_mapping_value(value)

    for table_name, table_data in data.items():
        if table_name in LI_MAPPING_RESERVED_KEYS or not isinstance(table_data, dict):
            continue

        support_table = props.li_support_tables.add()
        support_table.table_name = table_name
        support_table.description = table_data.get('_comment', '')
        for key, value in table_data.items():
            if key == '_comment':
                continue
            row = support_table.rows.add()
            row.key = str(key)
            row.value = _stringify_mapping_value(value)

    props.li_mapping_loaded = True


def _load_li_mapping_into_props(props):
    apply_li_mapping_payload_to_props(props, load_li_mapping_payload())


def li_mapping_payload_from_props(props, base_data=None):
    data = dict(base_data or {})
    data['$schema_version'] = props.li_mapping_schema_version or '1.0'
    data['description'] = props.li_mapping_description
    data['reference_sheet'] = props.li_mapping_reference_sheet

    columns = []
    for column in props.li_mapping_columns:
        columns.append({
            'column': column.column_name,
            'source_type': column.source_type,
            'source': _build_source_from_column(column),
            'notes': column.notes,
        })

    data['columns'] = columns

    for key in list(data.keys()):
        if key not in LI_MAPPING_RESERVED_KEYS and isinstance(data[key], dict):
            del data[key]

    for support_table in props.li_support_tables:
        table_data = {}
        if support_table.description:
            table_data['_comment'] = support_table.description

        for row in support_table.rows:
            row_key = row.key.strip()
            if not row_key:
                continue
            table_data[row_key] = _parse_mapping_value(row.value)

        data[support_table.table_name] = table_data

    return data


def _save_li_mapping_from_props(props):
    save_li_mapping_payload(
        li_mapping_payload_from_props(props, load_li_mapping_payload())
    )


class Operator_load_li_mapping(bpy.types.Operator):
    bl_idname = "catag.load_li_mapping"
    bl_label = "load LI mapping"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props

        try:
            _load_li_mapping_into_props(props)
        except Exception as exc:
            self.report({'ERROR'}, f"Failed to load LI mapping: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, "LI mapping loaded")
        return {'FINISHED'}


class Operator_save_li_mapping(bpy.types.Operator):
    bl_idname = "catag.save_li_mapping"
    bl_label = "save LI mapping"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props

        if not props.li_mapping_loaded:
            self.report({'WARNING'}, "Load LI mapping before saving")
            return {'CANCELLED'}

        try:
            _save_li_mapping_from_props(props)
        except Exception as exc:
            self.report({'ERROR'}, f"Failed to save LI mapping: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, "LI mapping changes applied")
        return {'FINISHED'}


class Operator_add_li_mapping_column(bpy.types.Operator):
    bl_idname = "catag.add_li_mapping_column"
    bl_label = "add LI mapping column"
    bl_options = {"REGISTER", "UNDO"}

    source_type : bpy.props.StringProperty(name="source type", default='manual')

    def execute(self, context):
        props = context.scene.og_props
        column = props.li_mapping_columns.add()
        column.column_name = "Material" if self.source_type == 'material' else "New Column"
        column.source_type = self.source_type
        column.notes = ''
        props.active_li_mapping_index = len(props.li_mapping_columns) - 1
        props.li_mapping_loaded = True
        return {'FINISHED'}


class Operator_remove_li_mapping_column(bpy.types.Operator):
    bl_idname = "catag.remove_li_mapping_column"
    bl_label = "remove LI mapping column"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_mapping_index

        if index < 0 or index >= len(props.li_mapping_columns):
            self.report({'WARNING'}, "No LI mapping column selected")
            return {'CANCELLED'}

        props.li_mapping_columns.remove(index)
        props.active_li_mapping_index = min(index, len(props.li_mapping_columns) - 1)
        return {'FINISHED'}


class Operator_move_li_mapping_column(bpy.types.Operator):
    bl_idname = "catag.move_li_mapping_column"
    bl_label = "move LI mapping column"
    bl_options = {"REGISTER", "UNDO"}

    index : bpy.props.IntProperty(name="index", default=-1)
    direction : bpy.props.EnumProperty(
        name="direction",
        items=[
            ('UP', "Up", "Move column up"),
            ('DOWN', "Down", "Move column down"),
        ],
        default='UP',
    )

    def execute(self, context):
        props = context.scene.og_props
        count = len(props.li_mapping_columns)

        if self.index < 0 or self.index >= count:
            self.report({'WARNING'}, "No LI mapping column selected")
            return {'CANCELLED'}

        target_index = self.index - 1 if self.direction == 'UP' else self.index + 1
        if target_index < 0 or target_index >= count:
            return {'CANCELLED'}

        props.li_mapping_columns.move(self.index, target_index)
        props.active_li_mapping_index = target_index
        props.li_mapping_loaded = True
        return {'FINISHED'}


class Operator_li_mapping_pick_property(bpy.types.Operator):
    """Copy the guided bSDD Pset/Property selection to the LI source fields."""
    bl_idname = "catag.li_mapping_pick_property"
    bl_label = "use selected property"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_mapping_index

        if index < 0 or index >= len(props.li_mapping_columns):
            self.report({'WARNING'}, "No LI mapping column selected")
            return {'CANCELLED'}

        column = props.li_mapping_columns[index]
        if not column.picker_pset or not column.picker_property:
            self.report({'WARNING'}, "Select Element, Property set, and Property before applying")
            return {'CANCELLED'}

        column.source_type = 'ifc_property'
        column.source_pset = column.picker_pset
        column.source_property = column.picker_property

        if not column.column_name or column.column_name == "New Column":
            column.column_name = column.picker_property

        self.report({'INFO'}, f"{column.picker_pset}.{column.picker_property} applied to the column")
        return {'FINISHED'}


class Operator_add_li_mapping_source_item(bpy.types.Operator):
    bl_idname = "catag.add_li_mapping_source_item"
    bl_label = "add LI mapping source item"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_mapping_index

        if index < 0 or index >= len(props.li_mapping_columns):
            self.report({'WARNING'}, "No LI mapping column selected")
            return {'CANCELLED'}

        column = props.li_mapping_columns[index]
        source_item = column.source_items.add()
        source_item.key = "key"
        source_item.value = "value"
        column.active_source_item_index = len(column.source_items) - 1
        return {'FINISHED'}


class Operator_remove_li_mapping_source_item(bpy.types.Operator):
    bl_idname = "catag.remove_li_mapping_source_item"
    bl_label = "remove LI mapping source item"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_mapping_index

        if index < 0 or index >= len(props.li_mapping_columns):
            self.report({'WARNING'}, "No LI mapping column selected")
            return {'CANCELLED'}

        column = props.li_mapping_columns[index]
        source_index = column.active_source_item_index
        if source_index < 0 or source_index >= len(column.source_items):
            self.report({'WARNING'}, "No source field selected")
            return {'CANCELLED'}

        column.source_items.remove(source_index)
        column.active_source_item_index = min(source_index, len(column.source_items) - 1)
        return {'FINISHED'}


class Operator_add_li_support_table_row(bpy.types.Operator):
    bl_idname = "catag.add_li_support_table_row"
    bl_label = "add LI support table row"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_support_table_index
        if index < 0 or index >= len(props.li_support_tables):
            self.report({'WARNING'}, "No support table selected")
            return {'CANCELLED'}

        table = props.li_support_tables[index]
        row = table.rows.add()
        row.key = "key"
        row.value = "value"
        table.active_row_index = len(table.rows) - 1
        return {'FINISHED'}


class Operator_remove_li_support_table_row(bpy.types.Operator):
    bl_idname = "catag.remove_li_support_table_row"
    bl_label = "remove LI support table row"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_li_support_table_index
        if index < 0 or index >= len(props.li_support_tables):
            self.report({'WARNING'}, "No support table selected")
            return {'CANCELLED'}

        table = props.li_support_tables[index]
        row_index = table.active_row_index
        if row_index < 0 or row_index >= len(table.rows):
            self.report({'WARNING'}, "No support table row selected")
            return {'CANCELLED'}

        table.rows.remove(row_index)
        table.active_row_index = min(row_index, len(table.rows) - 1)
        return {'FINISHED'}

def get_qtde(type):
    elements = ifcopenshell.util.element.get_types(type) or []
    qtde = 0
    if type.is_a('IfcPipeSegmentType'):
        for e in elements:
            pset = (
                ifcopenshell.util.element.get_pset(
                    e,
                    "OGSubPset_FlexiblePipeSegmentOccurence",
                )
                or {}
            )
            length = pset.get("NominalLength")
            if length in (None, ''):
                continue
            try:
                qtde += float(length)
            except (TypeError, ValueError):
                continue
    else:
        qtde = len(elements)
    return qtde


def _get_occurrence_quantity(occurrence, qto_name, quantity_name):
    if occurrence is None or not qto_name or not quantity_name:
        return None

    qtos = ifcopenshell.util.element.get_psets(occurrence, should_inherit=False)
    qto_data = qtos.get(qto_name, {})
    value = qto_data.get(quantity_name)
    return value if value not in (None, '') else None


def _sum_occurrence_quantities(occurrences, qto_name, quantity_name):
    values = []
    for occurrence in occurrences:
        value = _get_occurrence_quantity(occurrence, qto_name, quantity_name)
        if value in (None, ''):
            continue
        try:
            value = float(value)
        except (TypeError, ValueError):
            continue
        values.append(value)

    return sum(values) if values else None


def _load_li_mapping_data():
    return load_li_mapping_payload()


def _ensure_xlsx_suffix(filepath):
    return filepath if filepath.lower().endswith('.xlsx') else f"{filepath}.xlsx"


def _get_representative_occurrence(type_entity):
    elements = ifcopenshell.util.element.get_types(type_entity) or []
    return elements[0] if elements else None


def _get_occurrence_list(type_entity, occurrence=None, occurrences=None):
    if type_entity is None:
        if occurrences is not None:
            return occurrences
        return [occurrence] if occurrence is not None else []
    return ifcopenshell.util.element.get_types(type_entity) or []


def _get_entity_id(entity):
    if entity is None:
        return None
    return entity.id() if hasattr(entity, 'id') else id(entity)


def _has_type_assignment(entity):
    try:
        return ifcopenshell.util.element.get_type(entity) is not None
    except Exception:
        return bool(getattr(entity, 'IsTypedBy', None))


def _get_untyped_realizing_elements(model, excluded_ids=None):
    elements = []
    seen_ids = set()
    excluded_ids = excluded_ids or set()

    connection_rels = []
    for rel_type in ('IfcRelConnectsWithRealizingElements', 'IfcRelConnectsWithRealizing'):
        try:
            connection_rels.extend(model.by_type(rel_type))
        except RuntimeError:
            continue

    for rel in connection_rels:
        for entity in getattr(rel, 'RealizingElements', None) or []:
            if entity is None or not entity.is_a('IfcElement') or _has_type_assignment(entity):
                continue

            entity_id = _get_entity_id(entity)
            if entity_id in seen_ids or entity_id in excluded_ids:
                continue

            seen_ids.add(entity_id)
            elements.append(entity)

    return elements


def _group_occurrences_by_name(occurrences):
    groups = {}
    for occurrence in occurrences:
        name = (getattr(occurrence, 'Name', None) or '').strip()
        key = name or f"__id__:{_get_entity_id(occurrence)}"
        groups.setdefault(key, []).append(occurrence)
    return groups.values()


def _normalize_class_name(entity_name):
    if not entity_name:
        return ''
    normalized = str(entity_name)
    if normalized.startswith('Ifc'):
        normalized = normalized[3:]
    if normalized.endswith('Type'):
        normalized = normalized[:-4]
    return normalized


def _get_entity_attribute_value(entity, attribute_name):
    if entity is None or not attribute_name:
        return None

    if attribute_name == 'is_a':
        return _normalize_class_name(entity.is_a())

    return getattr(entity, attribute_name, None)


def _coalesce_entity_attribute(entities, attribute_name, fallback_attribute=None):
    for entity in entities:
        value = _get_entity_attribute_value(entity, attribute_name)
        if value not in (None, ''):
            return value

    if fallback_attribute:
        for entity in entities:
            value = _get_entity_attribute_value(entity, fallback_attribute)
            if value not in (None, ''):
                return value
    return None


def _get_parent_spatial_chain(entity):
    visited = set()
    queue = [entity]
    parents = []

    while queue:
        current = queue.pop(0)
        if current is None:
            continue
        entity_id = current.id() if hasattr(current, 'id') else id(current)
        if entity_id in visited:
            continue
        visited.add(entity_id)

        if getattr(current, 'ContainedInStructure', None):
            for rel in current.ContainedInStructure:
                structure = getattr(rel, 'RelatingStructure', None)
                if structure is not None:
                    parents.append(structure)
                    queue.append(structure)

        if getattr(current, 'Decomposes', None):
            for rel in current.Decomposes:
                parent = getattr(rel, 'RelatingObject', None)
                if parent is not None:
                    parents.append(parent)
                    queue.append(parent)

        if getattr(current, 'Nests', None):
            for rel in current.Nests:
                parent = getattr(rel, 'RelatingObject', None)
                if parent is not None:
                    parents.append(parent)
                    queue.append(parent)

    return parents


def _get_spatial_value(type_entity, occurrence, source):
    level_name = source.get('level')
    fallback_levels = source.get('fallback_levels', [])
    attribute = source.get('attribute')
    fallback_attribute = source.get('fallback_attribute')
    targets = [level_name] + list(fallback_levels)
    chain = _get_parent_spatial_chain(occurrence)

    for target in targets:
        for parent in chain:
            if parent.is_a(target):
                value = _coalesce_entity_attribute([parent], attribute, fallback_attribute)
                if value not in (None, ''):
                    return value
    return ''


def _get_aggregation_parent_chain(entity):
    """Walk only the Nests/Decomposes assembly chain, one level at a time.

    Unlike _get_parent_spatial_chain, this does not follow
    ContainedInStructure/IsGroupedBy, so spatial containers are not mixed into
    the assembly chain. chain[0] is the direct parent, chain[1] the grandparent,
    and so on.
    """
    chain = []
    current = entity
    visited = set()

    while True:
        parent = None
        if getattr(current, 'Nests', None):
            parent = current.Nests[0].RelatingObject
        elif getattr(current, 'Decomposes', None):
            parent = current.Decomposes[0].RelatingObject

        if parent is None:
            break
        entity_id = parent.id() if hasattr(parent, 'id') else id(parent)
        if entity_id in visited:
            break
        visited.add(entity_id)

        chain.append(parent)
        current = parent

    return chain


def _resolve_aggregation_parent(occurrence, source):
    """Read an attribute from a specific ancestor in the assembly chain.

    source:
      level              : ancestor level (1 = direct parent, 2 = grandparent).
                            Defaults to 1.
      attribute          : ancestor attribute to read (defaults to "Name").
      fallback_attribute : alternate attribute if the main one is empty.
    """
    try:
        level = int(source.get('level', 1))
    except (TypeError, ValueError):
        level = 1

    attribute = source.get('attribute') or 'Name'
    fallback_attribute = source.get('fallback_attribute')

    chain = _get_aggregation_parent_chain(occurrence)
    index = level - 1
    if index < 0 or index >= len(chain):
        return ''

    value = _coalesce_entity_attribute([chain[index]], attribute, fallback_attribute)
    return value if value not in (None, '') else ''


def _resolve_spatial_name_part(occurrence, source):
    """Extract information from the Name of the first matching ancestor.

    The search walks Nests/Decomposes/ContainedInStructure until it finds a Name
    containing the configured separator. This handles models where the actual
    spatial hierarchy does not distinguish platform/well, but the root segment
    Name encodes the line route, for example "P-52/7-RO-25D-RJS".

    source:
      separator   : separator used in the Name (defaults to "/").
      part_index  : split part index to return; if omitted, returns the full
                    Name without splitting.
    """
    separator = source.get('separator', '/')
    part_index = source.get('part_index')

    chain = [occurrence] + _get_parent_spatial_chain(occurrence)
    for entity in chain:
        name = getattr(entity, 'Name', None) or ''
        if separator not in name:
            continue
        if part_index is None:
            return name
        parts = name.split(separator)
        try:
            index = int(part_index)
        except (TypeError, ValueError):
            return name
        if 0 <= index < len(parts):
            return parts[index].strip()
        return ''
    return ''


def _get_property_value(entities, pset_name, property_name):
    for entity in entities:
        if entity is None:
            continue
        pset = ifcopenshell.util.element.get_pset(entity, pset_name)
        if not pset:
            continue
        value = pset.get(property_name)
        if value not in (None, ''):
            return value
    return ''


def _get_class_key(type_entity, occurrence, source):
    attribute = source.get('attribute', 'ObjectType')
    fallback_attribute = source.get('fallback_attribute')
    value = _coalesce_entity_attribute([occurrence, type_entity], attribute, fallback_attribute)
    fallback_entity = type_entity or occurrence
    if value in (None, '') and fallback_entity is not None:
        value = _normalize_class_name(fallback_entity.is_a())
    return value or ''


def _resolve_ifc_class(type_entity, occurrence, source, mapping_data):
    class_key = _get_class_key(type_entity, occurrence, source)
    mapping_table = mapping_data.get(source.get('mapping_table'), {})
    return mapping_table.get(class_key, class_key)


def _resolve_ifc_quantity(type_entity, occurrence, source, mapping_data, row_values, occurrences=None):
    quantity_mode = source.get('quantity_mode', 'mapping')
    if quantity_mode == 'count':
        return len(_get_occurrence_list(type_entity, occurrence, occurrences))
    if quantity_mode == 'length':
        if type_entity is None:
            occurrence_list = _get_occurrence_list(type_entity, occurrence, occurrences)
            quantity = _sum_occurrence_quantities(
                occurrence_list,
                source.get('qto'),
                source.get('quantity', 'Length'),
            )
            return quantity if quantity is not None else len(occurrence_list)
        return get_qtde(type_entity)

    mapping_table = mapping_data.get(source.get('mapping_table'), {})
    selected_by = source.get('selected_by')
    class_name = row_values.get(selected_by, '')
    class_key = _get_class_key(type_entity, occurrence, {'attribute': 'ObjectType', 'fallback_attribute': 'is_a'})
    quantity_rule = mapping_table.get(class_key) or mapping_table.get(class_name) or mapping_table.get('_default', {})
    quantity_name = quantity_rule.get('quantity', 'Count')

    if quantity_name.lower() == 'length':
        if type_entity is None:
            occurrence_list = _get_occurrence_list(type_entity, occurrence, occurrences)
            quantity = _sum_occurrence_quantities(
                occurrence_list,
                quantity_rule.get('qto'),
                quantity_name,
            )
            return quantity if quantity is not None else len(occurrence_list)
        return get_qtde(type_entity)
    return len(_get_occurrence_list(type_entity, occurrence, occurrences))


def _resolve_computed(type_entity, occurrence, source, mapping_data, row_values, occurrences=None):
    method = source.get('method')
    if method == 'quantity_unit_symbol':
        qtd_value = row_values.get(source.get('derived_from', ''), '')
        if qtd_value in (None, ''):
            return ''

        derived_column_name = source.get('derived_from', '')
        derived_column = None
        for column in mapping_data.get('columns', []):
            if column.get('column') == derived_column_name:
                derived_column = column
                break

        derived_source = (derived_column or {}).get('source') or {}
        quantity_mode = derived_source.get('quantity_mode', 'mapping')
        if quantity_mode == 'count':
            return 'un'
        if quantity_mode == 'length':
            return 'm'

        class_key = _get_class_key(type_entity, occurrence, {'attribute': 'ObjectType', 'fallback_attribute': 'is_a'})
        quantity_table = mapping_data.get('quantity_by_class', {})
        quantity_rule = quantity_table.get(class_key) or quantity_table.get('_default', {})
        quantity_name = quantity_rule.get('quantity', 'Count')
        if quantity_name.lower() == 'length':
            occurrence_list = _get_occurrence_list(type_entity, occurrence, occurrences)
            sample = occurrence_list[0] if occurrence_list else occurrence
            if sample is not None:
                qto_name = quantity_rule.get('qto')
                if qto_name:
                    model = get_model()
                    psets = ifcopenshell.util.element.get_psets(sample, should_inherit=False)
                    if qto_name in psets and quantity_name in psets[qto_name]:
                        qto = model.by_id(psets[qto_name]['id'])
                        for quantity in qto.Quantities or []:
                            if quantity.Name == quantity_name:
                                unit = ifcopenshell.util.unit.get_property_unit(model, quantity)
                                if unit is not None:
                                    return get_unit_symbol(unit)
            return 'm'
        return 'un'

    if method == 'spatial_name_part':
        return _resolve_spatial_name_part(occurrence, source)

    template_table_name = source.get('template_table')
    selected_by = source.get('selected_by')
    if template_table_name and selected_by:
        template_table = mapping_data.get(template_table_name, {})
        class_name = row_values.get(selected_by, '')
        template = template_table.get(class_name) or template_table.get('_default', '')
        return _render_template(template, type_entity, occurrence)

    return ''


def _render_template(template, type_entity, occurrence):
    if not template:
        return ''

    entities = [occurrence, type_entity]

    def _replace(match):
        token = match.group(1)
        if token.startswith('attr.'):
            attr_name = token.split('.', 1)[1]
            value = _coalesce_entity_attribute(entities, attr_name)
            return '' if value in (None, '') else str(value)

        if '.' in token:
            pset_name, prop_name = token.split('.', 1)
            value = _get_property_value(entities, pset_name, prop_name)
            return '' if value in (None, '') else str(value)

        return ''

    return re.sub(r'\{([^{}]+)\}', _replace, template)


def _resolve_column_value(column_data, type_entity, occurrence, mapping_data, row_values, occurrences=None):
    source_type = column_data.get('source_type')
    source = column_data.get('source') or {}
    entities = [occurrence, type_entity]

    if source_type == 'ifc_attribute':
        return _coalesce_entity_attribute(entities, source.get('attribute'), source.get('fallback_attribute')) or ''

    if source_type in {'ifc_property', 'manual'}:
        return _get_property_value(entities, source.get('pset'), source.get('property'))

    if source_type == 'material':
        return resolve_material_information(type_entity, occurrence, source)

    if source_type == 'spatial':
        return _get_spatial_value(type_entity, occurrence, source)

    if source_type == 'aggregation_parent':
        return _resolve_aggregation_parent(occurrence, source)

    if source_type == 'ifc_class':
        return _resolve_ifc_class(type_entity, occurrence, source, mapping_data)

    if source_type == 'ifc_quantity':
        return _resolve_ifc_quantity(type_entity, occurrence, source, mapping_data, row_values, occurrences)

    if source_type == 'computed':
        return _resolve_computed(type_entity, occurrence, source, mapping_data, row_values, occurrences)

    if source_type == 'not_applicable':
        return ''

    return ''


def _build_li_row(type_entity, occurrence, mapping_data, occurrences=None):
    row_values = {}
    for column_data in mapping_data.get('columns', []):
        column_name = column_data.get('column', '')
        row_values[column_name] = _resolve_column_value(
            column_data,
            type_entity,
            occurrence,
            mapping_data,
            row_values,
            occurrences,
        )
    return row_values


def _build_li_rows(model, mapping_data):
    rows = []
    typed_occurrence_ids = set()

    for type_entity in model.by_type('IfcTypeProduct'):
        occurrences = _get_occurrence_list(type_entity)
        if not occurrences:
            continue

        typed_occurrence_ids.update(
            entity_id
            for entity_id in (_get_entity_id(entity) for entity in occurrences)
            if entity_id is not None
        )
        rows.append(_build_li_row(type_entity, occurrences[0], mapping_data))

    untyped_realizing_elements = _get_untyped_realizing_elements(model, typed_occurrence_ids)
    for occurrence_group in _group_occurrences_by_name(untyped_realizing_elements):
        rows.append(_build_li_row(None, occurrence_group[0], mapping_data, occurrence_group))

    return rows
            
def update_predefined_types():
    model = get_model()
    for entity in model.by_type('IfcElement'):
        if entity.IsTypedBy:
            type = entity.IsTypedBy[0].RelatingType
            if type.ElementType:
                object_type = type.ElementType.replace("Type", "")
                entity.ObjectType = object_type
                entity.PredefinedType = None
    

class Operator_load_products(bpy.types.Operator):
    """"""
    bl_idname  = "catag.load_products"
    bl_label   = "load products from catalog"
    bl_options = {"REGISTER", "UNDO"}    

    def execute(self, context): 
        props = context.scene.og_props               
        props.types.clear()
        props.types_loaded = True
        model = get_model()
        types = model.by_type('IfcTypeProduct')
        c = -1
        result = {}
        data = Catalog.get_ifc_type()
        classe_title = {
            'name': '',
            'tag': '',
            'description' : '',
            'element_type': '',
            'id' : 0
        }

        for type in types:
            dic = {}   
            dic['id'] = type.id()         
            dic['name'] = type.Name or  ''
            dic['tag'] = type.Tag or  ''
            dic['description'] = type.Description or ''
            dic['element_type'] = type.ElementType or ''
            dic['qtde'] = get_qtde(type)
            dic['unit'] = 'm' if type.is_a('IfcPipeSegmentType') else 'un'
            
            if type.ElementType not in result:
                result[type.ElementType] = []
            result[type.ElementType].append(dic)
        
        for key, values in  result.items():
                if key in data:
                    classe_title['name'] = data[key]
                else:
                    classe_title['name'] = key
                new_c = build_products(context, classe_title, c, 1, '', False, True)
                c += 1
                print(values)
                for value in values:
                    new_c = build_products(context, value, c, 2, '', True, False)
                    c = new_c
        refresh_types(context)
        return {"FINISHED"} 

class Operator_catalog_show_layers(bpy.types.Operator):
    """"""
    bl_idname  = "catag.show_layers"
    bl_label   = "show layers of the type"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

    def _build_html(self, type_name, type_props, nested_elements):
        import html as html_mod
        props_rows = "<tr><td>No properties found</td><td></td></tr>"
        for pset_name, pset_values in type_props.items():
            for prop, value in pset_values.items():
                props_rows += f"<tr><td>{html_mod.escape(str(prop))}</td><td>{html_mod.escape(str(value))}</td></tr>\n"

        all_columns = []
        columns_set = set()
        layers_data = []

        for nest in nested_elements:
            nest_name = getattr(nest, 'Name', '') or ''
            obj_type = getattr(nest, 'ObjectType', '') or ''
            label = f"{nest_name} [{obj_type}]" if obj_type else nest_name
            nest_psets = ifcopenshell.util.element.get_psets(nest)

            values = {}
            for pset_name, pset_values in nest_psets.items():
                for prop, value in pset_values.items():
                    if prop == 'id':
                        continue
                    key = (pset_name, prop)
                    values[key] = value
                    if key not in columns_set:
                        columns_set.add(key)
                        all_columns.append(key)

            layers_data.append({"label": label, "values": values})

        header_cells = "<th>Layer</th>"
        for pset, prop in all_columns:
            header_cells += f"<th>{html_mod.escape(prop)}<br><small>{html_mod.escape(pset)}</small></th>"

        layer_rows = ""
        for layer in layers_data:
            cells = f"<td><strong>{html_mod.escape(layer['label'])}</strong></td>"
            for key in all_columns:
                val = layer["values"].get(key, "")
                cells += f"<td>{html_mod.escape(str(val))}</td>"
            layer_rows += f"<tr>{cells}</tr>\n"

        report = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>{html_mod.escape(type_name)} - Layers</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
                h2 {{ color: #569cd6; }}
                h3 {{ color: #9cdcfe; margin-top: 24px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #3c3c3c; padding: 8px 12px; text-align: left; white-space: nowrap; }}
                th {{ background: #264f78; color: #ffffff; }}
                th small {{ color: #9cdcfe; font-weight: normal; }}
                tr:nth-child(even) {{ background: #2d2d2d; }}
                tr:hover {{ background: #37373d; }}
                .table-wrapper {{ overflow-x: auto; }}
            </style>
            </head>
            <body>
            <h2>{html_mod.escape(type_name)}</h2>

            <h3>Pipe Structure Properties</h3>
            <table>
                <tr><th>Property</th><th>Value</th></tr>
                {props_rows}
            </table>"""

        layers = f"""<h3>Layers</h3>
            <div class="table-wrapper">
            <table>
                <tr>{header_cells}</tr>
                {layer_rows}
            </table>
            </div>

            </body>
            </html>"""
        
        if len(layers_data) > 0:
            report += layers

        return report
    
    def execute(self, context):                             
        return {"FINISHED"}

    def invoke(self, context, event):
        model = get_model()
        ifc_type = model.by_id(self.id)   

        if ifc_type is not None:                
            type_name = ifc_type.Name or str(self.id)
            type_props = ifcopenshell.util.element.get_psets(ifc_type, psets_only=True)
            nested_elements = ifcopenshell.util.element.get_components(ifc_type) or []
            print(nested_elements)

            html = self._build_html(type_name, type_props, nested_elements)
            html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "layers.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            _open_in_browser(Path(html_path).as_uri())

            self.report({'INFO'}, "Layers opened in browser")
            return {"FINISHED"}
        else:
            self.report({'ERROR'}, f"No type found for id {self.id}")
            return {"CANCELLED"}

class Operator_catalog_select_layer(bpy.types.Operator):
    """"""
    bl_idname  = "catag.select_layer"
    bl_label   = "select elements of the layer"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

            
    def execute(self, context): 
            props = context.scene.og_props                     
            model = get_model()
            layer = model.by_id(self.id)           

            obj_blender = get_object(layer)
            if obj_blender:
                obj_blender.select_set(True)
                context.view_layer.objects.active = obj_blender

                self.report({'OPERATOR'}, 'Done!')
                return {"FINISHED"}    
            else:
                self.report({'ERROR'}, f"No layer found for id {self.id}")
                return {"CANCELLED"}        

class Operator_catalog_select_elements(bpy.types.Operator):
    """"""
    bl_idname  = "catag.select_elements"
    bl_label   = "select elements of the type"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

            
    def execute(self, context): 
            props = context.scene.og_props                     
            model = get_model()
            type = model.by_id(self.id)           
            elements=[]
            if type is not None:
                if getattr(type, "Types", None):
                    rels = [e for e in type.Types]                    
                    for rel in rels:
                        elements.extend(rel.RelatedObjects)

                for element in elements:
                    obj_blender = get_object(element)
                    if obj_blender:
                        obj_blender.select_set(True)
                        context.view_layer.objects.active = obj_blender

                self.report({'OPERATOR'}, 'Done!')
                return {"FINISHED"}    
            else:
                self.report({'ERROR'}, f"No type found for id {self.id}")
                return {"CANCELLED"}

class Operator_export_qtds(bpy.types.Operator):
    """"""
    bl_idname  = "catag.export_qtds"
    bl_label   = "export quantities to json"
    bl_options = {"REGISTER", "UNDO"}  
    filepath : bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context): 
            props = context.scene.og_props                     
            dic = {
                'Type Name': [],
                'Quantity': [],
                'Unit': []
            }
            for item in props.types:
                if item.qtde > 0:
                    dic['Type Name'].append(item.name)
                    dic['Quantity'].append(item.qtde)
                    dic['Unit'].append('un')
            df = pd.DataFrame(dic)

            df.to_excel(self.filepath + '.xlsx', index=False, engine='openpyxl')
            self.report({'INFO'}, f"Quantities exported to {self.filepath}.xlsx")
            return {"FINISHED"}


class Operator_export_li(bpy.types.Operator):
    bl_idname = "catag.export_li"
    bl_label = "export LI to excel"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        try:
            props = context.scene.og_props
            if props.li_mapping_loaded:
                mapping_data = li_mapping_payload_from_props(
                    props,
                    load_li_mapping_payload(),
                )
            else:
                mapping_data = _load_li_mapping_data()
            model = get_model()
            rows = _build_li_rows(model, mapping_data)
            if not rows:
                self.report({'WARNING'}, 'No LI rows could be generated from the current IFC model')
                return {'CANCELLED'}

            columns = [column.get('column', '') for column in mapping_data.get('columns', [])]
            df = pd.DataFrame(rows, columns=columns)
            output_path = _ensure_xlsx_suffix(self.filepath)
            df.to_excel(output_path, index=False, engine='openpyxl')
        except Exception as exc:
            self.report({'ERROR'}, f"Failed to export LI: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"LI exported to {output_path}")
        return {'FINISHED'}
