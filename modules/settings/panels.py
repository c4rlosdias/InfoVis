import bpy


class Panel_Info(bpy.types.Panel):
    
    bl_label        = "Info"
    bl_idname       = "VIEW3D_PT_og_info"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Info"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='INFO_LARGE')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="InfoVis - alpha - V 0.1.2", icon='MOD_LINEART')
        row = layout.row()
        row.label(text="26.04.28")
        layout.separator()
        layout = self.layout
        props = context.scene.og_props
        row = layout.row()
        row.label(text='Choose a bSDD dictionary:')
        row = layout.row()
        row.prop(props, 'dictionary')
