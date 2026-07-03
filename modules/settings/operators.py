import bpy

from ...data import config_profile
from ...data import decomposition_views
from ..catalog import operators as catalog_operators


_RELATION_PRESET_ITEMS = [
    (
        preset["key"],
        preset["label"],
        f"{preset['element_attribute']} / {preset['relationship_attribute']}",
    )
    for preset in decomposition_views.RELATION_PRESETS
]


def _get_addon_preferences(context):
    package_name = __package__.split(".modules", 1)[0]
    addon = context.preferences.addons.get(package_name)
    return addon.preferences if addon else None


def _get_addon_version():
    try:
        from ... import bl_info
    except Exception:
        return ""
    return ".".join(str(part) for part in bl_info.get("version", ()))


def _decomposition_payload_for_export(props):
    if props.decomposition_views_loaded and len(props.decomposition_views) > 0:
        return decomposition_views.payload_from_collection(props.decomposition_views)
    return config_profile.load_decomposition_payload()


def _li_mapping_payload_for_export(props):
    if props.li_mapping_loaded:
        return catalog_operators.li_mapping_payload_from_props(
            props,
            catalog_operators.load_li_mapping_payload(),
        )
    return catalog_operators.load_li_mapping_payload()


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


def _copy_relation_to_item(item, relation):
    normalized = decomposition_views.normalize_relation(relation)
    item.element_attribute = normalized["element_attribute"]
    item.relationship_type = normalized["relationship_type"]
    item.relationship_attribute = normalized["relationship_attribute"]


def _copy_view_to_item(item, view):
    item.id = view["id"]
    item.label = view.get("label", view["id"])
    item.root_ifc_class = view.get("root_ifc_class", "IfcProject")
    item.relations.clear()
    for relation in view.get("relations", []):
        relation_item = item.relations.add()
        _copy_relation_to_item(relation_item, relation)


def _load_views_into_props(props, views):
    props.decomposition_views.clear()
    for view in views:
        item = props.decomposition_views.add()
        _copy_view_to_item(item, view)

    props.active_decomposition_view_index = 0 if props.decomposition_views else -1
    props.active_decomposition_relation_index = 0
    props.decomposition_views_loaded = True


def _active_decomposition_view(props):
    index = props.active_decomposition_view_index
    if 0 <= index < len(props.decomposition_views):
        return props.decomposition_views[index]
    return None


def _unique_view_id(props, base="view"):
    base = base.strip().lower().replace(" ", "_") or "view"
    existing = {view.id for view in props.decomposition_views}
    if base not in existing:
        return base

    index = 1
    while f"{base}_{index}" in existing:
        index += 1
    return f"{base}_{index}"


class Operator_load_decomposition_views(bpy.types.Operator):
    bl_idname = "settings.load_decomposition_views"
    bl_label = "Load Decomposition Views"
    bl_description = "Load decomposition view configuration from decomposition_view.json"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        try:
            views = decomposition_views.load_views()
            from ...data import tree as data_tree
            data_tree.load_views(force=True)
        except Exception as exc:
            self.report({'ERROR'}, f"Could not load decomposition views: {exc}")
            return {"CANCELLED"}

        _load_views_into_props(props, views)
        self.report({'INFO'}, "Decomposition views loaded.")
        return {"FINISHED"}


class Operator_save_decomposition_views(bpy.types.Operator):
    bl_idname = "settings.save_decomposition_views"
    bl_label = "Save Decomposition Views"
    bl_description = "Save decomposition view configuration to decomposition_view.json"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        payload = decomposition_views.payload_from_collection(props.decomposition_views)
        errors = decomposition_views.validate_payload(payload)
        if errors:
            self.report({'ERROR'}, errors[0])
            return {"CANCELLED"}

        try:
            decomposition_views.save_payload(payload)
            from ...data import tree as data_tree
            data_tree.load_views(force=True)
        except Exception as exc:
            self.report({'ERROR'}, f"Could not save decomposition views: {exc}")
            return {"CANCELLED"}

        props.decomposition_views_loaded = True
        self.report({'INFO'}, "Decomposition views saved.")
        return {"FINISHED"}


class Operator_reset_decomposition_views(bpy.types.Operator):
    bl_idname = "settings.reset_decomposition_views"
    bl_label = "Reset Decomposition Views"
    bl_description = "Load the default decomposition views into the editor"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        _load_views_into_props(props, decomposition_views.default_views())
        self.report({'INFO'}, "Default decomposition views loaded. Click Save to write the JSON file.")
        return {"FINISHED"}


class Operator_add_decomposition_view(bpy.types.Operator):
    bl_idname = "settings.add_decomposition_view"
    bl_label = "Add Decomposition View"
    bl_description = "Add a new configurable decomposition view"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        item = props.decomposition_views.add()
        item.id = _unique_view_id(props)
        item.label = "New view"
        item.root_ifc_class = "IfcProject"
        relation = item.relations.add()
        _copy_relation_to_item(relation, decomposition_views.get_preset("aggregation"))

        props.active_decomposition_view_index = len(props.decomposition_views) - 1
        props.active_decomposition_relation_index = 0
        props.decomposition_views_loaded = True
        return {"FINISHED"}


class Operator_duplicate_decomposition_view(bpy.types.Operator):
    bl_idname = "settings.duplicate_decomposition_view"
    bl_label = "Duplicate Decomposition View"
    bl_description = "Duplicate the selected decomposition view"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        source = _active_decomposition_view(props)
        if source is None:
            self.report({'WARNING'}, "No decomposition view selected.")
            return {"CANCELLED"}

        item = props.decomposition_views.add()
        item.id = _unique_view_id(props, f"{source.id}_copy")
        item.label = f"{source.label or source.id} copy"
        item.root_ifc_class = source.root_ifc_class
        for relation in source.relations:
            relation_item = item.relations.add()
            relation_item.element_attribute = relation.element_attribute
            relation_item.relationship_type = relation.relationship_type
            relation_item.relationship_attribute = relation.relationship_attribute

        props.active_decomposition_view_index = len(props.decomposition_views) - 1
        props.active_decomposition_relation_index = 0
        return {"FINISHED"}


class Operator_remove_decomposition_view(bpy.types.Operator):
    bl_idname = "settings.remove_decomposition_view"
    bl_label = "Remove Decomposition View"
    bl_description = "Remove the selected decomposition view"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        index = props.active_decomposition_view_index
        if 0 <= index < len(props.decomposition_views):
            props.decomposition_views.remove(index)
            props.active_decomposition_view_index = min(
                max(index - 1, 0),
                len(props.decomposition_views) - 1,
            )
            props.active_decomposition_relation_index = 0
        return {"FINISHED"}


class Operator_add_decomposition_relation(bpy.types.Operator):
    bl_idname = "settings.add_decomposition_relation"
    bl_label = "Add IFC Relation"
    bl_description = "Add an IFC relationship traversal rule to the selected view"
    bl_options = {"REGISTER", "UNDO"}

    preset : bpy.props.EnumProperty(name="Preset", items=_RELATION_PRESET_ITEMS)

    def execute(self, context):
        props = context.scene.og_props
        view = _active_decomposition_view(props)
        if view is None:
            self.report({'WARNING'}, "No decomposition view selected.")
            return {"CANCELLED"}

        relation = view.relations.add()
        _copy_relation_to_item(relation, decomposition_views.get_preset(self.preset))
        props.active_decomposition_relation_index = len(view.relations) - 1
        return {"FINISHED"}


class Operator_remove_decomposition_relation(bpy.types.Operator):
    bl_idname = "settings.remove_decomposition_relation"
    bl_label = "Remove IFC Relation"
    bl_description = "Remove the selected IFC relationship traversal rule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        view = _active_decomposition_view(props)
        if view is None:
            self.report({'WARNING'}, "No decomposition view selected.")
            return {"CANCELLED"}

        index = props.active_decomposition_relation_index
        if 0 <= index < len(view.relations):
            view.relations.remove(index)
            props.active_decomposition_relation_index = min(
                max(index - 1, 0),
                len(view.relations) - 1,
            )
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


class Operator_export_config_profile(bpy.types.Operator):
    bl_idname = "settings.export_config_profile"
    bl_label = "Export Config Profile"
    bl_description = "Export editable InfoVis configuration to a portable JSON profile"
    bl_options = {"REGISTER"}

    filepath : bpy.props.StringProperty(
        name="File Path",
        default=config_profile.PROFILE_FILENAME,
        subtype="FILE_PATH",
    )
    filter_glob : bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = config_profile.PROFILE_FILENAME
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        props = context.scene.og_props
        preferences = _get_addon_preferences(context)

        try:
            profile = config_profile.build_profile(
                props=props,
                preferences=preferences,
                addon_version=_get_addon_version(),
                decomposition_payload=_decomposition_payload_for_export(props),
                li_mapping_payload=_li_mapping_payload_for_export(props),
            )
            errors = config_profile.validate_profile(profile)
            if errors:
                self.report({'ERROR'}, errors[0])
                return {'CANCELLED'}

            output_path = config_profile.ensure_json_suffix(self.filepath)
            config_profile.save_json(output_path, profile)
        except Exception as exc:
            self.report({'ERROR'}, f"Could not export config profile: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Config profile exported to {output_path}")
        return {'FINISHED'}


class Operator_import_config_profile(bpy.types.Operator):
    bl_idname = "settings.import_config_profile"
    bl_label = "Import Config Profile"
    bl_description = "Import editable InfoVis configuration from a portable JSON profile"
    bl_options = {"REGISTER", "UNDO"}

    filepath : bpy.props.StringProperty(
        name="File Path",
        default=config_profile.PROFILE_FILENAME,
        subtype="FILE_PATH",
    )
    filter_glob : bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        props = context.scene.og_props
        preferences = _get_addon_preferences(context)

        try:
            profile = config_profile.load_json(self.filepath)
            errors = config_profile.validate_profile(profile)
            if errors:
                self.report({'ERROR'}, errors[0])
                return {'CANCELLED'}

            decomposition_payload = profile.get("decomposition_views")
            if decomposition_payload is not None:
                views = decomposition_views.save_payload(decomposition_payload)["views"]
                from ...data import tree as data_tree
                data_tree.load_views(force=True)
                _load_views_into_props(props, views)

            li_mapping_payload = profile.get("li_mapping")
            if li_mapping_payload is not None:
                catalog_operators.save_li_mapping_payload(li_mapping_payload)
                catalog_operators.apply_li_mapping_payload_to_props(
                    props,
                    li_mapping_payload,
                )

            config_profile.apply_label_settings_to_props(
                props,
                profile.get("label_settings", {}),
            )
            config_profile.apply_preferences_to_addon_preferences(
                preferences,
                profile.get("preferences", {}),
            )
        except Exception as exc:
            self.report({'ERROR'}, f"Could not import config profile: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, "Config profile imported.")
        return {'FINISHED'}
