# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name"        : "InfoVis - alpha - v1.0.0",
    "author"      : "Carlos Dias",
    "description" : "",
    "blender"     : (5, 0, 0),
    "version"     : (1, 0, 0),
    "location"    : "View3D > Panel > InfoVis",
    "warning"     : "",
    "category"    : "User"
}


import bpy
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class

from .modules import get_classes
from .modules.og_properties import OG_Properties
from .modules.common.operators import register_ifc_label_overlay, unregister_ifc_label_overlay
from . import data
from .data import tree as _data_tree


# ----- Add-on Preferences -----

class OilGasAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    cde_url: bpy.props.StringProperty(
        name="CDE URL",
        description="Base URL for the CDE API",
        default="http://localhost:8000",
    )
    cde_token: bpy.props.StringProperty(
        name="CDE Token",
        description="Authentication token for the CDE",
        default="",
        subtype='PASSWORD',
    )
    debug_mode: bpy.props.BoolProperty(
        name="Debug Mode",
        description="Enable debug mode",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="CDE Integration", icon='URL')
        box.prop(self, "cde_url")
        box.prop(self, "cde_token")
        box.prop(self, "debug_mode")


classes = [
    OilGasAddonPreferences,
] + get_classes()
owner = object()

def _subscribe_msgbus():
    bpy.msgbus.clear_by_owner(owner)
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.LayerObjects, "active"),
        owner=owner,
        args=(),
        notify=_data_tree.call_back
    )

@bpy.app.handlers.persistent
def _on_load_post(*args):
    _subscribe_msgbus()

def register():
    for c in classes:
        register_class(c)
    Scene.og_props = PointerProperty(type=OG_Properties)
    _subscribe_msgbus()
    bpy.app.handlers.load_post.append(_on_load_post)
    register_ifc_label_overlay()


def unregister():
    if _on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_load_post)
    bpy.msgbus.clear_by_owner(owner)
    unregister_ifc_label_overlay()
    if hasattr(Scene, "og_props"):
        del Scene.og_props
    for c in classes:
        try:
            unregister_class(c)
        except RuntimeError:
            pass

if __name__ == "__main__":
    register()

