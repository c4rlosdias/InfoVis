# InfoVis Development

## Purpose

This guide explains how to prepare the environment, iterate on the add-on, and
package InfoVis releases while staying aligned with the current repository
structure.

## Requirements

- Blender 5.0 or newer
- access to Blender's embedded Python
- Git
- VS Code or another editor with Python support

## Development-Relevant Structure

- `__init__.py`: add-on entry point and class registration
- `modules/`: operators, panels, and domain `PropertyGroup`s
- `data/`: integrations and support logic
- `resources/`: supporting JSON files
- `Example/`: IFC file for manual testing
- `build_release.bat` and `build_release.sh`: packaging scripts

## Environment Setup

### Python Dependencies

`requirements.txt` lists support dependencies for the project. In the Blender
environment, runtime dependencies are bundled in `wheels/` and declared in
`blender_manifest.toml`.

Use Blender's extensions installation flow so these wheel dependencies are
resolved during install.

### Install the Add-on for Local Iteration

Recommended flow:

1. work normally in this repository
2. generate an installable zip with the build script
3. reinstall the zip in Blender whenever changes need validation

Windows:

```powershell
.\build_release.bat dev-local
```

Linux or macOS:

```bash
./build_release.sh dev-local
```

The generated package is written to `releases/dev-local.zip`.

### Install in Blender

1. open Blender
2. go to `Edit > Preferences > Add-ons`
3. click `Install from Disk`
4. select the zip generated in `releases/`
5. enable the `InfoVis` add-on

## Recommended Workflow

1. change code in `modules/`, `data/`, or `resources/`
2. generate a new zip with the build script
3. reinstall or remove and reinstall the add-on in Blender
4. validate affected panels and operators with a real IFC file
5. repeat the cycle until the feature is stable

## Where to Make Each Kind of Change

### New Operator

1. add the class in `modules/<domain>/operators.py`
2. register the class in `modules/__init__.py`
3. expose the action in the appropriate panel when needed
4. use `data/` to encapsulate IFC, bSDD, or CDE access

### New Panel or UIList

1. implement it in `modules/<domain>/panels.py`
2. register it in `modules/__init__.py`
3. read and write state only through `context.scene.og_props` or related
   Blender properties

### New `PropertyGroup`

1. declare the type in the corresponding domain module
2. register the type before `OG_Properties`
3. add the aggregate property in `modules/og_properties.py` when the state is
   shared

### New Integration or Business Rule

Prefer keeping logic out of panel `draw()` methods. If the feature talks to
APIs, IFC files, catalogs, or data transformations, the natural destination is
usually `data/`.

## Practical Project Rules

- keep `modules/__init__.py` as the single source of class registration order
- do not put heavy logic inside `Panel.draw()`
- preserve `OG_Properties` as the shared state between modules
- keep `wheels/` aligned with the dependency list in `blender_manifest.toml`
- test in Blender after any change involving registration, UI, or callbacks

## Manual Validation

Use `Example/C3388.8_UN-31.ifc` as a baseline for manual checks when applicable.

Minimum checklist:

1. the add-on installs and enables without errors
2. the main panels appear in the View3D sidebar
3. object selection updates the properties panel information
4. changed operators run without exceptions in the Blender console
5. affected overlays or lists reflect the new state after refresh

## Debugging in Blender

The Blender Python console can be used for quick checks.

Useful examples:

```python
import bpy
import InfoVis
from InfoVis.modules import get_classes

props = bpy.context.scene.og_props
print(len(get_classes()))
print(hasattr(props, "classes"))
```

If the add-on was installed with another folder name, adjust the import to the
actual package name in the Blender environment.

## Release Process

The build scripts assemble the package in `releases/InfoVis/` and then create a
final zip file.

Packaged content:

- `__init__.py`
- `modules/`
- `data/`
- `wheels/`
- `resources/`

Before publishing a release:

1. confirm the version in `bl_info` inside `__init__.py`
2. validate zip installation in a clean Blender environment
3. confirm that JSON resources and bundled libraries are included
4. record relevant changes in the main documentation

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [guides/OPERATORS_DOCUMENTATION.md](guides/OPERATORS_DOCUMENTATION.md)
- [guides/PANELS_DOCUMENTATION.md](guides/PANELS_DOCUMENTATION.md)
- [guides/PROPERTIES_DOCUMENTATION.md](guides/PROPERTIES_DOCUMENTATION.md)
- [guides/DATA_DOCUMENTATION.md](guides/DATA_DOCUMENTATION.md)
- [reference/GLOSSARY.md](reference/GLOSSARY.md)
