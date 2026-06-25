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


class BIM_UL_decomposition_views(bpy.types.UIList):
    bl_idname = "BIM_UL_decomposition_views"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            split = row.split(factor=0.48, align=True)
            split.label(text=item.label or item.id, icon='NODETREE')
            split.label(text=item.root_ifc_class or "No root class", icon='DOT')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='NODETREE')


class BIM_UL_decomposition_view_relations(bpy.types.UIList):
    bl_idname = "BIM_UL_decomposition_view_relations"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            split = row.split(factor=0.34, align=True)
            split.prop(item, "element_attribute", text="", emboss=True, icon='DOT')
            sub = split.split(factor=0.52, align=True)
            sub.prop(item, "relationship_type", text="", emboss=True, icon='PROPERTIES')
            sub.prop(item, "relationship_attribute", text="", emboss=True, icon='DOT')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='PROPERTIES')


def _active_decomposition_view(props):
    index = props.active_decomposition_view_index
    if 0 <= index < len(props.decomposition_views):
        return props.decomposition_views[index]
    return None


def _active_decomposition_relation(props, view):
    if view is None:
        return None
    index = props.active_decomposition_relation_index
    if 0 <= index < len(view.relations):
        return view.relations[index]
    return None


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

        layout.separator()
        row = layout.row()
        row.label(text="Decomposition views:", icon='NODETREE')
        row = layout.row(align=True)
        row.operator("settings.load_decomposition_views", text="Load")
        row.operator("settings.save_decomposition_views", text="Save")
        row.operator("settings.reset_decomposition_views", text="Defaults")

        if not props.decomposition_views_loaded:
            row = layout.row()
            row.label(text="Load decomposition_view.json to edit the views.", icon='INFO')

        row = layout.row()
        col_list = row.column()
        col_list.template_list(
            "BIM_UL_decomposition_views", "",
            props, "decomposition_views",
            props, "active_decomposition_view_index",
            rows=3,
        )
        col_btn = row.column(align=True)
        col_btn.operator("settings.add_decomposition_view", icon='ADD', text="")
        col_btn.operator("settings.duplicate_decomposition_view", text="Dup")
        col_btn.operator("settings.remove_decomposition_view", icon='REMOVE', text="")

        active_view = _active_decomposition_view(props)
        if active_view:
            box = layout.box()
            box.prop(active_view, "id")
            box.prop(active_view, "label")
            box.prop(active_view, "root_ifc_class")

            box.separator()
            row = box.row()
            row.label(text="IFC relation attributes:", icon='PROPERTIES')
            row = box.row()
            rel_list = row.column()
            rel_list.template_list(
                "BIM_UL_decomposition_view_relations", "",
                active_view, "relations",
                props, "active_decomposition_relation_index",
                rows=4,
            )
            rel_btn = row.column(align=True)
            rel_btn.operator_menu_enum("settings.add_decomposition_relation", "preset", icon='ADD', text="")
            rel_btn.operator("settings.remove_decomposition_relation", icon='REMOVE', text="")

            active_relation = _active_decomposition_relation(props, active_view)
            if active_relation:
                col = box.column(align=True)
                col.prop(active_relation, "element_attribute")
                col.prop(active_relation, "relationship_type")
                col.prop(active_relation, "relationship_attribute")
