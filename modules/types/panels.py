import bpy
import bonsai.tool as tool

from ... import auth


class Panel_Types(bpy.types.Panel):
    
    bl_label        = "Types"
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
        element = model.by_id(props.elements_containers[props.active_element_index].id if props.active_element_index < len(props.containers_show) else None)
        print(element)
        if element is not None:
            types = getattr(element, "IsTypedBy", None)
            if types:
                type = types[0].RelatingType
                if type:
                    row.label(text=f"[{type.ElementType}]{type.Name}")
                else:
                    row.label(text="Type: None", icon='ERROR')
            else:
                row.label(text="Type: None", icon='ERROR')


        row = layout.row()
        row.separator()
        row = layout.row()


        


