import bpy
from bpy.types import PropertyGroup
from bpy.props import *


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
