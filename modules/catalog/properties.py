import bpy
from bpy.types import PropertyGroup
from bpy.props import *

from ...data.bsdd_dictionary import (
    DICTIONARY_DISCIPLINE_ITEMS,
    get_object_type_items,
    get_pset_items,
    get_property_items,
)


class Class_type(PropertyGroup):
    id           : IntProperty(name='id')
    tag          : StringProperty(name='tag')
    name         : StringProperty(name='name')
    description  : StringProperty(name='description')
    element_type : StringProperty(name='element type')
    has_children : BoolProperty(name="has children")    
    is_hidden    : BoolProperty(name="is hidden", default=True)
    is_expanded  : BoolProperty(name="Is Expanded", default=True)
    index        : IntProperty(name="index")
    parent       : StringProperty(name="parent")
    level        : IntProperty(name="level index")
    qtde         : FloatProperty(name="quantity of elements of this type")
    unit         : StringProperty(name="unit of measurement for quantity")


class Layer(PropertyGroup):
    id            : IntProperty(name="id")
    name          : StringProperty(name="name")
    description   : StringProperty(name="description")


LI_SOURCE_TYPE_ITEMS = [
    ('ifc_attribute', 'IFC Attribute', 'Direct attribute from the IFC entity'),
    ('ifc_property', 'IFC Property', 'Property inside a Pset'),
    ('ifc_quantity', 'IFC Quantity', 'Quantity inside a Qto'),
    ('ifc_class', 'IFC Class', 'IFC class/type of the occurrence'),
    ('spatial', 'Spatial', 'Value derived from the spatial hierarchy'),
    ('aggregation_parent', 'Aggregation Parent', 'Attribute from an assembly ancestor (Nests/IfcRelAggregates); use Level=1 for the direct parent, 2 for the grandparent, etc.'),
    ('computed', 'Computed', 'Value calculated from other fields'),
    ('manual', 'Manual', 'Manual value or custom property'),
    ('not_applicable', 'Not Applicable', 'Field with no direct IFC relationship'),
]


LI_QUANTITY_MODE_ITEMS = [
    ('mapping', 'Mapping Table', 'Uses the quantity mapping table by class'),
    ('count', 'Count Occurrences', 'Counts how many occurrences exist for the IFC type'),
    ('length', 'Sum Length', 'Sums length for linear types'),
]


class LIMappingSourceItem(PropertyGroup):
    key   : StringProperty(name='key')
    value : StringProperty(name='value')


class LISupportTableRow(PropertyGroup):
    key   : StringProperty(name='key')
    value : StringProperty(name='value')


class LISupportTable(PropertyGroup):
    table_name        : StringProperty(name='table name')
    description       : StringProperty(name='table description')
    rows              : CollectionProperty(name='rows', type=LISupportTableRow)
    active_row_index  : IntProperty(name='active row index', default=0)


def _li_picker_object_types(self, context):
    return get_object_type_items(self.picker_discipline)


def _li_picker_psets(self, context):
    return get_pset_items(self.picker_discipline, self.picker_object_type)


def _li_picker_properties(self, context):
    return get_property_items(self.picker_discipline, self.picker_object_type, self.picker_pset)


class LIMappingColumn(PropertyGroup):
    column_name              : StringProperty(name='column name')
    source_type              : EnumProperty(name='source type', items=LI_SOURCE_TYPE_ITEMS)
    notes                    : StringProperty(name='notes')
    source_ifc_class         : StringProperty(name='source ifc class')
    source_level             : StringProperty(name='source level')
    source_attribute         : StringProperty(name='source attribute')
    source_fallback_attribute: StringProperty(name='source fallback attribute')
    source_pset              : StringProperty(name='source pset')
    source_property          : StringProperty(name='source property')
    source_mapping_table     : StringProperty(name='source mapping table')
    source_quantity_mode     : EnumProperty(name='source quantity mode', items=LI_QUANTITY_MODE_ITEMS, default='mapping')
    source_selected_by       : StringProperty(name='source selected by')
    source_template_table    : StringProperty(name='source template table')
    source_derived_from      : StringProperty(name='source derived from')
    source_method            : StringProperty(name='source method')
    source_format            : StringProperty(name='source format')
    source_allowed_values    : StringProperty(name='source allowed values')
    source_items             : CollectionProperty(name='source items', type=LIMappingSourceItem)
    active_source_item_index : IntProperty(name='active source item index', default=0)

    # Guided picker: navigates the bSDD dictionary (resources/subsea_*.json)
    # as a cascade (Discipline -> Element -> Property set -> Property) to fill
    # source_pset/source_property without typing technical names by hand. See
    # Operator_li_mapping_pick_property.
    picker_discipline         : EnumProperty(name='Discipline', items=DICTIONARY_DISCIPLINE_ITEMS, default='flexible_pipes')
    picker_object_type        : EnumProperty(name='Element', items=_li_picker_object_types)
    picker_pset               : EnumProperty(name='Property set', items=_li_picker_psets)
    picker_property           : EnumProperty(name='Property', items=_li_picker_properties)
