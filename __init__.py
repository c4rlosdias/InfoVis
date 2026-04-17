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
    "version"     : (0, 1, 2),
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

from .modules import get_classes
from .modules.og_properties import OG_Properties
from . import data
from .data import tree as _data_tree
from . import auth


# ----- Operadores de autenticação -----

class OG_OT_Login(bpy.types.Operator):
    bl_idname = "og.login"
    bl_label = "Login"
    bl_description = "Autenticar com a senha cadastrada"

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        pw = prefs.auth_password
        if auth.login(pw):
            prefs.auth_password = ""
            self.report({'INFO'}, "Autenticado com sucesso")
        else:
            prefs.auth_password = ""
            self.report({'ERROR'}, "Senha incorreta")
        return {'FINISHED'}


class OG_OT_Logout(bpy.types.Operator):
    bl_idname = "og.logout"
    bl_label = "Logout"
    bl_description = "Encerrar sessão autenticada"

    def execute(self, context):
        auth.logout()
        self.report({'INFO'}, "Sessão encerrada")
        return {'FINISHED'}


# ----- Preferências do Addon -----

class OilGasAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    cde_url: bpy.props.StringProperty(
        name="CDE URL",
        description="URL base da API do CDE",
        default="http://localhost:8000",
    )
    cde_token: bpy.props.StringProperty(
        name="CDE Token",
        description="Token de autenticação para o CDE",
        default="",
        subtype='PASSWORD',
    )
    debug_mode: bpy.props.BoolProperty(
        name="Debug Mode",
        description="Ativar modo de depuração",
        default=False,
    )
    auth_password: bpy.props.StringProperty(
        name="Senha",
        description="Senha para autenticação no addon",
        default="",
        subtype='PASSWORD',
    )

    def draw(self, context):
        layout = self.layout

        # --- Autenticação ---
        box = layout.box()
        box.label(text="Autenticação para status de editor", icon='LOCKED')

        if auth.is_authenticated():
            box.label(text="Status de editor: Autenticado", icon='CHECKMARK')
            box.operator("og.logout", icon='PANEL_CLOSE')
        else:
            box.label(text="Status de editor: Não autenticado", icon='ERROR')
            box.prop(self, "auth_password")
            box.operator("og.login", icon='UNLOCKED')

        # # --- Outras configurações ---
        # box3 = layout.box()
        # box3.label(text="Configurações", icon='PREFERENCES')
        # box3.prop(self, "cde_url")
        # box3.prop(self, "cde_token")
        # box3.prop(self, "debug_mode")


classes = [
    OilGasAddonPreferences,
    OG_OT_Login,
    OG_OT_Logout,
] + get_classes()
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
        notify=_data_tree.call_back 
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

