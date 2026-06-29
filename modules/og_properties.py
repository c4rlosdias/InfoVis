import bpy
from bpy.types import PropertyGroup
from bpy.props import *
import bonsai.tool as tool
import ifcopenshell
import ifcopenshell.util.element

from ..data.bsdd import bSDD
from ..data.cde import CDE_Api
from .dictionary.properties import Ifc_properties, Class_info, Class_prop_info
from .catalog.properties import Class_type, Layer, LIMappingColumn, LIMappingSourceItem, LISupportTable, LISupportTableRow
from .props.properties import Enumeration_values, Property_info, Documents, Pset_info
from .decomposition.properties import Container
from .analysis.properties import AnalysisLegendItem
from .analysis.service import (
    ANALYSIS_DISCIPLINE_ITEMS,
    analysis_get_object_types,
    analysis_get_properties,
    analysis_get_psets,
    analysis_get_values,
    invalidate_analysis_value_cache,
)


class IFC_Label_Attribute(PropertyGroup):
    """Um atributo IFC a ser exibido na viewport overlay."""
    attr_name : StringProperty(name='Attribute', default='Name')
    display_name : StringProperty(name='Display text', default='')


class Decomposition_View_Relation(PropertyGroup):
    element_attribute : StringProperty(name='Element attribute', default='IsDecomposedBy')
    relationship_type : StringProperty(name='Relationship type', default='IfcRelAggregates')
    relationship_attribute : StringProperty(name='Relationship attribute', default='RelatedObjects')


class Decomposition_View(PropertyGroup):
    id : StringProperty(name='ID', default='assets')
    label : StringProperty(name='Label', default='Assets')
    root_ifc_class : StringProperty(name='Root IFC class', default='IfcProject')
    relations : CollectionProperty(name='IFC relations', type=Decomposition_View_Relation)


def analysis_selection_changed(self, context):
    self.analysis_status = ''
    legend = getattr(self, "analysis_legend", None)
    if legend is not None:
        legend.clear()
    invalidate_analysis_value_cache()


# update function for the decomposition tree 
def _update_tree_type(self, context):
    def add_elements(elements,level=0):
        new = self.elements_tree.add()
        for element in elements:
            new.name = element['name'] or 'Unnamed'
            new.object_type = element['id'] or 'Unnamed'
            new.level = level
            new.is_expanded = False
            
            if 'objects' in element and len(element['objects']) > 0:
                new.has_children = True
                add_elements(element['objects'], level=level+1)
            else:
                new.has_children = False

    cde = CDE_Api('')
    elements_tree = []

    i = 0    
    for element in elements_tree:
        elements_tree = cde.get_contracts(self.containers_show[self.active_element_index])
        self.elements_tree.clear()
        new = self.elements_tree.add()
        new.name = element['name'] or 'Unnamed'        
        new.object_type = element['id'] or 'Unnamed'
        new.level = 0
        new.is_expanded = False
        new.has_children = True if 'objects' in element and len(element['objects']) > 0 else False
        if 'objects' in element and len(element['objects']) > 0:
            add_elements(element['objects'], level=1)

        new.is_hidden = False if new.has_children else True
        i += 1

def update_tree_type(self, context):
    bpy.ops.decomposition.load(all_expanded=False)


def get_decomposition_view_items(self, context):
    try:
        from ..data.tree import load_views
        items = []
        for view in load_views():
            view_id = view.get("id", "").strip()
            if view_id:
                items.append((
                    view_id,
                    view.get("label") or view_id,
                    view.get("root_ifc_class", ""),
                ))
        return items or [('assets', 'Assets', 'IfcProject')]
    except Exception:
        return [('assets', 'Assets', 'IfcProject')]
    


def _get_dictionaries(self, context):                
    if not bSDD.is_loaded:
        bSDD.load_dictionaries()
    return bSDD.data_dic
        
def get_dictionaries(self, context):                
    dictionaries = [
       ('https://identifier.buildingsmart.org/uri/bs-energy/subsea-flexible-pipes/2.1', 'Subsea Flexible Pipes v2.1', '2.1'),
       ('https://identifier.buildingsmart.org/uri/bs-energy/subsea-rigid-pipelines/1.0', 'Subsea Rigid Pipelines v1.0', '1.0')
    ]
    return dictionaries

def active_prop_changed(self, context):
    self.info_class_prop_loaded = False
    self.class_info.clear()

def active_class_changed(self, context):
    self.class_prop_info.clear()
    self.classes_loaded = False
    self.class_prop_info_loaded = False

def active_class_prop_changed(self, context):
    return None

def active_product_changed(self, context):
    global _updating_element
    type_id = self.types_show[self.active_type_index].id if self.active_type_index < len(self.types_show) else None
    print(f"Active type ID: {type_id}")
    if type_id is not None and type_id != 0:
        model = tool.Ifc.get()
        ifc_type = model.by_id(type_id)
        
        nested_elements = ifcopenshell.util.element.get_components(ifc_type) or []
        print(f"Selected type: {nested_elements}")
        self.layers.clear()

        for element in nested_elements:            
            new_layer = self.layers.add()
            new_layer.id = element.id()
            new_layer.name = element.Name or f"Element {element.id()}"
            new_layer.description = element.get_info() or ''

        obj = tool.Ifc.get_object(ifc_type)
        if obj:
            bpy.ops.object.select_all(action='DESELECT')
            if obj.hide_get():
                obj.hide_set(False)
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.props.load_properties()

    self.product_loaded = False

def active_type_changed(self, context):
    self.types_loaded = False

def active_element_changed(self, context):
    from ..data import tree as _data_tree
    if _data_tree._syncing_tree:
        return
    
    model = tool.Ifc.get()
    print(f"Active element index: {self.active_element_index}")
    ifc_id = self.containers_show[self.active_element_index].id if self.active_element_index < len(self.containers_show) else None
    if ifc_id is None:
        return
    ifc_element = model.by_id(ifc_id)
    obj = tool.Ifc.get_object(ifc_element)
    if obj is None:
        return
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    context.view_layer.objects.active = obj

    # view type layers
    type_ifc = ifcopenshell.util.element.get_type(ifc_element) if ifc_element is not None else None
    type_id = type_ifc.id() if type_ifc is not None else None    
    if type_id is not None:
        model = tool.Ifc.get()
        ifc_type = model.by_id(type_id)
        print(f"Selected type: {ifc_type}")
        nested_elements = ifcopenshell.util.element.get_components(ifc_type) or []
        print(f"Selected type: {nested_elements}")
        self.layers.clear()

        for element in nested_elements:            
            new_layer = self.layers.add()
            new_layer.id = element.id()
            new_layer.name = element.Name or f"Element {element.id()}"
            new_layer.description = element.get_info() or ''

    # view associated contracts
    cde = CDE_Api('')
    elements_tree = []
    elements_tree = cde.get_contracts(self.containers_show[self.active_element_index])

    i = 0
    print(f"Elements tree: {elements_tree}")
    for element in elements_tree:
        self.elements_tree.clear()
        new = self.elements_tree.add()
        new.name = element['name'] or 'Unnamed'        
        new.object_type = element['description'] or 'Unnamed'
        new.level = 0
        new.is_expanded = False
        #new.has_children = True if 'objects' in element and len(element['objects']) > 0 else False
        # if 'objects' in element and len(element['objects']) > 0:
        #     add_elements(element['objects'], level=1)

        new.is_hidden = False 
        i += 1

def load_products(self, context):   
    props = context.scene.my_props
    if props.products_loaded:             
        products = [
                ('pipe1','Pipe 1','Pipe 1'),
                ('pipe2','Pipe 2','Pipe 2'),
                ('valve1','Valve 3','Valve 1')
        ]

    else:
        products = [] 
    return products


class OG_Properties(PropertyGroup): 
    
    # O&G Dictionary

    dictionary                 : EnumProperty(items=get_dictionaries, name='',  description='Get Dictionaries')
    #dictionary                 : EnumProperty(items=get_dictionaries, name='',  description='Get Dictionaries')  
    active_property_index      : IntProperty(name='property index', default=0, update=active_prop_changed)
    ifc_prop                   : CollectionProperty(name='properties', type=Ifc_properties) 
    active_info_prop_index     : IntProperty(name='object index', default=0)
    class_info                 : CollectionProperty(name='info class', type=Class_info)    
    active_class_index         : IntProperty(name='class index', default=0, update=active_class_changed)
    active_class_prop_index    : IntProperty(name='class prop index', default=0, update=active_class_prop_changed)
    classes                    : CollectionProperty(name='classes', type=Class_info) 
    classes_shown              : CollectionProperty(name='classes show', type=Class_info) 
    
    active_tree_element_index  : IntProperty(name='element index', default=0)
    
    # Decomposition

    tree_type                : EnumProperty(
                                    items=get_decomposition_view_items,
                                    name='Tree Type',
                                    update=update_tree_type
                               ) # type: ignore
    active_element_index     : IntProperty(name='element index', default=0, update=active_element_changed)
    elements_containers      : CollectionProperty(name='elements containers', type=Container)  # type: ignore
    containers_show          : CollectionProperty(name='containers show', type=Container)  # pyright: ignore[reportInvalidTypeForm]
    elements_tree            : CollectionProperty(name='elements tree', type=Container)
    elements_tree_show       : CollectionProperty(name='elements tree show', type=Container)
    decomposition_views      : CollectionProperty(name='decomposition views', type=Decomposition_View)
    active_decomposition_view_index : IntProperty(name='decomposition view index', default=0)
    active_decomposition_relation_index : IntProperty(name='decomposition relation index', default=0)
    decomposition_views_loaded : BoolProperty(name='decomposition views loaded', default=False)
    
    show_agg                 : BoolProperty(name="change aggregations", default=False)
    chg_order                : BoolProperty(name="change order", default=False)
    agg_type                 : EnumProperty (
                                    name="aggregation type",
                                    items=[     
                                        ("nests", "Nests", ""),
                                        ("aggregations", "Aggregations", "")
                                    ]
                             )


    add_prop_clicked         : BoolProperty(name="add property clicked", default=False)
    class_description        : StringProperty(name='class description') 
    class_definition         : StringProperty(name='class definition')
    class_version            : StringProperty(name='class version date') 
    class_type               : StringProperty(name='class type') 
    class_ifctype            : StringProperty(name='ifc class') 
    classes_loaded           : BoolProperty(name='classes loaded', default=False)   
    dictionaries_loaded      : BoolProperty(name='Dictionaries loaded')
      
    prop_datatype            : StringProperty(name='property data type')
    prop_units               : StringProperty(name='property units')
    prop_type                : StringProperty(name='property type')
    prop_description         : StringProperty(name='property description')
    prop_definition          : StringProperty(name='property definition')

    class_prop_info          : CollectionProperty(name="class prop info", type=Class_prop_info)
    
    info_prop_loaded         : BoolProperty(name='info prop loaded', default=False)
    info_class_loaded        : BoolProperty(name='info class loaded', default=False)
    info_class_prop_loaded   : BoolProperty(name='info class prop loaded', default=False)
    ids_file                 : StringProperty(name='IDS file')
    
    
    # O&G Catalog
    products                 : CollectionProperty(name="products", type=Class_info)
    types                    : CollectionProperty(name="types", type=Class_type)    
    types_show               : CollectionProperty(name="types", type=Class_type)           
    products_show            : CollectionProperty(name="products", type=Class_info)
    products_loaded          : BoolProperty(name="products loaded", default=False)
    types_loaded             : BoolProperty(name="products loaded", default=False)
    active_product_index     : IntProperty(name='product index', default=0, update=active_product_changed)
    active_type_index        : IntProperty(name='product index', default=0, update=active_product_changed)
    product_description      : StringProperty(name='product description', default='')
    layers                   : CollectionProperty(name="layers", type=Container)
    active_layer_index       : IntProperty(name='layer index', default=0)
    active_type_id          : IntProperty(name='active type id', default=0)
    li_mapping_schema_version : StringProperty(name='LI mapping schema version', default='1.0')
    li_mapping_description    : StringProperty(name='LI mapping description', default='')
    li_mapping_reference_sheet: StringProperty(name='LI mapping reference sheet', default='')
    li_mapping_columns        : CollectionProperty(name='LI mapping columns', type=LIMappingColumn)
    active_li_mapping_index   : IntProperty(name='LI mapping index', default=0)
    li_support_tables         : CollectionProperty(name='LI support tables', type=LISupportTable)
    active_li_support_table_index : IntProperty(name='LI support table index', default=0)
    li_mapping_loaded         : BoolProperty(name='LI mapping loaded', default=False)

    # O&G Properties
    active_pset_index        : IntProperty(name='pset index', default=0)
    prop_metadata            : CollectionProperty(name="psets", type=Pset_info)
    active_property_index    : IntProperty(name='property index', default=0)
    icon_edit_prop           : StringProperty(name='icon edit property', default='GREASEPENCIL')
    invert_xy                : BoolProperty(name="invert xy", default=False)
    pset_index               : IntProperty(name='pset index', default=0)
    prop_index               : IntProperty(name='prop index', default=0)
    XAxis                    : StringProperty(name='property of the X axis')
    show_description         : BoolProperty(name='Show property description', default=True ) 

    has_document             : BoolProperty(name='Has documentation', default=False)
    docs_expanded            : BoolProperty(name='is expanded', default=True)
    document                 : StringProperty(name='document')
    documents                : CollectionProperty(name='documents', type=Documents)

    show_table               : BoolProperty(name='Show table', default=False)

    # Analysis
    analysis_discipline      : EnumProperty(
                                 items=ANALYSIS_DISCIPLINE_ITEMS,
                                    name='Discipline',
                                    default='flexible_pipes',
                                    update=analysis_selection_changed,
                               )
    analysis_object_type     : EnumProperty(
                                    items=analysis_get_object_types,
                                    name='ObjectType',
                                    update=analysis_selection_changed,
                               )
    analysis_pset            : EnumProperty(
                                    items=analysis_get_psets,
                                    name='Property set',
                                    update=analysis_selection_changed,
                               )
    analysis_property        : EnumProperty(
                                    items=analysis_get_properties,
                                    name='Property',
                                    update=analysis_selection_changed,
                               )
    analysis_color_mode      : EnumProperty(
                                    items=[
                                        ('distinct', 'Distinct values', 'Color each distinct value with a different color'),
                                        ('exact', 'Exact value', 'Highlight a single selected value'),
                                        ('range', 'Numeric range', 'Color numeric values within a selected range'),
                                    ],
                                    name='Analysis mode',
                                    default='distinct',
                                    update=analysis_selection_changed,
                               )
    analysis_value           : EnumProperty(
                                    items=analysis_get_values,
                                    name='Value',
                                    update=analysis_selection_changed,
                               )
    analysis_range_min       : FloatProperty(name='Range min', default=0.0, update=analysis_selection_changed)
    analysis_range_max       : FloatProperty(name='Range max', default=0.0, update=analysis_selection_changed)
    analysis_status          : StringProperty(name='Analysis status', default='')
    analysis_legend          : CollectionProperty(name='Analysis legend', type=AnalysisLegendItem)

    # Viewport overlays
    show_ifc_label              : BoolProperty(name='Show IFC label', description='Show the IFC element name in the viewport when selected', default=True)
    ifc_label_attributes        : CollectionProperty(name='IFC label attributes', type=IFC_Label_Attribute)
    active_ifc_label_attr_index : IntProperty(name='active attribute index', default=0)
    label_offset_x              : FloatProperty(name='Offset X', description='Horizontal label offset from the object (px)', default=80.0, min=-500.0, max=500.0)
    label_offset_y              : FloatProperty(name='Offset Y', description='Vertical label offset from the object (px)', default=80.0, min=-500.0, max=500.0)

    # Element Connections
    connect_type             : EnumProperty(
                                    name="Connection Type",
                                    items=[
                                        ("IfcRelConnectsPorts", "IfcRelConnectsPorts",""),
                                        ("IfcRelConnectsElements", "IfcRelConnectsElements",""),
                                        ("IfcRelConnectsWithRealizingElements", "IfcRelConnectsWithRealizingElements","")
                                    ],                                
                                    default="IfcRelConnectsElements"
                                )
