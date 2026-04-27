import bpy
import bonsai.tool as tool

from ... import auth
from ..catalog.operators import Operator_catalog_show_layers, Operator_catalog_select_elements


class Panel_Types(bpy.types.Panel):
    
    bl_label        = "Constructive Type"
    bl_idname       = "VIEW3D_PT_types"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G-Occurrence"
    bl_options      = {"DEFAULT_CLOSED"}
    
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GREASEPENCIL')    

    def draw(self, context):
        model = tool.Ifc.get()
        layout = self.layout        
        props = context.scene.og_props
        row = layout.row()
        obj = context.active_object
        if obj is not None and obj.select_get():
            element = model.by_id(obj.BIMObjectProperties.ifc_definition_id)
            types = getattr(element, "IsTypedBy", None)
            if types:
                type = types[0].RelatingType
                if type:
                    row.label(text=f"{type.ElementType}")
                    row.operator("catag.select_elements", text="", icon='RESTRICT_SELECT_OFF').id = type.id()
                    row.operator("catag.show_layers", text="", icon='INFO_LARGE').id = type.id()
                    row = layout.row()
                    row.label(text=f" Name           : {type.Name}", icon='DOT')
                    row = layout.row()
                    row.label(text=f" Description :  {type.Description}", icon = 'DOT')

                else:
                    row.label(text="Type: None", icon='ERROR')
            else:
                row.label(text="Type: None", icon='ERROR')


        row = layout.row()
        row.separator()
        row = layout.row()


        


