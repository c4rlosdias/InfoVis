import bpy

import ifcopenshell.api.pset
import ifcopenshell.util.element as element
import bonsai.tool as tool

from ...data.ifc_utils import get_prop_type
from ... import auth


class Panel_Properties(bpy.types.Panel):
    
    bl_label        = "Properties"
    bl_idname       = "VIEW3D_PT_og_properties"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G-Occurrence"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PROPERTIES')

    def draw(self, context):   
        props = context.scene.og_props 
        layout = self.layout       
        row = layout.row()   
        obj = context.active_object  
        

        if obj is not None and obj.select_get():
            model = tool.Ifc.get()     
            row = layout.row()                      
            row.operator("props.load_properties", text="Load properties")    

            if props.has_document and len(props.documents) > 0:
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

                        if auth.is_authenticated():
                            op0 = row.operator("props.load_doc", icon='FILEBROWSER', text="") 
                            op0.index = -1
                            op0.doc_index = document.index

                        op = row.operator("props.open_doc", icon='BORDERMOVE', text="")  
                        op.location = document.location

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
                            
                    row = layout.row()
                    if pset.is_expanded:
                        icon = 'TRIA_DOWN'
                    else:
                        icon = 'TRIA_RIGHT'
                    row.operator("props.expand", icon=icon, text="").index = pset.index
                    if props.show_description:
                        row.label(text=pset.description, icon='COPY_ID') 
                    else:
                        row.label(text=pset.name, icon='COPY_ID')                   
                         

                    layout.separator()

                    if pset.is_expanded:                        
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
                                    op = row.operator("props.doc_edit", icon='CHECKMARK', text="") 
                                    op.ifc_id = ifc_pset.id()
                                    op.id = document.identification   
                                    op.name = document.name 
                                    op.location = document.location                                  

                                    row = box.row()
                                    if auth.is_authenticated():
                                        row.prop(document, 'identification')
                                    else:
                                        row.label(text=f'Identification : {document.identification}')
                                    
                                    row = box.row()
                                    if auth.is_authenticated():
                                        row.prop(document, 'name')
                                    else:
                                        row.label(text=f'Name : {document.name}')
                                    
                                    row = box.row()
                                    if auth.is_authenticated():
                                        row.prop(document, 'location')
                                    else:
                                        row.label(text=f'Location : {document.location}')
                                    
                                    if document.location != '':
                                        op = row.operator("props.load_doc", icon='FILEBROWSER', text="") 
                                        op.index = pset.index 

                                        op = row.operator("props.open_doc", icon='BORDERMOVE', text="") 
                                        op.location = document.location                           
                                    
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
                        
                        for item in pset.props:   
                                                             
                            if 'Table' in  item.name:
                                names = item.name.split('_')

                                title = names[0]
                                if props.show_description:
                                    name_prop = item.description
                                else:
                                    name_prop = names[1]
                                
                                if title != old_title:
                                    rowb = box.row(align=True)
                                    rowb.scale_y =0.8                                    
                                    rowb.label(text=f' {title}', icon='VIEW_ORTHO')

                                    if 'Crushing' in pset.name:                                                                               
                                       op = rowb.operator("props.graph", icon='NORMALIZE_FCURVES', text="plot") 
                                       op.pset_index = pset.index
                                       op.prop_index = item.index
                                       

                                    rowb = box.row() 
                                    rowb = box.row(align=True)
                                    col = rowb.column(align=True)
                                    col.scale_x = 0.7
                                    
                                    i = 1

                                if i==1:
                                    col = rowb.column(align=True)                                
                                
                                if item.name not in titulos:
                                    if props.show_description:
                                        name_prop = f"{item.description} {item.datatype}" if item.description != '' else f"No description {item.datatype}"
                                    else:
                                        name_prop = f"{item.name.split('_')[1]} {item.datatype}"
                                    
                                    col.label(text=name_prop)                                        
                                    titulos = titulos + item.name  

                                act_prop = f"value{item.type_value}"  
                                if auth.is_authenticated():                                                                                            
                                    col.prop(item, act_prop, text='')                                
                                else:
                                    val= str(getattr(item, act_prop))
                                    col.label(text=f'|{val}|')
                                if i%item.n_rows == 0:
                                    col = rowb.column(align=True)   

                                old_title =title
                                old_name_prop = name_prop
  
                            else:    
                                if item.name != old_name_prop:
                                    rowb = box.row(align=True)
                                    if auth.is_authenticated():
                                        op=rowb.operator("props.edit", icon='CHECKMARK', text="")   
                                        op.pset_index = pset.index
                                        op.prop_index = item.index  
                                    if props.show_description:
                                        prop_name =  f' {item.description}' if item.description != '' else " No description"
                                        icon = 'BLANK'
                                    else:
                                        prop_name = f' {item.name}'   
                                        icon = 'BLANK'

                                    rowb.label(text=prop_name)
                                    

                                if item.type_prop == 'IfcPropertyEnumeratedValue':
                                    rowb = box.row(align=True)   
                                    col = rowb.column(align=True)
                                    if not auth.is_authenticated():
                                        col.prop(item, "enumerated", text='')
                                    else:
                                        val=getattr(item, "enbumerated")
                                        col.label(text=str(val))
                                    col = rowb.column(align=False)
                                    for enum in item.enumerations:
                                        col.prop(enum, "enumerated", text=getattr(enum, f"value{enum.type_value}"))
                                    if getattr(item, "has_document", False) and auth.is_authenticated():
                                        op=rowb.operator("props.edit", icon='CHECKMARK', text="")   
                                        op.pset_index = pset.index
                                        op.prop_index = item.index 
                                    old_name_prop = item.name   

                                else:
                                    col = rowb.column(align=True)
                                    col.alignment = 'RIGHT'
                                    act_prop = f"value{item.type_value}"  
                                    if auth.is_authenticated():                              
                                        col.prop(item, act_prop, text='')                                  
                                    else:
                                        val = getattr(item, act_prop)                                    
                                        col.label(text=str(val))                                                 
                                    col = rowb.column()
                                    col.scale_x =0.4
                                    col.label(text=item.datatype)
                                    old_name_prop = item.name 

                            i += 1

                    old_is_a = pset.is_a
        for area in context.screen.areas:
            area.tag_redraw()
