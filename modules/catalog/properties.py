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
    is_hidden    : BoolProperty(name="is Hidded", default=True)
    is_expanded  : BoolProperty(name="Is Expanded", default=True)
    index        : IntProperty(name="index")
    parent       : StringProperty(name="parent")
    level        : IntProperty(name="level index")
    qtde         : FloatProperty(name="qtde of elements of this type")
    unit         : StringProperty(name="unit of measurement for quantity")


class Layer(PropertyGroup):
    id            : IntProperty(name="id")
    name          : StringProperty(name="name")
    description   : StringProperty(name="description")


LI_SOURCE_TYPE_ITEMS = [
    ('ifc_attribute', 'IFC Attribute', 'Atributo direto da entidade IFC'),
    ('ifc_property', 'IFC Property', 'Propriedade dentro de um Pset'),
    ('ifc_quantity', 'IFC Quantity', 'Quantidade dentro de um Qto'),
    ('ifc_class', 'IFC Class', 'Classe/tipo IFC da ocorrência'),
    ('spatial', 'Spatial', 'Valor derivado da hierarquia espacial'),
    ('aggregation_parent', 'Aggregation Parent', 'Atributo de um ancestral na cadeia de montagem (Nests/IfcRelAggregates) — use Nível=1 para o pai imediato, 2 para o avô, etc.'),
    ('computed', 'Computed', 'Valor calculado a partir de outros campos'),
    ('manual', 'Manual', 'Valor manual ou propriedade customizada'),
    ('not_applicable', 'Not Applicable', 'Campo sem relação direta com o IFC'),
]


LI_QUANTITY_MODE_ITEMS = [
    ('mapping', 'Mapping Table', 'Usa a tabela de mapeamento de quantidades por classe'),
    ('count', 'Count Occurrences', 'Conta quantas ocorrências existem para o tipo IFC'),
    ('length', 'Sum Length', 'Soma comprimento para tipos lineares'),
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
    editable                 : BoolProperty(name='editable', default=True)
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

    # Seletor guiado: navega pelo dicionário bSDD (resources/subsea_*.json)
    # em cascata (Discipline -> Element -> Property set -> Property) para
    # preencher source_pset/source_property sem precisar digitar os nomes
    # técnicos à mão. Ver Operator_li_mapping_pick_property.
    picker_discipline         : EnumProperty(name='Discipline', items=DICTIONARY_DISCIPLINE_ITEMS, default='flexible_pipes')
    picker_object_type        : EnumProperty(name='Element', items=_li_picker_object_types)
    picker_pset               : EnumProperty(name='Property set', items=_li_picker_psets)
    picker_property           : EnumProperty(name='Property', items=_li_picker_properties)
