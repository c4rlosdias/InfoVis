import bpy
import textwrap

from ...data.tree import draw_tree


def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)


class Panel_Connect(bpy.types.Panel):
    
    bl_label        = "Subsea Classes"
    bl_idname       = "VIEW3D_PT_og_connect"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"    
    bl_category     = "InfoVis-Dictionary"
    bl_order = 0
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='OUTLINER')

    def draw(self, context):           
        layout = self.layout
        props = context.scene.og_props

        row = layout.row()
        row.operator("bsdd.get_class", text="get classes from bSDD")
        if len(props.classes_shown) > 0:
            row = layout.row()
            row.label(text="Classes Information:", icon='INFO')

            self.layout.template_list(
                "BIM_UL_classes",
                "",
                props,
                "classes_shown",
                props,
                "active_class_index",
                rows=10
            )

            active_class = props.classes_shown[props.active_class_index]
            row = layout.row()                                
            op = row.operator("bsdd.get_class_info", text="  Get Class Information  ")
            op.uri = active_class.uri
                              
            op2 = row.operator("bsdd.get_class_prop", text="  Get Class Properties  ")
            op2.uri = active_class.uri

            row = layout.row()
            row.separator()

            if props.classes_loaded:
                row = layout.row()
                row.label(text="Class Information:", icon='INFO')
                box = layout.box()
                row = box.row(align=True)                    
                row.label(text=f'Definition : ', icon='DOT')

                _label_multiline(
                    context=context,
                    text=props.class_definition,
                    parent=box
                )         
                                
                row = box.row()
                row.label(text=f'Description : {props.class_description}', icon='DOT')
                row = box.row()
                row.label(text=f'Version date : {props.class_version}', icon='DOT')
                row = box.row()
                row.label(text=f'Class type : {props.class_type}', icon='DOT')
                if props.class_ifctype != '':
                    row = box.row()
                    row.label(text=f'Ifc class : {props.class_ifctype}', icon='DOT') 
            
            if props.info_class_prop_loaded:
                row = layout.row()
                row.label(text="Class Properties Information:", icon='INFO')
                if len(props.class_prop_info)>0:
                    self.layout.template_list(
                        "BIM_UL_class_prop",
                        "",
                        props,
                        "class_prop_info",
                        props,
                        "active_class_prop_index",
                        rows=10
                    )
                else:
                   row.label(text="Class has no properties", icon='WARNING_LARGE') 

        if len(props.ifc_prop) > 0:
            row = layout.row()
            row.operator("object.clear_prop", text="Clear")
            row.operator("object.assign_all", text="Assing all")
            row.operator("object.unassign_all", text="Unassign all")
            row = layout.row()
            row.label(text="Properties of the selected objects:")                       
            self.layout.template_list(
                "BIM_UL_ifc_properties",
                "",
                props,
                "ifc_prop",
                props,
                "active_property_index",
            )
            
            active_property = props.ifc_prop[props.active_property_index]
            row = layout.row()                                
            op = row.operator("property.get_prop_info", text="  Get Property Information  ")
            op.uri = active_property.uri

            if props.info_prop_loaded:
                row = layout.row()
                row.label(text="Property Information:", icon='INFO')
                box = layout.box()
                row = box.row(align=True)                    
                row.label(text=f'Definition : ', icon='DOT')

                _label_multiline(
                    context=context,
                    text=props.prop_definition,
                    parent=box
                )
                
                row = box.row()
                row.label(text=f'Description : {props.prop_description}', icon='DOT')
                row = box.row()
                row.label(text=f'Data Type : {props.prop_datatype}', icon='DOT')
                row = box.row()
                row.label(text=f'Property Type : {props.prop_type}', icon='DOT')
                row = box.row()
                row.label(text=f'Units : {props.prop_units}', icon='DOT')
                row = layout.row()
                row.label(text="Related classes :", icon='DOT')
                self.layout.template_list(
                    "BIM_UL_property_class",
                    "",
                    props,
                    "class_info",
                    props,
                    "active_info_prop_index",
                )
                
            row = layout.row(align=True)
            row = layout.row()
            row.operator("object.add_prop", text="Add selected properties") 
            
        if len(props.classes_shown) > 0:
            row = layout.row()
            row.operator("ids.export", text="Export IDS file", icon="EXPORT")


class BIM_UL_ifc_properties(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            if item.is_selected == True:
                row.prop(item, "is_selected", text="", icon="RADIOBUT_ON")  
            else:
                row.prop(item, "is_selected", text="", icon="RADIOBUT_OFF", ) 
            row.label(text=item.name, icon="TEXT")            
            op = row.operator("object.uri", text="", icon="URL")
            op.uri = item.uri


class BIM_UL_property_class(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row()
            row.label(text=item.description)
            row.label(text=item.name)
            row.label(text=f'PSET: [{item.propertyset}]')
            op = row.operator("object.uri", text="", icon="URL")
            op.uri = item.uri
         
     
class BIM_UL_classes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            icon_type="COLOR"
            if item.type == 'Material':
                icon_type = 'MATERIAL_DATA'
            else:
                icon_type = 'COLOR'

            draw_tree(layout, item,
                operators = [
                    {"name": "object.uri", "icon": 'URL', "att": [("uri", item.uri)]}
                ],
                attributes = [(f'[{item.code}] {item.name}', icon_type)],                
                property = 'classes'
            )


class BIM_UL_class_prop(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            row.label(text= f'{item.description}', icon = 'DOT' )             
            row.operator("object.uri", text="", icon="URL").uri = item.uri
