"""Runtime properties for the CDE panel."""

from bpy.props import CollectionProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup


def _clear_selected_ifc_export(self, context):
    """Do not show an export created for a previously selected submission."""
    self.exports.clear()
    self.export_index = -1


class CDEProjectItem(PropertyGroup):
    local_id: StringProperty(name="Internal ID")
    global_id: StringProperty(name="Global ID")
    name: StringProperty(name="Project")
    description: StringProperty(name="Description")
    assets_count: StringProperty(name="Assets")


class CDEAssetItem(PropertyGroup):
    local_id: StringProperty(name="Internal ID")
    global_id: StringProperty(name="Global ID")
    name: StringProperty(name="Asset")
    asset_type: StringProperty(name="Type")


class CDEIfcFileItem(PropertyGroup):
    local_id: StringProperty(name="Internal ID")
    global_id: StringProperty(name="Global ID")
    asset_global_id: StringProperty(name="Asset")
    name: StringProperty(name="IFC File")
    schema: StringProperty(name="Schema")
    status: StringProperty(name="Status")
    file_size: IntProperty(name="File Size", min=0)


class CDEExportItem(PropertyGroup):
    export_id: StringProperty(name="Export ID")
    asset_global_id: StringProperty(name="Asset Global ID")
    source_ifc_file_id: StringProperty(name="Source IFC File ID")
    status: StringProperty(name="Status")
    filename: StringProperty(name="Artifact Filename")
    file_size: IntProperty(name="Artifact Size", min=0)
    created_date: StringProperty(name="Created")
    error_message: StringProperty(name="Error")


class CDEProperties(PropertyGroup):
    base_url: StringProperty(
        name="CDE URL", default="http://cde.certi.api.br:8080",
        description="Base URL of the CDE API",
    )
    client_id: StringProperty(name="Client ID")
    client_secret: StringProperty(name="Client Secret", subtype="PASSWORD")
    connection_status: StringProperty(name="Connection", default="Disconnected")
    operation_status: StringProperty(name="Operation")
    projects: CollectionProperty(type=CDEProjectItem)
    project_index: IntProperty(default=-1)
    assets: CollectionProperty(type=CDEAssetItem)
    asset_index: IntProperty(default=-1)
    ifc_files: CollectionProperty(type=CDEIfcFileItem)
    ifc_file_index: IntProperty(default=-1, update=_clear_selected_ifc_export)
    exports: CollectionProperty(type=CDEExportItem)
    export_index: IntProperty(default=-1)
