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
        

class BIM_UL_products(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            icons = {
                'Pipe Fitting' : 'MOD_SIMPLEDEFORM',
                'Pipe Segment' : 'IPO_EASE_IN_OUT'
            }
            if item.name in icons:
                icontype = icons[item.name]
            else:
                icontype = 'NONE'

            draw_tree(layout, item,
                operators = [                    
                    {"name": "catag.select_elements", "icon": 'RESTRICT_SELECT_OFF', "att": [("id", item.id)]},
                    {"name": "catag.show_layers", "icon": 'INFO_LARGE', "att": [("id", item.id)]}
                ],
                attributes = [(f'{item.name}', icontype)] if item.tag != '' else [(f'{item.name}', icontype)],             
                property = 'types',
                only_children=True
            )
             

class BIM_UL_layers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            row.label(text=item.name, icon='LAYER_USED')
            row.operator("catag.select_layer", text="", icon='OBJECT_DATA').id = item.id
