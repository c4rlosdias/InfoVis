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
    is_hidden   : BoolProperty(name="is hidden", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    index       : IntProperty(name="index")
    parent      : StringProperty(name="parent")
    level       : IntProperty(name="level")
    type        : StringProperty(name="class type")


class Class_prop_info(PropertyGroup):
    name          : StringProperty(name='class property name')
    uri           : StringProperty(name='class property uri')
    datatype      : StringProperty(name='class property data type')
    units         : StringProperty(name='class property units')
    propertyset   : StringProperty(name='class property set')
    description   : StringProperty(name='class property description')
    definition    : StringProperty(name='class property definition')
