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
    "name"        : "Oil&Gas Tools",
    "author"      : "Carlos Dias",
    "description" : "",
    "blender"     : (5, 0, 0),
    "version"     : (0, 1, 1),
    "location"    : "View3D > Panel > O&G Tools",
    "warning"     : "",
    "category"    : "User"
}


import sys
import os
import platform
import subprocess
import bpy
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class

if platform.system() == "Windows":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))
else:
    # On Linux/macOS the bundled libs contain Windows-only binaries (.pyd),
    # so we install the required packages into Blender's Python instead.
    _required = ["matplotlib", "scipy", "tqdm", "rdflib", "kiwisolver", "cycler"]
    _missing = []
    for _pkg in _required:
        try:
            __import__(_pkg)
        except ImportError:
            _missing.append(_pkg)
    if _missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *_missing])

from .operators import *
from .panels import *
from .properties import *
from . import data


classes = [     
    Operator_get_properties,
    Operator_get_classes,
    Operator_contract_tree,
    Operator_expand_tree,
    Operator_decomposition_move,
    Operator_add_properties,
    Operator_clear_properties,
    Operator_get_prop_info,
    Operator_get_class_info,
    Operator_get_class_prop,
    Operator_assign_all,
    Operator_unassign_all,
    Operator_uri,
    Operator_export_ids,
    Operator_decomposition_select_components,
    Operator_decomposition_select_element,
    Operator_catalog_select_type,
    Operator_catalog_select_elements,
    Operator_catalog_show_layers,
    Operator_catalog_select_layer,
    Operator_load_products,
    Operator_props_load,
    Operator_props_expand,
    Operator_docs_expand,
    Operator_props_edit,
    Operator_disconnect,
    Operator_select_object,
    Operator_add_connect,    
    Columns,
    Operator_props_graph,
    Operator_props_invert,
    Operator_document_edit,
    Operator_document_load,
    Operator_document_open,
    Operator_show_table,
    Operator_decomposition_load,
    ErrorMessage,    
    Panel_Connect, 
    Panel_Decompositions,  
    Panel_Connect_Elements,
    Panel_Catalog, 
    Panel_Properties,
    Panel_Settings,
    Panel_Info,
    BIM_UL_tree,
    BIM_UL_ifc_properties,
    BIM_UL_classes,
    BIM_UL_class_prop,
    BIM_UL_products,
    BIM_UL_property_class,
    BIM_UL_decomposition,
    BIM_UL_layers,
    Ifc_properties,
    Enumeration_values,
    Documents,  
    Class_info,
    Class_type,
    Class_prop_info,
    Layer,
    Property_info,
    Pset_info,
    Container,
    OG_Properties,
]
owner = object()
def register():
    for c in classes:
        register_class(c)
    Scene.og_props = PointerProperty(type=OG_Properties)
    bpy.types.WindowManager.add_connect_object_a = PointerProperty(type=bpy.types.Object, name="Object A")
    bpy.types.WindowManager.add_connect_object_b = PointerProperty(type=bpy.types.Object, name="Object B")
    bpy.types.WindowManager.add_connect_object_c = PointerProperty(type=bpy.types.Object, name="Object C")
    bpy.msgbus.subscribe_rna( 
        key=(bpy.types.LayerObjects, "active"),
        owner=owner,
        args=(),
        notify=data.call_back 
    )
    #bpy.app.handlers.depsgraph_update_post.append(data.on_active_object_change)



def unregister():
    #bpy.app.handlers.depsgraph_update_post.remove(data.on_active_object_change)
    bpy.msgbus.clear_by_owner(owner)
    if hasattr(bpy.types.WindowManager, "add_connect_object_c"):
        del bpy.types.WindowManager.add_connect_object_c
    if hasattr(bpy.types.WindowManager, "add_connect_object_b"):
        del bpy.types.WindowManager.add_connect_object_b
    if hasattr(bpy.types.WindowManager, "add_connect_object_a"):
        del bpy.types.WindowManager.add_connect_object_a
    if hasattr(Scene, "og_props"):
        del Scene.og_props
    for c in classes:
        try:
            unregister_class(c)
        except RuntimeError:
            pass

if __name__ == "__main__":
    register()

