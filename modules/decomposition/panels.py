import bpy

from ...data.tree import draw_tree


class _Panel_Decompositions(bpy.types.Panel):
    
    bl_label        = "Decompositions"
    bl_idname       = "VIEW3D_PT_og_decompositions"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Occurrence"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='NODETREE')

    def draw(self, context):   
        layout = self.layout     
        props = context.scene.og_props
        row = layout.row(align=True)
        row.operator("decomposition.load", text="Load decompositions")
        row.operator("decomposition.export_tree", text="Export", icon='EXPORT')
        row = layout.row()
        row.label(text="Project Composition:", icon='INFO')

        if len(props.containers_show) > 0:
            self.layout.template_list(
                "BIM_UL_decomposition",
                "",
                props,
                "containers_show",
                props,
                "active_element_index",
                rows=5
            )
            row = layout.row()

        row.label(text="Associated Contracts:", icon='INFO')
        row = layout.row()
        #row.prop(props, "tree_type", expand=True)
        

        if len(props.elements_tree) > 0:           

            self.layout.template_list(
                "BIM_UL_tree",
                "",
                props,
                "elements_tree",
                props,
                "active_tree_element_index",
                rows=5
            )
            row = layout.row()

class Panel_Decompositions(bpy.types.Panel):
    
    bl_label        = "Decompositions"
    bl_idname       = "VIEW3D_PT_og_decompositions"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Occurrence"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='NODETREE')

    def draw(self, context):   
        layout = self.layout     
        props = context.scene.og_props
        row = layout.row(align=True)
        #row.operator("decomposition.load", text="Load decompositions")
        row.operator("decomposition.export_tree", text="Export", icon='EXPORT')
        row = layout.row()
        row.label(text="Project Composition:", icon='INFO')

        row = layout.row()
        row.prop(props, "tree_type", expand=True)
        
        if len(props.containers_show) > 0:
            row = layout.row(align=True)
            op = row.operator("common.set_tree_expansion", text="Expand all", icon='DISCLOSURE_TRI_DOWN')
            op.expand = True
            op.property = "elements_containers"
            op = row.operator("common.set_tree_expansion", text="Collapse children", icon='DISCLOSURE_TRI_RIGHT')
            op.expand = False
            op.property = "elements_containers"

            self.layout.template_list(
                "BIM_UL_decomposition",
                "",
                props,
                "containers_show",
                props,
                "active_element_index",
                rows=5
            )
            row = layout.row()

        if len(props.elements_tree) > 0:    
            row = layout.row()  
            row.label(text="Associated Contracts:", icon='INFO')       
            self.layout.template_list(
                "BIM_UL_tree",
                "",
                props,
                "elements_tree",
                props,
                "active_tree_element_index",
                rows=5
            )
            row = layout.row()

class BIM_UL_decomposition(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        props = context.scene.og_props
        if item:

            row = layout.row(align=True)
            blank = 1
            if item.type == "IfcProject":
                icon = 'CURRENT_FILE'
            elif item.type == "IfcSite":
                icon = 'OBJECT_HIDDEN'
            elif item.type == "IfcBuilding":
                icon = 'STICKY_UVS_LOC'
            elif item.type == "IfcElementAssembly":
                icon = 'STICKY_UVS_LOC'
            elif item.type == "IfcPipeSegment":
                icon = 'IPO_EASE_OUT'         
            elif item.type == "IfcCableSegment":
                icon = 'DOT'  
            elif item.type == "IfcValve":
                icon = 'DOT'      
            else:
                icon = 'DOT'

            operators = []
            if item.has_children:
                operators += [                    
                        {"name": "decomposition.select_components", "icon": 'RESTRICT_SELECT_OFF', "att": [("index", item.index)]}
                ]


            draw_tree(layout, item,
                operators = operators,
                attributes = [(f'[{item.object_type}] {item.name}', icon)],                
                property = 'elements_containers'
            )


class BIM_UL_tree(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        props = context.scene.og_props
        if item:
            row = layout.row(align=True)
            blank = 1
            icon = 'NONE'

            draw_tree(layout, item,
                operators = [
                    {"name": "decomposition.select_element", "icon": 'OBJECT_DATAMODE', "att": [("index", item.index)]},
                    {"name": "decomposition.select_components", "icon": 'RESTRICT_SELECT_OFF', "att": [("index", item.index)]}
                ],
                attributes = [(f'[{item.name}] - {item.object_type}', icon)],                
                property = 'elements_tree'
            )
