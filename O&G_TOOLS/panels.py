import bpy
from .operators import *
import bonsai.tool as tool
import textwrap


def _label_multiline(context, text, parent):
    chars = int(context.region.width / 6)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)

# ---------------------------------------------------------------------
# Conecta com o bSDD e apresenta as versões do dicionário
# ---------------------------------------------------------------------

class Panel_Connect(bpy.types.Panel):
    
    bl_label        = "Choose dictionary version"
    bl_idname       = "VIEW3D_PT_connect"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw(self, context):           
        layout = self.layout
        props = context.scene.my_props
        row = layout.row()
        row.prop(props, 'dictionary')


# ---------------------------------------------------------------------
# Importa e/ou atualiza as propriedades diretamente do dicionário no bSDD
# para um template de propriedades no Bonsai
# ---------------------------------------------------------------------

class Panel_Import_Properties(bpy.types.Panel):
    
    bl_label        = "Oil & Gas Subsea Get Properties"
    bl_idname       = "VIEW3D_PT_dictionary"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}
    
    
    def draw(self, context):           
        layout = self.layout     
        props = context.scene.my_props
        # botão para conectar com o bSDD e obter as propriedades do dicionario selecionado
        row = layout.row()
        row.operator("bsdd.get_prop", text="get properties from bSDD")
        # imprime a lista de propriedades do elemento selecionado
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
            
            # botao para imprimir info da propriedade ativa
            active_property = props.ifc_prop[props.active_property_index]
            row = layout.row()                                
            op = row.operator("property.get_prop_info", text="  Get Property Information  ")
            op.uri = active_property.uri

            # Imprime informações da propriedade ativa 
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



# Painel de propriedades            
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


# Painel de classe das propriedades            
class BIM_UL_property_class(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row()
            row.label(text=item.description)
            row.label(text=item.name)
            row.label(text=f'PSET: [{item.propertyset}]')
            op = row.operator("object.uri", text="", icon="URL")
            op.uri = item.uri
            

# ---------------------------------------------------------------------
# Importa as classes diretamente do dicionário no bSDD 
# da versão selecionada
# ---------------------------------------------------------------------

class Panel_Import_Classes(bpy.types.Panel):
    
    bl_label        = "Oil & Gas Subsea Get Classes"
    bl_idname       = "VIEW3D_PT_import_classes"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}


    def draw(self, context):           
        layout = self.layout     
        props = context.scene.my_props
        # botão para conectar com o bSDD e obter as propriedades do dicionario selecionado
        row = layout.row()
        row.operator("bsdd.get_class", text="get classes from bSDD")
        # Imprime informações da propriedade ativa 
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

            # botao para imprimir info da classe ativa
            active_class = props.classes_shown[props.active_class_index]
            row = layout.row()                                
            op = row.operator("bsdd.get_class_info", text="  Get Class Information  ")
            op.uri = active_class.uri

            row = layout.row()
            row.label(text=str(active_class.name))
            row.label(text=str(props.active_class_index))
            # Imprime informações da classe ativa 
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

                
            
# Painel de classes             
class BIM_UL_classes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            if item.type == 'Material':
                icontype = 'MATERIAL_DATA'
            else:
                icontype = 'COLOR'

            if not item.is_hidden:
                for i in range(0, item.level_index - 1):
                    row.label(text="", icon="BLANK1")
                if item.has_children:
                    if item.is_expanded:
                        row.operator(
                            "object.contract_classes", text="", emboss=False, icon="DISCLOSURE_TRI_DOWN"
                        ).index = item.index
                    else:
                        row.operator(
                            "object.expand_classes", text="", emboss=False, icon="DISCLOSURE_TRI_RIGHT"
                        ).index = item.index
                else:
                    row.label(text="", icon="BLANK1") 

                row.label(text= f'[{item.code}] {item.name}', icon = icontype ) 
                row.operator("object.create", text="", icon="RESTRICT_SELECT_OFF").uri = item.uri
                row.operator("object.uri", text="", icon="URL").uri = item.uri


# ---------------------------------------------------------------------
# Exporta as definições das propriedades no template do usuário para 
# um arquivo IDS
# ---------------------------------------------------------------------

class Panel_Export_Properties(bpy.types.Panel):
    
    bl_label        = "Export Property template"
    bl_idname       = "VIEW3D_PT_export"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}
    
    
    def draw(self, context):           
        layout = self.layout 
        model = tool.Ifc.get()
        if model:
            row = layout.row()
            row.operator("ids.export", text="Export local template to IDS file", icon="EXPORT")


# ---------------------------------------------------------------------
# Mostra a arvore de decomposicao dos elementos
#
# ---------------------------------------------------------------------

class Panel_Decompositions(bpy.types.Panel):
    
    bl_label        = "Decompositions"
    bl_idname       = "VIEW3D_PT_decompositions"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Decomposition"
    bl_options      = {"DEFAULT_CLOSED"}
    
    
    def draw(self, context):           
        layout = self.layout     
        props = context.scene.my_props
        row = layout.row()
        row.operator("elements.decomposition", text="load")

        # Imprime a arvore de decomposicao de elementos 
        if len(props.elements_containers) > 0:
            row = layout.row()
            row.label(text="Element decomposition:", icon='INFO')

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
        row.label(text=f"{props.active_element_index}")


# Painel de classes             
class BIM_UL_decomposition(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            
                    

            row = layout.row(align=True)

            objs = [tool.Ifc.get_entity(x).id()  for x in context.selected_objects]
            

            if item.type == "IfcProject":
                icon = 'CURRENT_FILE'
            elif item.type == "IfcSite":
                icon = 'WORLD'
            elif item.type == "IfcBuilding":
                icon = 'RENDER_STILL'
            elif item.type == "IfcElementAssembly":
                icon = 'PROP_ON'
            elif item.type == "IfcPipeSegment":
                icon = 'IPO_EASE_OUT'            
            elif item.type == "IfcCableSegment":
                icon = 'OUTLINER_DATA_LIGHT'            
            else:
                icon = 'OUTLINER'

            #props = context.scene.my_props

            if not item.is_hidden:
                for i in range(0, item.level - 1):
                    row.label(text="", icon="BLANK1")

                if item.has_children:
                    if item.is_expanded:
                        row.operator(
                            "element.contract_decomposition", text="", emboss=False, icon="DISCLOSURE_TRI_DOWN"
                        ).index = item.index
                    else:
                        row.operator(
                            "element.expand_decomposition", text="", emboss=False, icon="DISCLOSURE_TRI_RIGHT"
                        ).index = item.index
                else:
                    row.label(text="", icon="BLANK1") 
                row.label(text= item.name, icon = icon )

                icon2 = "CANCEL" if item.is_selected == True else "RESTRICT_SELECT_OFF"                                
                row.operator("element.selection", text="", icon=icon2).index = item.index
                
                

                # row.operator("object.uri", text="", icon="URL").uri = item.uri

# ---------------------------------------------------------------------
# Conecta com o bSDD e apresenta as versões do dicionário
# ---------------------------------------------------------------------

class Panel_Catalog(bpy.types.Panel):
    
    bl_label        = "Type catalog"
    bl_idname       = "VIEW3D_PT_catalog"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Catalog"
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw(self, context):           
        layout = self.layout
        props = context.scene.my_props
        row = layout.row()
        row.label(text="ssss")
        row = layout.row()
        row.operator("catag.exp_json", text="export json")
        