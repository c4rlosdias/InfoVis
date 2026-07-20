import bpy
from bpy.types import PropertyGroup
from bpy.props import *


class Container(PropertyGroup):
    has_children  : BoolProperty(name="has children")    
    is_hidden     : BoolProperty(name="is hidden", default=True)
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
