import bpy
from bpy.types import PropertyGroup
from bpy.props import *
import bonsai.tool as tool
import ifcopenshell
import ifcopenshell.util.selector as selector
import requests
from .data import *

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

    # self.elements_containers.clear()
    # model = tool.Ifc.get()
     
    # # dependendo do tipo de decomposição selecionada, busca os elementos raiz para montar a árvore
    # if self.tree_type == 'assets':
    #     elements = selector.filter_elements(model, "IfcGroup, ObjectType=SubseaAsset")
    # elif self.tree_type == 'contracts':
    #     elements = selector.filter_elements(model, "IfcGroup, ObjectType=SubseaContract")
    # elif self.tree_type == 'inventory':
    #     elements = selector.filter_elements(model, "IfcGroup, ObjectType=SubseaInventory")
    # else:
    #     elements = []

    # if len(elements) > 0:
    #     for element in elements: 
    #         load_contained_elements_by_decomposition(element, 'elements_tree', context)  
    #     i = 0          
    #     for element in self.elements_containers:
    #         element.index = i
    #         element.is_hidden = False if element.level==1 else True
    #         element.is_expanded = False if element.level==1 else True  
    #         i += 1   
    #     refresh_container(context)

def get_dictionaries(self, context):                
    if not bSDD.is_loaded:
        bSDD.load_dictionaries()
    return bSDD.data_dic
        
def active_prop_changed(self, context):
    self.info_class_prop_loaded = False
    self.class_info.clear()


def active_class_changed(self, context):
    self.class_prop_info.clear()
    self.classes_loaded = False
    self.class_prop_info_loaded = False

def active_class_prop_changed(self, context):
    #self.classes_shown.clear()
    self.info_class_prop_loaded = False

def active_product_changed(self, context):
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

    self.product_loaded = False

def active_type_changed(self, context):
    #self.classes_shown.clear()
    self.types_loaded = False

def active_element_changed(self, context):
    model = tool.Ifc.get()
    print(f"Active element index: {self.active_element_index}")
    for element in self.containers_show:
        if element.index == self.active_element_index:
            o = tool.Ifc.get_entity(model.by_id(element.id))
            print(f"Selected element: {o}")
        else:
            element.is_selected = False


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

class Ifc_properties(PropertyGroup):       
    name        : StringProperty(name='name')
    code        : StringProperty(name='code')
    description : StringProperty(name='description')
    uri         : StringProperty(name="uri")
    is_selected : BoolProperty(name="is selected", default=True)

class Class_info(PropertyGroup):
    code        : StringProperty(name='code')
    name        : StringProperty(name='name')
    description : StringProperty(name='description')
    uri         : StringProperty(name='uri')    
    propertyset : StringProperty(name='property set')
    has_children: BoolProperty(name="has children")    
    is_hidden   : BoolProperty(name="is Hidded", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    index       : IntProperty(name="index")
    parent      : StringProperty(name="parent")
    level       : IntProperty(name="level")
    type        : StringProperty(name="class type")

class Class_type(PropertyGroup):
    id          : IntProperty(name='id')
    tag         : StringProperty(name='tag')
    name        : StringProperty(name='name')
    description : StringProperty(name='description')
    element_type : StringProperty(name='element type')
    has_children: BoolProperty(name="has children")    
    is_hidden   : BoolProperty(name="is Hidded", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    index       : IntProperty(name="index")
    parent      : StringProperty(name="parent")
    level       : IntProperty(name="level index")


class Enumeration_values(PropertyGroup):        
    enumerated  : BoolProperty(name="enumerated", default=False)
    valuestr    : StringProperty(name="value str")
    valueint    : IntProperty(name='value int')
    valuefloat  : FloatProperty(name='value float')
    valuebool   : BoolProperty(name="value bool")
    datatype    : StringProperty(name='data type', default='')
    type_value  : StringProperty(name="type value")

class Property_info(PropertyGroup):    
    
    index        : IntProperty(name='prop index')
    name         : StringProperty(name='property name')
    description  : StringProperty(name='property description')
    valuestr     : StringProperty(name='value str')
    valueint     : IntProperty(name='value int')
    valuefloat   : FloatProperty(name='value float')
    valuebool    : BoolProperty(name="value bool")
    type_value   : StringProperty(name="type value")
    type_prop    : StringProperty(name='typr prop')
    n_columns    : IntProperty(name='n columns', default=1)
    n_rows       : IntProperty(name='n columns', default=1)
    datatype     : StringProperty(name='data type', default='')
    enumerations : CollectionProperty(name="enumerated", type=Enumeration_values)
    

class Class_prop_info(PropertyGroup):
    name          : StringProperty(name='class property name')
    uri           : StringProperty(name='class property uri')
    datatype      : StringProperty(name='class property data type')
    units         : StringProperty(name='class property units')
    propertyset   : StringProperty(name='class property set')
    description   : StringProperty(name='class property description')
    definition    : StringProperty(name='class property definition')

class Documents(PropertyGroup):    
    index          : IntProperty(name="index")
    identification : StringProperty(name="ID")
    location       : StringProperty(name="Location")   
    name           : StringProperty(name="Name") 
    

class Pset_info(PropertyGroup):    
    name          : StringProperty(name='pset name')
    is_a          : StringProperty(name= "is a")
    id_obj        : IntProperty(name="id object")       
    index         : IntProperty(name='index')
    props         : CollectionProperty(name="properties", type=Property_info)
    is_expanded   : BoolProperty(name="Is Expanded", default=False)
    min_x         : FloatProperty(name='min X', default=0)
    max_x         : FloatProperty(name='max X', default=0)
    min_y         : FloatProperty(name='min Y', default=0)
    max_y         : FloatProperty(name='max Y', default=0)
    mult_x        : IntProperty(name='interval X', default=0)
    mult_y        : IntProperty(name='interval Y', default=0)
    interpoled    : BoolProperty(name="Is Interpolated", default=False)
    has_document  : BoolProperty(name='Has documentation', default=False)
    docs_expanded : BoolProperty(name='is expanded', default=True)
    document      : StringProperty(name='document')
    documents     : CollectionProperty(name='documents', type=Documents)
    

class Container(PropertyGroup):
    has_children  : BoolProperty(name="has children")    
    is_hidden     : BoolProperty(name="is Hidded", default=True)
    is_expanded   : BoolProperty(name="Is Expanded", default=True)
    is_selected   : BoolProperty(name="Is Selected")
    index         : IntProperty(name="index")
    id            : IntProperty(name="id")
    parent        : StringProperty(name="parent")
    level         : IntProperty(name="level")
    type          : StringProperty(name="element type")   
    name          : StringProperty(name="name") 
    object_type   : StringProperty(name="object_type")
    is_nested     : BoolProperty(name="is nested", default=False)

class Layer(PropertyGroup):
    id            : IntProperty(name="id")
    name          : StringProperty(name="name")
    description   : StringProperty(name="description")

class OG_Properties(PropertyGroup): 
    
    # O&G Dictionary

    dictionary                 : EnumProperty(items=get_dictionaries, name='',  description='Get Dictionaries')  
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
    
    show_ports               : BoolProperty(name="show ports", default=False)
    show_agg                 : BoolProperty(name="show aggregations / nests", default=False)
    chg_order                : BoolProperty(name="change order", default=False)


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



