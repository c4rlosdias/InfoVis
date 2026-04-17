import bpy
import bonsai.tool as tool

from ...data.ifc_utils import add_connections


class Operator_disconnect(bpy.types.Operator):
    """Operator para desconectar um objeto selecionado"""
    bl_idname  = "conn.disconnect"
    bl_label   = "Disconnect Object"
    bl_options = {"REGISTER", "UNDO"} 
    
    rel_id: bpy.props.IntProperty()

    def execute(self, context):
        model = tool.Ifc.get()
        rel = model.by_id(self.rel_id)
        if rel:
            model.remove(rel)            
            self.report({'INFO'}, f"Disconnected connection {self.rel_id}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, f"No connection found for {self.rel_id}.")
            return {'CANCELLED'}
        

class Operator_select_object(bpy.types.Operator):
    """Operator para selecionar objeto com eyedropper e atribuir à propriedade correta"""
    bl_idname  = "conn.select_object"
    bl_label   = "Select Object"
    bl_options = {"REGISTER", "UNDO"} 
    
    obj_name: bpy.props.StringProperty()

    def execute(self, context):
        wm = context.window_manager

        if getattr(wm, self.obj_name, None) is None:
            setattr(wm, self.obj_name, context.active_object)
            self.report({'INFO'}, f"Selected {context.active_object.name} for {self.obj_name}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Both connection object fields are already filled.")
            return {'CANCELLED'}


class Operator_add_connect(bpy.types.Operator):
    """Adiciona conexão selecionando objeto via UI"""
    bl_idname  = "conn.add_connect"
    bl_label   = "Add Connection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        props = context.scene.og_props
        obj_a = getattr(wm, 'add_connect_object_a', None)
        obj_b = getattr(wm, 'add_connect_object_b', None)
        obj_c = getattr(wm, 'add_connect_object_c', None)
        r = add_connections(obj_a, obj_b, obj_c, props.connect_type)
        if r:
            self.report({'INFO'}, "Connection added successfully.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to add connection. Check console for details.")
            return {'CANCELLED'}
