import bpy
import bonsai.tool as tool

from ..common.operators import Select_object


class Panel_Connect_Elements(bpy.types.Panel):
    
    bl_label        = "Connect Elements"
    bl_idname       = "VIEW3D_PT_connect_elements"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Occurrence"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def get_connects(self, object):
        connects = []
        element = tool.Ifc.get_entity(object)
        rels1 = element.ConnectedFrom if hasattr(element, 'ConnectedFrom') else []
        rels2 = element.ConnectedTo if hasattr(element, 'ConnectedTo') else []
        rels3 = element.IsConnectionRealization if hasattr(element, 'IsConnectionRealization') else []
        rels = list(rels1) + list(rels2) + list(rels3)
        rels= set(rels)
        for rel in rels:
            if rel.is_a("IfcRelConnectsElements") or rel.is_a("IfcRelConnectsWithRealizingElements"):                
                connects.append(
                    {   
                        'id': rel.id(),
                        'Connection Type': rel.is_a(),  
                        'Related Element': rel.RelatedElement,
                        'Relating Element': rel.RelatingElement,                        
                        'Realizing Elements': getattr(rel, 'RealizingElements', None)
                    }
                )
            else:
                connects.append(
                    {
                        'id': rel.id(),
                        'Connection Type': rel.is_a(),  
                        'Related Port': rel.RelatedPort,
                        'Relating Port': rel.RelatingPort,                        
                        'Realizing Element': getattr(rel, 'RealizingElement', None)
                    }
                )

        return connects
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GREASEPENCIL')    

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        if len(context.selected_objects) > 0:
            for obj in context.selected_objects:
                row=layout.row()
                row.separator()
                row=layout.row()
                row.label(text=f"Selected: {obj.name}", icon='OBJECT_DATA')                
                c = 1
                for connect in self.get_connects(obj):
                    row = layout.row()
                    row.label(text=f"connection #{c}", icon='LINKED')
                    row.operator("conn.disconnect", text="", icon='UNLINKED').rel_id = connect['id']
                    self.draw_connect(layout, connect)
                    c += 1

    def draw_connect(self, layout, connect):
        box = layout.box()

        row=box.row()
        col1 = row.column(align=True)
        col2 = row.column(align=True)
        col3 = row.column(align=True)

        row=col1.row(align=True)        
        row.operator("element.select_object", text="", icon='RESTRICT_SELECT_OFF').id = connect['Related Element'].id() 
        row.label(text=connect['Related Element'].Name if connect['Related Element'] else "None") 
        row=col2.row(align=True)
        row.label(text= '', icon='ARROW_LEFTRIGHT')      
        row=col3.row(align=True)
        row.label(text=connect['Relating Element'].Name if connect['Relating Element'] else "None")
        row.operator("element.select_object", text="", icon='RESTRICT_SELECT_OFF').id = connect['Relating Element'].id()
        
        if 'Realizing Elements' in connect and connect['Realizing Elements']:
            for value in connect['Realizing Elements']:
                row = box.row()
                row.label(text=f"{value.Name}:", icon='DOT')
                row.operator("element.select_object", text="", icon='RESTRICT_SELECT_OFF').id = value.id()                   

    def _draw_connect(self, layout, connect):
        box = layout.box()
        for key, value in connect.items():
            if key == 'id':
                continue
            if isinstance(value, (tuple, list)) and value:
                row = box.row()
                row.label(text=f"{key}:", icon='LINKED')
                for v in value:
                    row = box.row(align=True)
                    row.label(text=f"     {getattr(v, 'Name', str(v))}", icon='DOT') 
                    if type(v) != str and hasattr(v, 'id') and (v.is_a("IfcElement") or v.is_a("IfcPort")):
                        row.operator("element.select_object", text="", icon='RESTRICT_SELECT_OFF').id = v.id()                   
            elif value is not None:
                row = box.row()
                row.label(text=f"{key}: {getattr(value, 'Name', str(value))}", icon='LINKED')
                if type(value) != str and hasattr(value, 'id') and (value.is_a("IfcElement") or value.is_a("IfcPort")):
                    row.operator("element.select_object", text="", icon='RESTRICT_SELECT_OFF').id = value.id()           
