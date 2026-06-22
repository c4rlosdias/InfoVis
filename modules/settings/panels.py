import bpy


class BIM_UL_ifc_label_attrs(bpy.types.UIList):
    bl_idname = "BIM_UL_ifc_label_attrs"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            split = row.split(factor=0.58, align=True)
            split.prop(item, "attr_name", text="", emboss=True, icon='DOT')
            split.prop(item, "display_name", text="", emboss=True, icon='FONT_DATA')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='DOT')


class Panel_Info(bpy.types.Panel):
    
    bl_label        = "Settings"
    bl_idname       = "VIEW3D_PT_og_info"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Settings"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='INFO_LARGE')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="InfoVis - alpha - V 0.1.2", icon='MOD_LINEART')
        row = layout.row()
        row.label(text="26.05.14")
        layout.separator()
        layout = self.layout
        props = context.scene.og_props
        row = layout.row()
        row.label(text="Show IFC labels")
        layout.separator()
        row = layout.row()
        icon = 'HIDE_OFF' if props.show_ifc_label else 'HIDE_ON'
        row.prop(props, 'show_ifc_label', icon=icon, toggle=True)

        layout.separator()
        row = layout.row()
        row.label(text="Fields to display:", icon='LINENUMBERS_ON')
        row = layout.row(align=True)
        split = row.split(factor=0.58, align=True)
        split.label(text="Field")
        split.label(text="Display text")
        row = layout.row()
        col_list = row.column()
        col_list.template_list(
            "BIM_UL_ifc_label_attrs", "",
            props, "ifc_label_attributes",
            props, "active_ifc_label_attr_index",
            rows=3,
        )
        col_btn = row.column(align=True)
        col_btn.operator("settings.add_ifc_label_attr", icon='ADD', text="")
        col_btn.operator("settings.add_ifc_label_property", icon='PROPERTIES', text="")
        col_btn.operator("settings.remove_ifc_label_attr", icon='REMOVE', text="")

        layout.separator()
        row = layout.row(align=True)
        row.label(text="Label offset (px):", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(props, 'label_offset_x')
        row.prop(props, 'label_offset_y')
