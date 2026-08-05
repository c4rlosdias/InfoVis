import bpy


_LI_SOURCE_LABELS = {
    'ifc_attribute': 'Element Information',
    'ifc_property': 'Technical Property',
    'material': 'Material',
    'ifc_quantity': 'Quantity',
    'ifc_class': 'Element Class',
    'spatial': 'Location',
    'aggregation_parent': 'Assembly Parent',
    'computed': 'Calculated Value',
    'manual': 'Custom Property',
    'not_applicable': 'Not Applicable',
}


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

    def _draw_property_picker(self, layout, selected):
        picker = layout.box()
        picker.label(text="Choose from the project dictionary", icon='VIEWZOOM')
        picker.prop(selected, "picker_discipline", text="Discipline")
        picker.prop(selected, "picker_object_type", text="Element")
        picker.prop(selected, "picker_pset", text="Property group")
        picker.prop(selected, "picker_property", text="Information")
        picker.operator("catag.li_mapping_pick_property", text="Use selected information", icon='CHECKMARK')

    def _draw_simple_source(self, layout, selected):
        source_box = layout.box()
        source_box.label(text="Where does this column come from?", icon='PROPERTIES')

        if selected.source_type == 'material':
            source_box.prop(selected, "source_material_field", text="Material information")
            if selected.source_material_field == 'property':
                source_box.prop(selected, "source_pset", text="Property group")
                source_box.prop(selected, "source_property", text="Property")
        elif selected.source_type == 'ifc_attribute':
            source_box.prop(selected, "source_attribute", text="Element field")
        elif selected.source_type in {'ifc_property', 'manual'}:
            self._draw_property_picker(source_box, selected)
        elif selected.source_type == 'ifc_quantity':
            source_box.prop(selected, "source_quantity_mode", text="Quantity method")
        elif selected.source_type == 'aggregation_parent':
            source_box.prop(selected, "source_level", text="Parent level")
        elif selected.source_type == 'spatial':
            source_box.prop(selected, "source_level", text="Location type")
        elif selected.source_type in {'ifc_class', 'computed'}:
            source_box.label(text="This source is ready. Open Advanced settings to change its rule.")
        else:
            source_box.label(text="This column will be left empty in the export.")

    def _draw_extra_fields(self, layout, selected):
        extra = layout.box()
        extra.label(text="Extra source fields", icon='SETTINGS')
        extra.template_list(
            "BIM_UL_li_mapping_source_items", "", selected, "source_items",
            selected, "active_source_item_index", rows=4,
        )
        row = extra.row(align=True)
        row.operator("catag.add_li_mapping_source_item", text="Add Field", icon='ADD')
        row.operator("catag.remove_li_mapping_source_item", text="Remove Field", icon='REMOVE')
        source_index = selected.active_source_item_index
        if 0 <= source_index < len(selected.source_items):
            source_item = selected.source_items[source_index]
            extra.prop(source_item, "key", text="Key")
            extra.prop(source_item, "value", text="Value")

    def _draw_support_tables(self, layout, props):
        support_box = layout.box()
        support_box.label(text="Support Tables", icon='PRESET')
        support_box.template_list(
            "BIM_UL_li_support_tables", "", props, "li_support_tables",
            props, "active_li_support_table_index", rows=4,
        )
        support_index = props.active_li_support_table_index
        if not (0 <= support_index < len(props.li_support_tables)):
            return
        support_table = props.li_support_tables[support_index]
        detail = support_box.box()
        detail.prop(support_table, "table_name", text="Table")
        detail.prop(support_table, "description", text="Comment")
        detail.template_list(
            "BIM_UL_li_support_table_rows", "", support_table, "rows",
            support_table, "active_row_index", rows=5,
        )
        row = detail.row(align=True)
        row.operator("catag.add_li_support_table_row", text="Add Row", icon='ADD')
        row.operator("catag.remove_li_support_table_row", text="Remove Row", icon='REMOVE')
        row_index = support_table.active_row_index
        if 0 <= row_index < len(support_table.rows):
            support_row = support_table.rows[row_index]
            detail.prop(support_row, "key", text="Key")
            detail.prop(support_row, "value", text="Value")

    def draw(self, context):
        props = context.scene.og_props
        layout = self.layout

        action_box = layout.box()
        action_box.label(text="Generate the Item List from the current IFC model")
        action_box.operator("catag.export_li", text="Export Item List", icon='EXPORT')

        if not props.li_mapping_loaded:
            action_box.operator(
                "catag.load_li_mapping",
                text="Configure Columns",
                icon='SETTINGS',
            )
            action_box.label(text="The saved profile will be used when exporting.", icon='INFO')
            return

        row = action_box.row(align=True)
        row.operator("catag.save_li_mapping", text="Apply Changes", icon='FILE_TICK')
        row.operator("catag.load_li_mapping", text="Reload Saved", icon='FILE_REFRESH')

        columns_box = layout.box()
        columns_box.label(text="Item List Columns", icon='SPREADSHEET')
        columns_box.template_list(
            "BIM_UL_li_mapping_columns", "", props, "li_mapping_columns",
            props, "active_li_mapping_index", rows=8,
        )
        row = columns_box.row(align=True)
        row.operator("catag.add_li_mapping_column", text="Add Column", icon='ADD')
        material = row.operator("catag.add_li_mapping_column", text="Add Material", icon='MATERIAL')
        material.source_type = 'material'
        row.operator("catag.remove_li_mapping_column", text="Remove", icon='REMOVE')

        active_index = props.active_li_mapping_index
        selected = props.li_mapping_columns[active_index] if 0 <= active_index < len(props.li_mapping_columns) else None
        if selected is not None:
            detail = layout.box()
            detail.label(text="Selected Column")
            detail.prop(selected, "column_name", text="Column name")
            detail.prop(selected, "source_type", text="Information source")
            self._draw_simple_source(detail, selected)

        advanced = layout.box()
        advanced.prop(props, "li_mapping_advanced", text="Advanced settings", icon='SETTINGS')
        if not props.li_mapping_advanced:
            return

        advanced.prop(props, "li_mapping_reference_sheet", text="Reference Sheet")
        advanced.prop(props, "li_mapping_description", text="Description")
        advanced.prop(props, "li_mapping_schema_version", text="Schema")
        advanced.label(text="resources/li_mapping.json", icon='FILE')

        if selected is not None:
            technical = advanced.box()
            technical.label(text="Technical source settings")
            technical.prop(selected, "source_ifc_class", text="IFC Class")
            technical.prop(selected, "source_pset", text="Pset")
            technical.prop(selected, "source_property", text="Property")
            technical.prop(selected, "source_attribute", text="Attribute")
            technical.prop(selected, "source_fallback_attribute", text="Fallback")
            technical.prop(selected, "source_mapping_table", text="Mapping Table")
            technical.prop(selected, "source_selected_by", text="Selected By")
            technical.prop(selected, "source_template_table", text="Template Table")
            technical.prop(selected, "source_derived_from", text="Derived From")
            technical.prop(selected, "source_method", text="Method")
            technical.prop(selected, "source_format", text="Format")
            technical.prop(selected, "source_allowed_values", text="Allowed Values")
            technical.prop(selected, "notes", text="Notes")
            self._draw_extra_fields(advanced, selected)

        self._draw_support_tables(advanced, props)


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
            label_row.label(text=_LI_SOURCE_LABELS.get(item.source_type, item.source_type))

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
