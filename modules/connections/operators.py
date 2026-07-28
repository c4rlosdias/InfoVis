import bpy

from ...data.ifc_session import get_model

class Operator_disconnect(bpy.types.Operator):
    """Disconnect a selected object relationship."""
    bl_idname  = "conn.disconnect"
    bl_label   = "Disconnect Object"
    bl_options = {"REGISTER", "UNDO"} 
    
    rel_id: bpy.props.IntProperty()

    def execute(self, context):
        model = get_model()
        rel = model.by_id(self.rel_id)
        if rel:
            model.remove(rel)            
            self.report({'INFO'}, f"Disconnected connection {self.rel_id}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, f"No connection found for {self.rel_id}.")
            return {'CANCELLED'}

