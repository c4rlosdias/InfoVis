import bpy

from ...data.tree import draw_tree


class Panel_Catalog(bpy.types.Panel):
    
    bl_label        = "Catalog"
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
            row.prop(props, "li_mapping_reference_sheet", text="Planilha")
            row = box.row()
            row.prop(props, "li_mapping_description", text="Descrição")

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
                row.prop(selected, "column_name", text="Coluna")
                row = detail.row()
                row.prop(selected, "source_type", text="Origem")
                row = detail.row()
                row.prop(selected, "editable", text="Editável")
                row = detail.row()
                row.prop(selected, "notes", text="Notas")

                source_box = detail.box()
                row = source_box.row()
                row.label(text="Source guiado", icon='PROPERTIES')

                if selected.source_type in {'ifc_attribute', 'ifc_property', 'manual'}:
                    row = source_box.row()
                    row.prop(selected, "source_ifc_class", text="Classe")

                if selected.source_type == 'spatial':
                    row = source_box.row()
                    row.prop(selected, "source_level", text="Nível (classe IFC)")

                if selected.source_type == 'aggregation_parent':
                    row = source_box.row()
                    row.prop(selected, "source_level", text="Nível (1=pai imediato, 2=avô, ...)")

                if selected.source_type in {'ifc_attribute', 'ifc_class', 'spatial', 'aggregation_parent'}:
                    row = source_box.row()
                    row.prop(selected, "source_attribute", text="Atributo")

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
                    row.label(text="Escolher do dicionário bSDD", icon='VIEWZOOM')
                    row = picker_box.row()
                    row.prop(selected, "picker_discipline", text="Discipline")
                    row = picker_box.row()
                    row.prop(selected, "picker_object_type", text="Element")
                    row = picker_box.row()
                    row.prop(selected, "picker_pset", text="Property set")
                    row = picker_box.row()
                    row.prop(selected, "picker_property", text="Property")
                    row = picker_box.row()
                    row.operator("catag.li_mapping_pick_property", text="Usar esta propriedade", icon='CHECKMARK')

                if selected.source_type == 'ifc_class':
                    row = source_box.row()
                    row.prop(selected, "source_mapping_table", text="Mapping Table")

                if selected.source_type in {'ifc_quantity', 'computed'}:
                    row = source_box.row()
                    if selected.source_type == 'ifc_quantity':
                        row.prop(selected, "source_quantity_mode", text="Modo")
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
                row.label(text="Campos extras", icon='SETTINGS')

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
                    row.prop(source_item, "key", text="Chave")
                    row = advanced_box.row()
                    row.prop(source_item, "value", text="Valor")

            support_box = box.box()
            row = support_box.row()
            row.label(text="Tabelas de apoio", icon='PRESET')

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
                row.prop(support_table, "table_name", text="Tabela")
                row = detail.row()
                row.prop(support_table, "description", text="Comentário")

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
                    row.prop(support_row, "key", text="Chave")
                    row = detail.row()
                    row.prop(support_row, "value", text="Valor")


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

            draw_tree(
                layout,
                item,
                operators=[
                    {"name": "catag.select_elements", "icon": 'RESTRICT_SELECT_OFF', "att": [("id", item.id)]},
                    {"name": "catag.show_layers", "icon": 'INFO_LARGE', "att": [("id", item.id)]}
                ],
                attributes=[
                    (f'Name: {item.name}', icontype),
                    (f'Qtde: {item.qtde}', icontype),
                    (f'Unit: {item.unit}', icontype)
                ] if item.level != 1 else [(f'{item.name}', icontype)],
                property='types',
                only_children=True
            )


class BIM_UL_li_mapping_columns(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.column_name or "<sem nome>", icon='SPREADSHEET')
            row.label(text=item.source_type)


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
            row.label(text=item.table_name or "<tabela>", icon='PRESET')
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
