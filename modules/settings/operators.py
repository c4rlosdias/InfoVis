import bpy


def _add_ifc_label_field(props, field_name, display_name=""):
    field_name = field_name.strip()
    display_name = display_name.strip()
    if not field_name:
        return False

    for index, item in enumerate(props.ifc_label_attributes):
        if item.attr_name == field_name:
            if display_name:
                item.display_name = display_name
            props.active_ifc_label_attr_index = index
            return True

    item = props.ifc_label_attributes.add()
    item.attr_name = field_name
    item.display_name = display_name
    props.active_ifc_label_attr_index = len(props.ifc_label_attributes) - 1
    return True


class Operator_add_ifc_label_attr(bpy.types.Operator):
    bl_idname  = "settings.add_ifc_label_attr"
    bl_label   = "Add Attribute"
    bl_description = "Add an IFC attribute to the 3D View label"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        _add_ifc_label_field(props, "Name", "Name")
        return {"FINISHED"}


class Operator_add_ifc_label_property(bpy.types.Operator):
    bl_idname  = "settings.add_ifc_label_property"
    bl_label   = "Add Property"
    bl_description = "Add a property in Pset.Property format to the 3D View label"
    bl_options = {"REGISTER", "UNDO"}

    field_name : bpy.props.StringProperty(name="Property", default="Pset.Property")
    display_name : bpy.props.StringProperty(name="Display text", default="")

    def execute(self, context):
        props = context.scene.og_props
        if not _add_ifc_label_field(props, self.field_name, self.display_name):
            self.report({'WARNING'}, "Property name is empty.")
            return {"CANCELLED"}
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
