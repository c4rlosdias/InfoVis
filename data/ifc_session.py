"""Single integration point between InfoVis and Bonsai's active IFC session."""

from __future__ import annotations

from typing import Any

import bonsai.tool as _bonsai_tool


def get_model():
    """Return the IFC model currently loaded by Bonsai, or ``None``."""
    return _bonsai_tool.Ifc.get()


def get_path() -> str:
    """Return the absolute path of the IFC model currently loaded by Bonsai."""
    return _bonsai_tool.Ifc.get_path()


def get_entity(obj: Any):
    """Return the IFC entity linked to a Blender object or data-block."""
    return _bonsai_tool.Ifc.get_entity(obj)


def get_object(entity: Any):
    """Return the Blender data-block linked to an IFC entity."""
    return _bonsai_tool.Ifc.get_object(entity)


def get_object_by_identifier(identifier: int | str):
    """Return the Blender data-block linked to an IFC STEP ID or GlobalId."""
    return _bonsai_tool.Ifc.get_object_by_identifier(identifier)


def get_bonsai_data_dir_path(data_dir: str):
    """Return a Bonsai data directory without exposing ``bonsai.tool``."""
    return _bonsai_tool.Blender.get_data_dir_path(data_dir)
