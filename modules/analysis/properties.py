import bpy
from bpy.types import PropertyGroup
from bpy.props import FloatVectorProperty, StringProperty


class AnalysisLegendItem(PropertyGroup):
    label : StringProperty(name="Label")
    color : FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
    )
