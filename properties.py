import bpy
from bpy.types import PropertyGroup
from bpy.props import *
import bonsai.tool as tool
import requests
from .data import bSDD

def get_dictionaries(self, context):                
    if not bSDD.is_loaded:
        bSDD.load_dictionaries()
    return bSDD.data_dic
        
def active_prop_changed(self, context):
    self.info_prop_loaded = False
    self.class_info.clear()

def active_class_changed(self, context):
    #self.classes_shown.clear()
    self.classes_loaded = False

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
    level_index : IntProperty(name="level index")
    type        : StringProperty(name="class type")

class Container(PropertyGroup):
    has_children: BoolProperty(name="has children")    
    is_hidden   : BoolProperty(name="is Hidded", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    is_selected : BoolProperty(name="Is Selected")
    index       : IntProperty(name="index")
    id          : IntProperty(name="id")
    parent      : StringProperty(name="parent")
    level       : IntProperty(name="level")
    type        : StringProperty(name="element type")   
    name        : StringProperty(name="name") 


class MyProperties(PropertyGroup): 
    
    active_info_prop_index   : IntProperty(name='object index', default=0)
    active_property_index    : IntProperty(name='property index', default=0, update=active_prop_changed)
    active_class_index       : IntProperty(name='class index', default=0, update=active_class_changed)
    active_element_index     : IntProperty(name='element index', default=0)
    add_prop_clicked         : BoolProperty(name="add property clicked", default=False)
    class_info               : CollectionProperty(name='info class', type=Class_info)
    classes                  : CollectionProperty(name='classes', type=Class_info) 
    classes_shown            : CollectionProperty(name='classes', type=Class_info) 
    elements_containers      : CollectionProperty(name='elements containers', type=Container) 
    containers_show          : CollectionProperty(name='containers show', type=Container) 
    class_description        : StringProperty(name='class description')
    class_definition         : StringProperty(name='class definition')
    class_version            : StringProperty(name='class version date') 
    class_type               : StringProperty(name='class type') 
    class_ifctype            : StringProperty(name='ifc class') 
    classes_loaded           : BoolProperty(name='classes loaded', default=False)   
    dictionaries_loaded      : BoolProperty(name='Dictionaries loaded')
    dictionary               : EnumProperty(items=get_dictionaries, name='',  description='Get Dictionaries')    
    prop_datatype            : StringProperty(name='property data type')
    prop_units               : StringProperty(name='property units')
    prop_type                : StringProperty(name='property type')
    prop_description         : StringProperty(name='property description')
    prop_definition          : StringProperty(name='property definition')
    ifc_prop                 : CollectionProperty(name='properties', type=Ifc_properties) 
    info_prop_loaded         : BoolProperty(name='info prop loaded', default=False)
    info_class_loaded        : BoolProperty(name='info class loaded', default=False)
    ids_file                 : StringProperty(name='IDS file')
    
    # Catalog

    products                 : EnumProperty(items=load_products, name='',  description='Select Product Type') 
    products_loaded          : BoolProperty(name="products loaded", default=False)


