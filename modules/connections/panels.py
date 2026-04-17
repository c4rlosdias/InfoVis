import bpy
import bonsai.tool as tool

from ... import auth


class Panel_Connect_Elements(bpy.types.Panel):
    
    bl_label        = "Connect Elements"
    bl_idname       = "VIEW3D_PT_connect_elements"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "O&G-Occurrence"
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
                        'Relating Element': rel.RelatingElement,
                        'Related Element': rel.RelatedElement,
                        'Realizing Elements': getattr(rel, 'RealizingElements', None)
                    }
                )
            else:
                connects.append(
                    {
                        'id': rel.id(),
                        'Connection Type': rel.is_a(),  
                        'Relating Port': rel.RelatingPort,
                        'Related Port': rel.RelatedPort,
                        'Realizing Element': getattr(rel, 'RealizingElement', None)
                    }
                )

        return connects
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GREASEPENCIL')    

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        props = context.scene.og_props
        row = layout.row()
        
        if len(context.selected_objects) > 0:
            for obj in context.selected_objects:
                row.label(text=f"Selected: {obj.name}", icon='OBJECT_DATA')                
                c = 1
                for connect in self.get_connects(obj):
                    row = layout.row()
                    row.label(text=f"connection #{c} - {connect['id']}", icon='LINKED')
                    if auth.is_authenticated():
                        row.operator("conn.disconnect", text="", icon='UNLINKED').rel_id = connect['id']
                    self.draw_connect(layout, connect)
                    c += 1

        row = layout.row()
        row.separator()
        row = layout.row()

        if auth.is_authenticated():
            row.label(text="Select objects to connect before clicking 'Add Connection'", icon='INFO')
            box = layout.box()
            row = box.row()
            row.prop(props, "connect_type", text="Connection Type")
            row = box.row()
            row.prop(wm, "add_connect_object_a", text="Relating Element A")
            if wm.add_connect_object_a is None:
                op= row.operator("conn.select_object", text="", icon='ADD')
                op.obj_name = "add_connect_object_a"
            row = box.row()
            row.prop(wm, "add_connect_object_b", text="Relating Element B")
            if wm.add_connect_object_b is None:
                op= row.operator("conn.select_object", text="", icon='ADD')
                op.obj_name = "add_connect_object_b"
        
            if props.connect_type != "IfcRelConnectsElements":
                row = box.row()
                row.prop(wm, "add_connect_object_c", text="Realizing Element")
                if wm.add_connect_object_c is None:
                    op = row.operator("conn.select_object", text="", icon='ADD')
                    op.obj_name = "add_connect_object_c"
            
            row = box.row()
            row.operator("conn.add_connect", text="Add Connection", icon='ADD')
        

    def draw_connect(self, layout, connect):
        box = layout.box()
        for key, value in connect.items():
            if key == 'id':
                continue
            if isinstance(value, (tuple, list)) and value:
                box.label(text=f"{key}:", icon='LINKED')
                for v in value:
                    box.label(text=f"    -{getattr(v, 'Name', str(v))}")                    
            elif value is not None:
                box.label(text=f"{key}: {getattr(value, 'Name', str(value))}", icon='LINKED')
