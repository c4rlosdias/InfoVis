import bpy


class Operator_add_ifc_label_attr(bpy.types.Operator):
    bl_idname  = "settings.add_ifc_label_attr"
    bl_label   = "Add Attribute"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        item = props.ifc_label_attributes.add()
        item.attr_name = "Name"
        props.active_ifc_label_attr_index = len(props.ifc_label_attributes) - 1
        return {"FINISHED"}


class Operator_remove_ifc_label_attr(bpy.types.Operator):
    bl_idname  = "settings.remove_ifc_label_attr"
    bl_label   = "Remove Attribute"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        idx = props.active_ifc_label_attr_index
        if 0 <= idx < len(props.ifc_label_attributes):
            props.ifc_label_attributes.remove(idx)
            props.active_ifc_label_attr_index = max(0, idx - 1)
        return {"FINISHED"}
