import bpy
from bpy.types import PropertyGroup
from bpy.props import *


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
