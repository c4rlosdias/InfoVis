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
    "blender"     : (4, 3, 0),
    "version"     : (0, 0, 1),
    "location"    : "View3D > Panel > Oil&Gas Tools",
    "warning"     : "",
    "category"    : "User"
}


import sys
import os
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class



#if sys.modules.get("bpy", None):
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))

from .operators import *
from .panels import *
from .properties import *

classes = [     
    Operator_get_properties,
    Operator_get_classes,
    Operator_load_decomposition,
    Operator_contract_classes,
    Operator_contract_products,
    Operator_expand_classes,
    Operator_expand_products,
    Operator_contract_decomposition,
    Operator_expand_decomposition,
    Operator_add_properties,
    Operator_clear_properties,
    Operator_get_prop_info,
    Operator_get_class_info,
    Operator_get_class_prop,
    Operator_assign_all,
    Operator_unassign_all,
    Operator_uri,
    Operator_export_ids,
    Operator_element_selection,
    Operator_catalog_insert_type,
    Operator_load_products,
    Operator_props_load,
    Operator_props_expand,
    Operator_props_edit,
    Columns,
    Operator_props_graph,
    Operator_props_invert,
    Operator_document_edit,
    Operator_document_load,
    Operator_show_table,
    Panel_Connect,
    Panel_Import_Properties,
    Panel_Import_Classes,
    Panel_Export_Properties, 
    Panel_Decompositions,  
    Panel_Catalog, 
    Panel_Properties,
    BIM_UL_ifc_properties,
    BIM_UL_classes,
    BIM_UL_class_prop,
    BIM_UL_products,
    BIM_UL_property_class,
    BIM_UL_decomposition,
    Ifc_properties,
    Enumeration_values,
    Class_info,
    Class_prop_info,
    Property_info,
    Pset_info,
    Container,    
    MyProperties,
]

def register():
    for c in classes:
        register_class(c)
    Scene.my_props = PointerProperty(type=MyProperties)


def unregister():
    del Scene.my_props
    for c in classes:
        unregister_class(c)

if __name__ == "__main__":
    register()

