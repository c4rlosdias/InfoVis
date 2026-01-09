import bpy
from .operators import *


import bonsai.tool as tool
import textwrap



def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)

def get_properties(ifc_obj):

    result = []
    result.append()

def get_product_description(context, index):
    props = context.scene.og_props 
    products = props.products_show
    for product in products:
        if product.index == index:
            return product.description
    

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# O&G Dictionary
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

# Conecta com o bSDD e apresenta as versões do dicionário

class Panel_Connect(bpy.types.Panel):
    
    bl_label        = "Subsea Classes"
    bl_idname       = "VIEW3D_PT_og_connect"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"    
    bl_category     = "O&G Tools"
    bl_order = 0
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='OUTLINER')

    def draw(self, context):           
        layout = self.layout
        props = context.scene.og_props
        model = tool.Ifc.get()

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
                              
            op2 = row.operator("bsdd.get_class_prop", text="  Get Class Properties  ")
            op2.uri = active_class.uri

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
            
            # Imprime informações da classe ativa 
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
            
            if model:
                row = layout.row()
                row.operator("ids.export", text="Export local template to IDS file", icon="EXPORT")

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
                row.operator("object.uri", text="", icon="URL").uri = item.uri

# Painel de propriedades da classe             
class BIM_UL_class_prop(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            row.label(text= f'{item.description}', icon = 'DOT' )             
            row.operator("object.uri", text="", icon="URL").uri = item.uri

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# O&G Decomposition
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

class Panel_Decompositions(bpy.types.Panel):
    
    bl_label        = "Decompositions"
    bl_idname       = "VIEW3D_PT_og_decompositions"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='NODETREE')

    def draw(self, context):           
        layout = self.layout     
        props = context.scene.og_props
        row = layout.row()
        row.operator("elements.decomposition", text="load")
        row = layout.row()
        row.prop(props, "show_ports")
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

# Painel de classes             
class BIM_UL_decomposition(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):        
        if item:
            row = layout.row(align=True)
            objs = [tool.Ifc.get_entity(x).id()  for x in context.selected_objects]           

            if item.type == "IfcProject":
                icon = 'CURRENT_FILE'
            elif item.type == "IfcSite":
                icon = 'OBJECT_HIDDEN'
            elif item.type == "IfcBuilding":
                icon = 'STICKY_UVS_LOC'
            elif item.type == "IfcElementAssembly":
                icon = 'OBJECT_HIDDEN'
            elif item.type == "IfcPipeSegment":
                icon = 'IPO_EASE_OUT'            
            elif item.type == "IfcCableSegment":
                icon = 'DOT'  
            elif item.type == "IfcValve":
                icon = 'DOT'           
            else:
                icon = 'DOT'

            #props = context.scene.og_props

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
                row.label(text= f'[{item.object_type}] {item.name}', icon=icon)
                icon2 = "CANCEL" if item.is_selected == True else "RESTRICT_SELECT_OFF"      
                row.operator("decomposition.select_element", text="", icon='OBJECT_DATAMODE').index = item.index                          
                row.operator("decomposition.select_components", text="", icon=icon2).index = item.index
             

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# O&G Catalog
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

class Panel_Catalog(bpy.types.Panel):
    
    bl_label        = "Type catalog"
    bl_idname       = "VIEW3D_PT_og_catalog"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GROUP_VCOL')

    def draw(self, context):   
        props = context.scene.og_props 
        layout = self.layout       
        row = layout.row()     

        # botão para conectar com o bSDD e obter as propriedades do dicionario selecionado
        row.operator("catag.load_products", text="Load type products")   

        # Imprime os produtos 
        if len(props.products) > 0:
            row = layout.row()
            row.label(text="Classes Information:", icon='INFO')

            self.layout.template_list(
                "BIM_UL_products",
                "",
                props,
                "products_show",
                props,
                "active_product_index",
                rows=10
            )
            
            row = layout.row()
            row.label(text="Product Information:", icon='INFO')
            box = layout.box()
            rowb = box.row()
            text = get_product_description(context, props.active_product_index)
            _label_multiline(context = context, parent = box, text = text)

# Painel de produtos             
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
                icontype = 'LAYER_ACTIVE'


            if not item.is_hidden:
                for i in range(0, item.level_index - 1):
                    row.label(text="", icon="BLANK1")
                if item.has_children:
                    if item.is_expanded:
                        row.operator(
                            "object.contract_products",
                            text="",
                            emboss=False,
                            icon="DISCLOSURE_TRI_DOWN"
                        ).index = item.index
                    else:
                        row.operator(
                            "object.expand_products",
                            text="",
                            emboss=False,
                            icon="DISCLOSURE_TRI_RIGHT"
                        ).index = item.index
                else:
                    row.label(text="", icon="BLANK1") 


                row.label(text= f'{item.name}', icon = icontype )

                if not item.has_children:
                    row.operator("catag.insert_type", text="", icon="PLUS").uri = item.name
                if item.uri != '':
                    row.operator("object.uri", text="", icon="URL").uri = item.uri

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# O&G Properties
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

class Panel_Properties(bpy.types.Panel):
    
    bl_label        = "Properties"
    bl_idname       = "VIEW3D_PT_og_properties"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PROPERTIES')

    def draw(self, context):   
        props = context.scene.og_props 
        layout = self.layout       
        row = layout.row()   
        # select objects 
        obj = context.active_object  
         
        
        if obj is not None and len(context.selected_objects) > 0:   
            model = tool.Ifc.get()     
            row = layout.row()                      
            row.operator("props.load_properties", text="Load properties")    

            # if the element type have some external document associated
            if props.has_document:
                    row = layout.row() 
                    row.label(text='Referenced documents:', icon = 'DOCUMENTS') 
                    if props.docs_expanded:
                        icon='TRIA_DOWN'
                    else:
                        icon='TRIA_RIGHT'
                    op = row.operator("docs.expand", icon=icon, text="")
                    op.index = -1
                    op.type = 'element'
                    
                    if props.docs_expanded:
                        box = layout.box()
                        for document in props.documents:
                            row = box.row() 
                            # operator to save the documento changes
                            op4 = row.operator("props.doc_edit", icon='CHECKMARK', text="") 
                            op4.ifc_id = tool.Ifc.get_entity(obj).id()
                            op4.id = document.identification
                            op4.name = document.name
                            op4.location = document.location

                            row = box.row()
                            row.prop(document, 'identification')
                            row = box.row()
                            row.prop(document, 'name')
                            row = box.row()
                            row.prop(document, 'location')

                            # operator to load external file
                            op0 = row.operator("props.load_doc", icon='FILEBROWSER', text="") 
                            op0.index = -1
                            op0.doc_index = document.index

                            # operator to visualize document
                            op = row.operator("props.open_doc", icon='BORDERMOVE', text="")  
                            op.location = document.location

                            # operator to plot
                            if document.location[-3:].upper() == 'CSV':
                                op3 = row.operator("props.graph", icon='NORMALIZE_FCURVES', text="") 
                                op3.pset_index = -1
                                op3.prop_index = -1 
                                op3.document = document.location


            layout.separator()                      
            
            if len(props.prop_metadata) > 0:
                old_is_a = ""
                row = layout.row()
                row.prop(props, "show_description")
                layout.separator()

                # imprime cada pset associado ao elemento
                for pset in props.prop_metadata:
                    row = layout.row()
                    if old_is_a != pset.is_a:
                        if pset.is_a == 'instance':
                            row = layout.row()
                            row.label(text="Occurence Properties:", icon='HOLDOUT_OFF') 
                            row = layout.row()
                        else:
                            row = layout.row()
                            row.label(text="Inherited Type Properties:", icon='CON_CHILDOF') 
                            row = layout.row()
                            
                    # pset é ou não expandida
                    row = layout.row()
                    if pset.is_expanded:
                        icon = 'TRIA_DOWN'
                    else:
                        icon = 'TRIA_RIGHT'
                    row.operator("props.expand", icon=icon, text="").index = pset.index
                    row.label(text=pset.name, icon='COPY_ID')                   
                         

                    layout.separator()

                    # se o pset está expandido                
                    if pset.is_expanded:                        
                        # se o pset tem algum documento externo associado
                        if pset.has_document:                               
                            ifc_pset = ifcopenshell.api.pset.add_pset(model, product=model.by_id(pset.id_obj), name=pset.name)  
                            row = layout.row()
                            row.label(text='Referenced documents:', icon='DOCUMENTS')

                            if pset.docs_expanded:
                                icon2='TRIA_DOWN'
                            else:
                                icon2='TRIA_RIGHT'
                            op = row.operator("docs.expand", icon=icon2, text="")
                            op.index = pset.index
                            op.type = 'property'    

                            if pset.docs_expanded:
                                box = layout.box()  
                                for document in pset.documents:                                
                                    row = box.row()
                                    # operador para editar a referencia                    
                                    op = row.operator("props.doc_edit", icon='CHECKMARK', text="") 
                                    op.ifc_id = ifc_pset.id()
                                    op.id = document.identification   
                                    op.name = document.name 
                                    op.location = document.location                                  

                                    row = box.row()
                                    row.prop(document, 'identification')
                                    row = box.row()
                                    row.prop(document, 'name')
                                    row = box.row()
                                    row.prop(document, 'location')
                                    # operador de carregamento de arquivo externo
                                    op = row.operator("props.load_doc", icon='FILEBROWSER', text="") 
                                    op.index = pset.index 

                                    # operador para visualizar o documento
                                    op = row.operator("props.open_doc", icon='BORDERMOVE', text="") 
                                    op.location = document.location                           
                                    
                                    # operador para plotagem do grafico
                                    if document.location[-3:].upper() == 'CSV':
                                        op = row.operator("props.graph", icon='NORMALIZE_FCURVES', text="") 
                                        op.pset_index = -1
                                        op.prop_index = -1
                                        op.document = document.location
                            
                        row = layout.row()
                        row.label(text="Properties:")
                        box = layout.box()
                        old_title="" 
                        old_name_prop = ""                        
                        titulos = '' 
                        i = 1
                        

                        # para cada propriedade
                        for item in pset.props:   
                                                             
                            # se existe a palavra Table no nome da propriedade
                            if 'Table' in  item.name:
                                names = item.name.split('_')
                                description = item.description
                                title = names[0]
                                if props.show_description:
                                    name_prop = item.description
                                else:
                                    name_prop = names[1]
                                
                                # imprime o titulo da tabela
                                if title != old_title:
                                    rowb = box.row(align=True)
                                    rowb.scale_y =0.8                                    
                                    rowb.label(text=f' {title}', icon='VIEW_ORTHO')

                                    # se a tabela representa dados para uma curva de crushing
                                    if 'Crushing' in pset.name:                                                                               
                                       op = rowb.operator("props.graph", icon='NORMALIZE_FCURVES', text="plot") 
                                       op.pset_index = pset.index
                                       op.prop_index = item.index

                                       print(pset.index)
                                       print(item.index)
                                       

                                    # imprime dados para a plotagem do gráfico
                                    rowb = box.row() 
                                    rowb = box.row(align=True)
                                    col = rowb.column(align=True)
                                    col.scale_x = 0.7
                                    
                                    i = 1

                                # monta a tabela
                                if i==1:
                                    col = rowb.column(align=True)                                
                                
                                if item.name not in titulos:
                                    if props.show_description:
                                        name_prop = f"{item.description} {item.datatype}"
                                    else:
                                        name_prop = f"{item.name.split('_')[1]} {item.datatype}"
                                    
                                    col.label(text=name_prop)                                        
                                    titulos = titulos + item.name  

                                act_prop = f"value{item.type_value}"                                                                                              
                                col.prop(item, act_prop, text='')                                
                                if i%item.n_rows == 0:
                                    col = rowb.column(align=True)   
                                    #col.alignment = 'CENTER' 

                                # controla a mudança de propriedades e colunas
                                old_title =title
                                old_name_prop = name_prop
  
                            #se não for tabela   
                            else:    
                                # se for o nome da propriedade                           
                                if item.name != old_name_prop:
                                    rowb = box.row(align=True)
                                    op=rowb.operator("props.edit", icon='CHECKMARK', text="")   
                                    op.pset_index = pset.index
                                    op.prop_index = item.index  
                                    prop_name =  f' {item.description}' if props.show_description else  f' {item.name}'                          
                                    rowb.label(text=prop_name)
                                    

                                # se for o tipo enumerado
                                if item.type_prop == 'IfcPropertyEnumeratedValue':
                                    rowb = box.row(align=True)   
                                    col = rowb.column(align=True)
                                    col.prop(item, "enumerated", text='')
                                    col = rowb.column(align=True)
                                    for enum in item.enumerations:
                                        print('ok')
                                        col.prop(enum, "enumerated", text=getattr(enum, f"value{enum.type_value}"))
                                    # se a propriedade tem documento associado
                                    if item.has_document:
                                        op=rowb.operator("props.edit", icon='CHECKMARK', text="")   
                                        op.pset_index = pset.index
                                        op.prop_index = item.index 
                                    old_name_prop = item.name   

                                # se for o valor da propriedade simples                               
                                else:
                                    col = rowb.column()
                                    col.scale_x =0.6
                                    act_prop = f"value{item.type_value}"                                
                                    col.prop(item, act_prop, text=item.datatype)
                                    old_name_prop = item.name 

                            i += 1

                    old_is_a = pset.is_a # type or instance
        for area in context.screen.areas:
            area.tag_redraw()



#============================================================================================
# Settings
#============================================================================================

class Panel_Settings(bpy.types.Panel):
    
    bl_label        = "Settings"
    bl_idname       = "VIEW3D_PT_og_settings"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PREFERENCES')

    def draw(self, context):
        layout = self.layout
        props = context.scene.og_props
        row = layout.row()
        row.label(text='Choose a bSDD dictionary:')
        row = layout.row()
        row.prop(props, 'dictionary')

#============================================================================================
# Info
#============================================================================================
class Panel_Info(bpy.types.Panel):
    
    bl_label        = "Info"
    bl_idname       = "VIEW3D_PT_og_info"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G Tools"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='INFO_LARGE')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="O&G Tools V 0.1.1", icon='MOD_LINEART')

