"""Blender operators for browsing and opening IFC models from the CDE."""

from __future__ import annotations

import tempfile
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

import bpy

from .service import CDEClient, CDEError


_client: CDEClient | None = None
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="InfoVis-CDE")


def _props(context):
    return context.window_manager.cde_props


def _active(collection, index):
    return collection[index] if 0 <= index < len(collection) else None


def _require_client() -> CDEClient:
    if _client is None or not _client.authenticated:
        raise CDEError("Connect to the CDE before continuing.")
    return _client


def _error(operator, props, error):
    message = str(error)
    props.operation_status = message
    operator.report({"ERROR"}, message)
    return {"CANCELLED"}


def _add_export(props, data, asset_global_id):
    item = props.exports.add()
    item.export_id = str(data.get("id") or "")
    item.asset_global_id = str(data.get("asset_global_id") or asset_global_id)
    item.source_ifc_file_id = str(
        data.get("source_ifc_file_id") or data.get("source_ifc_file") or ""
    )
    item.status = str(data.get("status") or "")
    item.filename = str(data.get("artifact_filename") or "")
    item.file_size = int(data.get("artifact_size") or 0)
    item.created_date = str(data.get("created_date") or "")
    item.error_message = str(data.get("error_message") or data.get("error_code") or "")
    return item


class CDE_OT_login(bpy.types.Operator):
    bl_idname = "cde.login"
    bl_label = "Connect"
    bl_description = "Authenticate with the CDE and start a JWT session"

    def execute(self, context):
        global _client
        props = _props(context)
        try:
            client = CDEClient(props.base_url)
            client.authenticate(props.client_id, props.client_secret)
            _client = client
            props.client_secret = ""
            props.connection_status = "Connected"
            props.operation_status = "JWT session started"
            bpy.ops.cde.load_projects()
            return {"FINISHED"}
        except Exception as error:
            props.connection_status = "Disconnected"
            return _error(self, props, error)


class CDE_OT_logout(bpy.types.Operator):
    bl_idname = "cde.logout"
    bl_label = "Disconnect"

    def execute(self, context):
        global _client
        props = _props(context)
        if _client:
            _client.logout()
        _client = None
        props.projects.clear(); props.assets.clear(); props.ifc_files.clear(); props.exports.clear()
        props.project_index = props.asset_index = props.ifc_file_index = props.export_index = -1
        props.connection_status, props.operation_status = "Disconnected", ""
        return {"FINISHED"}


class CDE_OT_load_projects(bpy.types.Operator):
    bl_idname = "cde.load_projects"
    bl_label = "Refresh Projects"

    def execute(self, context):
        props = _props(context)
        try:
            rows = _require_client().list_projects()
            props.projects.clear(); props.assets.clear(); props.ifc_files.clear(); props.exports.clear()
            for data in rows:
                item = props.projects.add()
                item.local_id = str(data.get("id") or "")
                item.global_id = str(data.get("global_id") or "")
                item.name = str(data.get("name") or item.global_id or "Project")
                item.description = str(data.get("description") or "")
                item.assets_count = str(data.get("assets_count") or "")
            props.project_index = 0 if props.projects else -1
            props.asset_index = props.ifc_file_index = props.export_index = -1
            props.operation_status = f"{len(rows)} project(s) found"
            return {"FINISHED"}
        except CDEError as error:
            return _error(self, props, error)


class CDE_OT_load_assets(bpy.types.Operator):
    bl_idname = "cde.load_assets"
    bl_label = "Load Assets"

    def execute(self, context):
        props, project = _props(context), _active(_props(context).projects, _props(context).project_index)
        if not project or not project.global_id:
            return _error(self, props, CDEError("Select a project."))
        try:
            rows = _require_client().list_assets(project.global_id)
            props.assets.clear(); props.ifc_files.clear(); props.exports.clear()
            for data in rows:
                item = props.assets.add()
                item.local_id = str(data.get("id") or "")
                item.global_id = str(data.get("global_id") or "")
                item.name = str(data.get("name") or item.global_id or "Asset")
                item.asset_type = str(data.get("type") or "")
            props.asset_index = 0 if props.assets else -1
            props.ifc_file_index = props.export_index = -1
            props.operation_status = f"{len(rows)} asset(s) found"
            return {"FINISHED"}
        except CDEError as error:
            return _error(self, props, error)


class CDE_OT_load_ifc_files(bpy.types.Operator):
    bl_idname = "cde.load_ifc_files"
    bl_label = "Load IFC Submissions"

    def execute(self, context):
        props, asset = _props(context), _active(_props(context).assets, _props(context).asset_index)
        if not asset or not asset.global_id:
            return _error(self, props, CDEError("Select an asset."))
        try:
            rows = _require_client().list_ifc_files(asset.global_id)
            props.ifc_files.clear()
            for data in rows:
                item = props.ifc_files.add()
                item.local_id = str(
                    data.get("id")
                    or data.get("pk")
                    or data.get("local_id")
                    or data.get("uuid")
                    or data.get("source_ifc_file_id")
                    or data.get("source_ifc_file")
                    or data.get("ifc_file_id")
                    or ""
                )
                item.global_id = str(data.get("global_id") or "")
                item.asset_global_id = asset.global_id
                item.name = str(data.get("name") or item.global_id or "model.ifc")
                item.schema, item.status = str(data.get("schema") or ""), str(data.get("status") or "")
                item.file_size = int(data.get("file_size") or 0)
            props.ifc_file_index = 0 if props.ifc_files else -1
            props.operation_status = f"{len(rows)} IFC file(s) found"
            return {"FINISHED"}
        except (CDEError, TypeError, ValueError) as error:
            return _error(self, props, error)


class CDE_OT_load_exports(bpy.types.Operator):
    bl_idname = "cde.load_exports"
    bl_label = "Refresh Selected IFC Export"

    def execute(self, context):
        props = _props(context)
        asset = _active(props.assets, props.asset_index)
        if not asset or not asset.global_id:
            return _error(self, props, CDEError("Select an asset."))
        selected = _active(props.exports, props.export_index)
        if not selected or not selected.export_id:
            return _error(self, props, CDEError("Generate an export for the selected IFC first."))
        try:
            data = _require_client().get_export(asset.global_id, selected.export_id)
            props.exports.clear()
            _add_export(props, data, asset.global_id)
            props.export_index = 0
            props.operation_status = "Selected IFC export refreshed"
            return {"FINISHED"}
        except (CDEError, TypeError, ValueError) as error:
            return _error(self, props, error)


class CDE_OT_generate_export(bpy.types.Operator):
    bl_idname = "cde.generate_export"
    bl_label = "Generate Export"
    bl_description = "Generate an export from the selected IFC submission"

    _future: Future | None = None
    _timer = None
    _progress_lock = threading.Lock()
    _progress_status = ""
    _asset_global_id = ""

    def _set_progress(self, status):
        with self._progress_lock:
            self._progress_status = status

    def execute(self, context):
        props = _props(context)
        asset = _active(props.assets, props.asset_index)
        if not asset or not asset.global_id:
            return _error(self, props, CDEError("Select an asset."))
        submission = _active(props.ifc_files, props.ifc_file_index)
        if not submission:
            return _error(self, props, CDEError("Select an IFC submission."))
        if submission.asset_global_id != asset.global_id:
            return _error(self, props, CDEError("Load and select an IFC submission for the selected asset."))
        ifc_global_id = submission.global_id
        if not ifc_global_id:
            return _error(self, props, CDEError("The selected IFC submission has no GlobalId."))
        try:
            client = _require_client()
        except CDEError as error:
            return _error(self, props, error)
        props.operation_status = f"Requesting export for {submission.name or ifc_global_id}..."
        self._asset_global_id = asset.global_id
        self._future = _executor.submit(
            client.generate_export_and_wait,
            asset.global_id,
            ifc_global_id,
            self._set_progress,
        )
        self._timer = context.window_manager.event_timer_add(0.25, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "ESC":
            self._finish(context)
            _props(context).operation_status = "Export monitoring canceled"
            return {"CANCELLED"}
        if event.type != "TIMER" or not self._future:
            return {"PASS_THROUGH"}
        with self._progress_lock:
            status = self._progress_status
        if status:
            _props(context).operation_status = f"IFC export: {status}"
        if not self._future.done():
            return {"PASS_THROUGH"}
        try:
            export = self._future.result()
            self._finish(context)
            export_id = str(export.get("id") or "")
            props = _props(context)
            props.exports.clear()
            _add_export(props, export, self._asset_global_id)
            props.export_index = 0
            props.operation_status = f"Export {export_id} succeeded"
            return {"FINISHED"}
        except Exception as error:
            self._finish(context)
            return _error(self, _props(context), error)

    def _finish(self, context):
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None


class CDE_OT_open_ifc(bpy.types.Operator):
    bl_idname = "cde.open_ifc"
    bl_label = "Open IFC from CDE"
    bl_description = "Download the selected completed export and open it with Bonsai"

    _future: Future | None = None
    _timer = None
    def execute(self, context):
        props = _props(context)
        asset = _active(props.assets, props.asset_index)
        selected = _active(props.exports, props.export_index)
        if not asset or not asset.global_id:
            return _error(self, props, CDEError("Select an asset."))
        if not selected or not selected.export_id:
            return _error(self, props, CDEError("Select an export."))
        if selected.asset_global_id and selected.asset_global_id != asset.global_id:
            return _error(self, props, CDEError("Refresh exports for the selected asset."))
        if selected.status != "succeeded":
            return _error(
                self,
                props,
                CDEError("The selected export is not ready. Refresh exports and select one with status succeeded."),
            )
        try:
            client = _require_client()
        except CDEError as error:
            return _error(self, props, error)
        props.operation_status = f"Downloading export {selected.export_id}..."
        cache_dir = str(Path(tempfile.gettempdir()) / "infovis_cde")
        filename = selected.filename or f"{asset.global_id}-{selected.export_id}.ifc"
        self._future = _executor.submit(
            client.download_export,
            asset.global_id,
            selected.export_id,
            cache_dir,
            filename,
        )
        self._timer = context.window_manager.event_timer_add(0.25, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "ESC":
            self._finish(context)
            _props(context).operation_status = "Opening canceled"
            return {"CANCELLED"}
        if event.type != "TIMER" or not self._future:
            return {"PASS_THROUGH"}
        if not self._future.done():
            return {"PASS_THROUGH"}
        try:
            filepath = self._future.result()
            self._finish(context)
            _props(context).operation_status = f"Opening {Path(filepath).name} in Bonsai..."
            result = bpy.ops.bim.load_project(filepath=filepath, should_start_fresh_session=True,
                                              use_relative_path=False)
            if "CANCELLED" in result:
                raise CDEError("Bonsai could not open the downloaded IFC.")
            _props(context).operation_status = f"IFC opened: {Path(filepath).name}"
            return {"FINISHED"}
        except Exception as error:
            self._finish(context)
            return _error(self, _props(context), error)

    def _finish(self, context):
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None


CLASSES = (
    CDE_OT_login,
    CDE_OT_logout,
    CDE_OT_load_projects,
    CDE_OT_load_assets,
    CDE_OT_load_ifc_files,
    CDE_OT_load_exports,
    CDE_OT_generate_export,
    CDE_OT_open_ifc,
)
