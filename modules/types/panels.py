import bpy
import bonsai.tool as tool

from ..catalog.operators import Operator_catalog_show_layers, Operator_catalog_select_elements


class Panel_Types(bpy.types.Panel):
    
    bl_label        = "Constructive Type"
    bl_idname       = "VIEW3D_PT_types"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Occurrence"
    bl_options      = {"DEFAULT_CLOSED"}
    
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GREASEPENCIL')    

    def draw(self, context):
        model = tool.Ifc.get()
        ifc_type = None
        layout = self.layout        
        props = context.scene.og_props
        row = layout.row()
        obj = context.active_object
        if obj is not None and obj.select_get():
            element = model.by_id(obj.BIMObjectProperties.ifc_definition_id)
            ifc_types = getattr(element, "IsTypedBy", None)
            if ifc_types:
                ifc_type = ifc_types[0].RelatingType
                if ifc_type:

                    row.label(text=f"{ifc_type.ElementType}")
                    row.operator("catag.select_elements", text="", icon='RESTRICT_SELECT_OFF').id = ifc_type.id()
                    row.operator("catag.show_layers", text="", icon='INFO_LARGE').id = ifc_type.id()
                    row.operator("element.select_object", text="", icon='RADIOBUT_ON').id = ifc_type.id()
                    row = layout.row()
                    row.label(text=f" Name           : {ifc_type.Name}", icon='DOT')
                    row = layout.row()
                    row.label(text=f" Description :  {ifc_type.Description}", icon = 'DOT')

                    if getattr(ifc_type, "HasAssociations", None):  
                        rels = ifc_type.HasAssociations
                        row= layout.row()
                        row.label(text="Associated Documents:", icon='FILE')                                                                        
                        for rel in rels:
                            if rel.is_a("IfcRelAssociatesDocument"):
                                document = rel.RelatingDocument  

                                location_value = str(getattr(document, 'Location', None))
                                if isinstance(location_value, str):
                                    location = location_value
                                elif location_value is not None:
                                    try:
                                        location = location_value.wrappedValue
                                    except AttributeError:
                                        location = str(location_value)
                                else:
                                    location = "N/A"
                                
                                box= layout.box()                      
                                row = box.row()
                                row.label(text=f"Identification: {getattr(document, 'Identification', 'N/A')}")
                                row = box.row()
                                row.label(text=f"Name: {getattr(document, 'Name', 'N/A')}")
                                row = box.row()
                                row.label(text=f"Location: {location}")
                                op = row.operator("props.open_doc", icon='BORDERMOVE', text="")  
                                op.location = location
                else:
                    row.label(text="Type: None", icon='ERROR')
            else:
                row.label(text="Type: None", icon='ERROR')
                


        row = layout.row()
        row.separator()
        row = layout.row()

        if len(props.layers) > 0 and ifc_type is not None and ifc_type.is_a("IfcPipeSegmentType"):            
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


        


