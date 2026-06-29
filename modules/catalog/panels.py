import bpy


def _draw_catalog_type_tree(layout, item, icon):
    if item.is_hidden:
        return

    row = layout.row(align=True)
    for _ in range(0, item.level - 1):
        row.label(text="", icon="BLANK1")

    if item.has_children:
        if item.is_expanded:
            op = row.operator("element.contract_tree", text="", emboss=False, icon="DISCLOSURE_TRI_DOWN")
        else:
            op = row.operator("element.expand_tree", text="", emboss=False, icon="DISCLOSURE_TRI_RIGHT")
        op.index = item.index
        op.property = 'types'
    else:
        row.label(text="", icon="BLANK1")

    if item.level == 1:
        row.label(text=item.name, icon=icon)
    else:
        split = row.split(factor=0.68, align=True)
        split.label(text=f'Name: {item.name}', icon=icon)
        split = split.split(factor=0.38, align=True)
        split.label(text=f'Quantity: {item.qtde:g}', icon=icon)
        split.label(text=f'Unit: {item.unit}', icon=icon)

    if not item.has_children:
        op = row.operator("catag.select_elements", text="", icon='RESTRICT_SELECT_OFF')
        op.id = item.id
        op = row.operator("catag.show_layers", text="", icon='INFO_LARGE')
        op.id = item.id


class Panel_Catalog(bpy.types.Panel):
    
    bl_label        = "Products Catalog"
    bl_idname       = "VIEW3D_PT_og_catalog"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Catalog"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GROUP_VCOL')

    def draw(self, context):   
        props = context.scene.og_props 
        layout = self.layout       
        row = layout.row()     

        row.operator("catag.load_products", text="Load type products")   

        if len(props.types) > 0:
            row = layout.row()
            row.label(text="Classes Information:", icon='INFO')

            self.layout.template_list(
                "BIM_UL_products",
                "",
                props,
                "types_show",
                props,
                "active_type_index",
                rows=10
            )

            row = layout.row(align=True)
            row.operator("catag.export_qtds", text="Export Quantities")
        
        if len(props.layers) > 0:            
            row = layout.row()
            row.label(text="Layers:", icon='INFO')

            self.layout.template_list(
                "BIM_UL_layers",
                "",
                props,
                "layers",
                props,
                "active_layer_index",
                rows=10
            )


class Panel_LI_Mapping(bpy.types.Panel):

    bl_label        = "LI Mapping"
    bl_idname       = "VIEW3D_PT_og_li_mapping"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Catalog"
    bl_options      = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SPREADSHEET')

    def draw(self, context):
        props = context.scene.og_props
        layout = self.layout
        box = layout.box()

        row = box.row(align=True)
        row.operator("catag.load_li_mapping", text="Load", icon='FILE_REFRESH')
        row.operator("catag.save_li_mapping", text="Save", icon='FILE_TICK')
        row = box.row(align=True)
        row.operator("catag.export_li", text="Export LI", icon='EXPORT')

        if props.li_mapping_loaded:
            row = box.row()
            row.prop(props, "li_mapping_schema_version", text="Schema")
            row = box.row()
            row.prop(props, "li_mapping_reference_sheet", text="Reference Sheet")
            row = box.row()
            row.prop(props, "li_mapping_description", text="Description")

            row = box.row()
            row.label(text="resources/li_mapping.json", icon='FILE')

            box.template_list(
                "BIM_UL_li_mapping_columns",
                "",
                props,
                "li_mapping_columns",
                props,
                "active_li_mapping_index",
                rows=8,
            )

            row = box.row(align=True)
            row.operator("catag.add_li_mapping_column", text="Add Column", icon='ADD')
            row.operator("catag.remove_li_mapping_column", text="Remove Column", icon='REMOVE')

            active_index = props.active_li_mapping_index
            if 0 <= active_index < len(props.li_mapping_columns):
                selected = props.li_mapping_columns[active_index]

                detail = box.box()
                row = detail.row()
                row.prop(selected, "column_name", text="Column")
                row = detail.row()
                row.prop(selected, "source_type", text="Source")
                row = detail.row()
                row.prop(selected, "notes", text="Notes")

                source_box = detail.box()
                row = source_box.row()
                row.label(text="Guided Source", icon='PROPERTIES')

                if selected.source_type in {'ifc_attribute', 'ifc_property', 'manual'}:
                    row = source_box.row()
                    row.prop(selected, "source_ifc_class", text="Class")

                if selected.source_type == 'spatial':
                    row = source_box.row()
                    row.prop(selected, "source_level", text="Level (IFC class)")

                if selected.source_type == 'aggregation_parent':
                    row = source_box.row()
                    row.prop(selected, "source_level", text="Level (1=direct parent, 2=grandparent, ...)")

                if selected.source_type in {'ifc_attribute', 'ifc_class', 'spatial', 'aggregation_parent'}:
                    row = source_box.row()
                    row.prop(selected, "source_attribute", text="Attribute")

                if selected.source_type in {'ifc_attribute', 'aggregation_parent'}:
                    row = source_box.row()
                    row.prop(selected, "source_fallback_attribute", text="Fallback")

                if selected.source_type in {'ifc_property', 'manual'}:
                    row = source_box.row()
                    row.prop(selected, "source_pset", text="Pset")
                    row = source_box.row()
                    row.prop(selected, "source_property", text="Property")
                    row = source_box.row()
                    row.prop(selected, "source_allowed_values", text="Allowed Values")

                    picker_box = source_box.box()
                    row = picker_box.row()
                    row.label(text="Pick from bSDD dictionary", icon='VIEWZOOM')
                    row = picker_box.row()
                    row.prop(selected, "picker_discipline", text="Discipline")
                    row = picker_box.row()
                    row.prop(selected, "picker_object_type", text="Element")
                    row = picker_box.row()
                    row.prop(selected, "picker_pset", text="Property set")
                    row = picker_box.row()
                    row.prop(selected, "picker_property", text="Property")
                    row = picker_box.row()
                    row.operator("catag.li_mapping_pick_property", text="Use this property", icon='CHECKMARK')

                if selected.source_type == 'ifc_class':
                    row = source_box.row()
                    row.prop(selected, "source_mapping_table", text="Mapping Table")

                if selected.source_type in {'ifc_quantity', 'computed'}:
                    row = source_box.row()
                    if selected.source_type == 'ifc_quantity':
                        row.prop(selected, "source_quantity_mode", text="Mode")
                    else:
                        row.prop(selected, "source_selected_by", text="Selected By")

                if selected.source_type == 'ifc_quantity' and selected.source_quantity_mode == 'mapping':
                    row = source_box.row()
                    row.prop(selected, "source_mapping_table", text="Mapping Table")
                    row = source_box.row()
                    row.prop(selected, "source_selected_by", text="Selected By")

                if selected.source_type == 'computed':
                    row = source_box.row()
                    row.prop(selected, "source_template_table", text="Template Table")
                    row = source_box.row()
                    row.prop(selected, "source_derived_from", text="Derived From")
                    row = source_box.row()
                    row.prop(selected, "source_method", text="Method")

                if selected.source_type in {'ifc_attribute', 'computed'}:
                    row = source_box.row()
                    row.prop(selected, "source_format", text="Format")

                advanced_box = detail.box()
                row = advanced_box.row()
                row.label(text="Extra Fields", icon='SETTINGS')

                advanced_box.template_list(
                    "BIM_UL_li_mapping_source_items",
                    "",
                    selected,
                    "source_items",
                    selected,
                    "active_source_item_index",
                    rows=5,
                )

                row = advanced_box.row(align=True)
                row.operator("catag.add_li_mapping_source_item", text="Add Field", icon='ADD')
                row.operator("catag.remove_li_mapping_source_item", text="Remove Field", icon='REMOVE')

                source_index = selected.active_source_item_index
                if 0 <= source_index < len(selected.source_items):
                    source_item = selected.source_items[source_index]
                    row = advanced_box.row()
                    row.prop(source_item, "key", text="Key")
                    row = advanced_box.row()
                    row.prop(source_item, "value", text="Value")

            support_box = box.box()
            row = support_box.row()
            row.label(text="Support Tables", icon='PRESET')

            support_box.template_list(
                "BIM_UL_li_support_tables",
                "",
                props,
                "li_support_tables",
                props,
                "active_li_support_table_index",
                rows=4,
            )

            support_index = props.active_li_support_table_index
            if 0 <= support_index < len(props.li_support_tables):
                support_table = props.li_support_tables[support_index]
                detail = support_box.box()
                row = detail.row()
                row.prop(support_table, "table_name", text="Table")
                row = detail.row()
                row.prop(support_table, "description", text="Comment")

                detail.template_list(
                    "BIM_UL_li_support_table_rows",
                    "",
                    support_table,
                    "rows",
                    support_table,
                    "active_row_index",
                    rows=6,
                )

                row = detail.row(align=True)
                row.operator("catag.add_li_support_table_row", text="Add Row", icon='ADD')
                row.operator("catag.remove_li_support_table_row", text="Remove Row", icon='REMOVE')

                row_index = support_table.active_row_index
                if 0 <= row_index < len(support_table.rows):
                    support_row = support_table.rows[row_index]
                    row = detail.row()
                    row.prop(support_row, "key", text="Key")
                    row = detail.row()
                    row.prop(support_row, "value", text="Value")


class BIM_UL_products(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            icons = {
                'Pipe Fitting': 'MOD_SIMPLEDEFORM',
                'Pipe Segment': 'IPO_EASE_IN_OUT'
            }
            if item.name in icons:
                icontype = icons[item.name]
            else:
                icontype = 'NONE'

            _draw_catalog_type_tree(layout, item, icontype)


class BIM_UL_li_mapping_columns(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index=0, flt_flag=0):
        if item:
            row = layout.row(align=True)
            label_row = row.row(align=True)
            label_row.label(text=item.column_name or "<sem nome>", icon='SPREADSHEET')
            label_row.label(text=item.source_type)

            controls = row.row(align=True)
            up_row = controls.row(align=True)
            up_row.enabled = index > 0
            up = up_row.operator("catag.move_li_mapping_column", text="", icon='TRIA_UP', emboss=False)
            up.index = index
            up.direction = 'UP'
            down_row = controls.row(align=True)
            down_row.enabled = index < len(data.li_mapping_columns) - 1
            down = down_row.operator("catag.move_li_mapping_column", text="", icon='TRIA_DOWN', emboss=False)
            down.index = index
            down.direction = 'DOWN'


class BIM_UL_li_mapping_source_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.key or "<chave>", icon='DOT')
            row.label(text=item.value or "")


class BIM_UL_li_support_tables(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.table_name or "<table>", icon='PRESET')
            row.label(text=f"{len(item.rows)} itens")


class BIM_UL_li_support_table_rows(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.key or "<chave>", icon='DOT')
            row.label(text=item.value or "")


class BIM_UL_layers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.name, icon='LAYER_USED')
            row.operator("catag.select_layer", text="", icon='OBJECT_DATA').id = item.id
