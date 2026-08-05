"""CDE browser panel."""

import bpy


def _active(collection, index):
    return collection[index] if 0 <= index < len(collection) else None


class CDE_UL_projects(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.name or item.global_id, icon="FILE_FOLDER")
        if item.assets_count:
            row.label(text=f"{item.assets_count} asset(s)")


class CDE_UL_assets(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.name or item.global_id, icon="OUTLINER_COLLECTION")
        if item.global_id:
            row.label(text=f"Global ID: {item.global_id}")
        if item.asset_type:
            row.label(text=item.asset_type)


class CDE_UL_ifc_files(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.name or item.global_id, icon="FILE_3D")
        row.label(text=item.schema or item.status)


class CDE_UL_exports(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.filename or item.export_id, icon="EXPORT")
        row.label(text=item.status or "unknown")


class CDE_PT_browser(bpy.types.Panel):
    bl_label = "CDE"
    bl_idname = "VIEW3D_PT_infovis_cde"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "InfoVis-CDE"
    bl_order = 0

    def draw_header(self, context):
        self.layout.label(text="", icon="NETWORK_DRIVE")

    def draw(self, context):
        props, layout = context.window_manager.cde_props, self.layout
        auth = layout.box()
        auth.label(text="Connection", icon="LOCKED" if props.connection_status == "Connected" else "UNLOCKED")
        auth.prop(props, "base_url", text="URL")
        auth.prop(props, "client_id", text="Client ID")
        auth.prop(props, "client_secret", text="Client Secret")
        row = auth.row(align=True)
        row.operator("cde.login", text="Connect", icon="LINKED")
        row.operator("cde.logout", text="Disconnect", icon="UNLINKED")
        auth.label(text=props.connection_status)

        projects = layout.box()
        row = projects.row(align=True)
        row.label(text="Projects", icon="FILE_FOLDER")
        row.operator("cde.load_projects", text="", icon="FILE_REFRESH")
        projects.template_list("CDE_UL_projects", "", props, "projects", props, "project_index", rows=4)
        projects.operator("cde.load_assets", text="Load Assets", icon="DISCLOSURE_TRI_RIGHT")

        if props.assets:
            assets = layout.box()
            assets.label(text="Assets", icon="OUTLINER_COLLECTION")
            assets.template_list("CDE_UL_assets", "", props, "assets", props, "asset_index", rows=4)
            selected_asset = _active(props.assets, props.asset_index)
            if selected_asset:
                assets.label(text=f"Global ID: {selected_asset.global_id or '-'}")
                assets.label(text=f"Type: {selected_asset.asset_type or '-'}")
            assets.operator("cde.load_ifc_files", text="Load IFC Submissions", icon="FILE_3D")

        if props.ifc_files:
            files = layout.box()
            files.label(text="IFC Submissions", icon="FILE_3D")
            files.template_list("CDE_UL_ifc_files", "", props, "ifc_files", props, "ifc_file_index", rows=5)
            selected = _active(props.ifc_files, props.ifc_file_index)
            if selected:
                files.label(text=f"Status: {selected.status or '-'}")
                files.label(text=f"Schema: {selected.schema or '-'}")
                files.label(text=f"IFC Global ID: {selected.global_id or '-'}")
            files.label(text="Select the submission to use as the export source.", icon="INFO")

        if props.assets:
            exports = layout.box()
            row = exports.row(align=True)
            row.label(text="Exports", icon="EXPORT")
            refresh = row.row(align=True)
            refresh.enabled = bool(props.exports)
            refresh.operator("cde.load_exports", text="", icon="FILE_REFRESH")
            if props.exports:
                exports.template_list(
                    "CDE_UL_exports", "", props, "exports", props, "export_index", rows=5
                )
                selected_export = _active(props.exports, props.export_index)
                if selected_export:
                    exports.label(text=f"Status: {selected_export.status or '-'}")
                    exports.label(text=f"Export ID: {selected_export.export_id or '-'}")
                    exports.label(text=f"File: {selected_export.filename or '-'}")
                    if selected_export.error_message:
                        exports.label(text=f"Error: {selected_export.error_message}", icon="ERROR")
            else:
                exports.label(text="Generate an export for the selected IFC.", icon="INFO")
            row = exports.row(align=True)
            selected_submission = _active(props.ifc_files, props.ifc_file_index)
            generate_row = row.row(align=True)
            generate_row.enabled = bool(
                selected_submission
                and selected_asset
                and selected_submission.asset_global_id == selected_asset.global_id
                and selected_submission.global_id
            )
            generate_row.operator("cde.generate_export", text="Export Selected IFC", icon="ADD")
            open_row = row.row(align=True)
            selected_export = _active(props.exports, props.export_index)
            open_row.enabled = bool(
                selected_export
                and selected_export.status == "succeeded"
                and selected_asset
                and selected_export.asset_global_id == selected_asset.global_id
            )
            open_row.operator("cde.open_ifc", text="Open in Bonsai", icon="IMPORT")

        if props.operation_status:
            layout.box().label(text=props.operation_status, icon="INFO")


CLASSES = (
    CDE_UL_projects,
    CDE_UL_assets,
    CDE_UL_ifc_files,
    CDE_UL_exports,
    CDE_PT_browser,
)
