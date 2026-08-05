"""Headless Blender smoke test for the isolated CDE module."""

import importlib.util
import sys
import types
from pathlib import Path

import bpy


ROOT = Path(__file__).parents[1]


def package(name, path):
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


package("InfoVis", ROOT)
package("InfoVis.modules", ROOT / "modules")
package("InfoVis.modules.cde", ROOT / "modules" / "cde")
service = load("InfoVis.modules.cde.service", ROOT / "modules" / "cde" / "service.py")
properties = load("InfoVis.modules.cde.properties", ROOT / "modules" / "cde" / "properties.py")
operators = load("InfoVis.modules.cde.operators", ROOT / "modules" / "cde" / "operators.py")
panels = load("InfoVis.modules.cde.panels", ROOT / "modules" / "cde" / "panels.py")

classes = (
    properties.CDEProjectItem,
    properties.CDEAssetItem,
    properties.CDEIfcFileItem,
    properties.CDEExportItem,
    properties.CDEProperties,
    *operators.CLASSES,
    *panels.CLASSES,
)

for cls in classes:
    bpy.utils.register_class(cls)
bpy.types.WindowManager.cde_props = bpy.props.PointerProperty(type=properties.CDEProperties)

assert bpy.context.window_manager.cde_props.base_url == "http://cde.certi.api.br:8080"
assert hasattr(bpy.context.window_manager.cde_props, "exports")
assert hasattr(bpy.ops.cde, "login")
assert hasattr(bpy.ops.cde, "load_exports")
assert hasattr(bpy.ops.cde, "generate_export")
assert hasattr(bpy.ops.cde, "open_ifc")
print("INFOVIS_CDE_REGISTER_OK")

del bpy.types.WindowManager.cde_props
for cls in reversed(classes):
    bpy.utils.unregister_class(cls)
print("INFOVIS_CDE_UNREGISTER_OK")
