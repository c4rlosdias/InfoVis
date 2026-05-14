import bpy
from bpy.types import PropertyGroup
from bpy.props import *
import bonsai.tool as tool
import ifcopenshell
import ifcopenshell.util.element

from ..data.bsdd import bSDD
from ..data.cde import CDE_Api
from .dictionary.properties import Ifc_properties, Class_info, Class_prop_info
from .catalog.properties import Class_type, Layer
from .props.properties import Enumeration_values, Property_info, Documents, Pset_info
from .decomposition.properties import Container


# update function for the decomposition tree 
def update_tree_type(self, context):
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
    if self.tree_type == 'assets':
        elements_tree = cde.get_assets()    
    elif self.tree_type == 'contracts':
        elements_tree = cde.get_contracts()
    elif self.tree_type == 'inventory':
        elements_tree = cde.get_inventory()
    i = 0
    
    for element in elements_tree:
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
    self.info_class_prop_loaded = False

def active_product_changed(self, context):
    global _updating_element
    type_id = self.types_show[self.active_type_index].id if self.active_type_index < len(self.types_show) else None
    print(f"Active type ID: {type_id}")
    if type_id is not None:
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
    type_id = ifcopenshell.util.element.get_type(ifc_element).id() if ifc_element is not None else None
    print(f"Active type ID: {type_id}")
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
                                    items=[
                                        ('assets', 'Assets', 'Assets'),
                                        ('contracts', 'Contracts', 'Contracts'),
                                        ('inventory', 'Inventory', 'Inventory')                                        
                                    ],
                                    name='Tree Type',
                                    update=update_tree_type
                               ) # type: ignore
    active_element_index     : IntProperty(name='element index', default=0, update=active_element_changed)
    elements_containers      : CollectionProperty(name='elements containers', type=Container)  # type: ignore
    containers_show          : CollectionProperty(name='containers show', type=Container)  # pyright: ignore[reportInvalidTypeForm]
    elements_tree            : CollectionProperty(name='elements tree', type=Container)
    elements_tree_show       : CollectionProperty(name='elements tree show', type=Container)
    
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
