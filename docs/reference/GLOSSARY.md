# Glossary and Quick Reference

## Main Terms

**InfoVis**
- Blender add-on for visualizing and enriching IFC data
- name defined in `bl_info` inside `__init__.py`

**Add-on**
- extension loaded by Blender
- registered through Python classes derived from types such as
  `bpy.types.Operator`, `bpy.types.Panel`, and `bpy.types.PropertyGroup`

**Blender**
- host application for the add-on
- provides the Python API, UI, handlers, and `msgbus`

**Context**
- `bpy.context` object
- central access point for the scene, active object, preferences, and UI state

**Bonsai**
- BIM ecosystem used by the project to access IFC data in Blender

## IFC and Integration Terms

**IFC**
- open format for construction data
- used as the basis for reading elements, properties, documents, and
  relationships

**IFC Entity**
- individual entity inside an IFC file
- common examples: `IfcWall`, `IfcPipeSegment`, `IfcDistributionElement`

**bSDD**
- buildingSMART Data Dictionary
- external dictionary queried by `data/bsdd.py`

**GUID / GlobalId**
- unique identifier of an IFC entity

**Pset**
- property set associated with an element

**IDS**
- Information Delivery Specification
- can be exported through operators in the `dictionary` domain

**CDE**
- Common Data Environment
- integration supported by `data/cde.py`

## Internal Project Terms

**PropertyGroup**
- data structure registered in Blender
- defined in `modules/*/properties.py` and aggregated in
  `modules/og_properties.py`

**OG_Properties**
- central state aggregator for the add-on
- available at `context.scene.og_props`

**Operator**
- executable action exposed to the user
- usually located in `modules/*/operators.py`

**Panel**
- visual component in the View3D sidebar
- usually located in `modules/*/panels.py`

**UIList**
- visual list used to display Blender collections with selection and
  interaction

**CollectionProperty**
- typed collection used to store lists inside `PropertyGroup`s

**Handler**
- function registered for Blender events, such as file loading

**msgbus**
- Blender observation mechanism used to react to active-object changes

**AddonPreferences**
- persistent add-on preferences defined in `OilGasAddonPreferences`

## Repository Structure

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- data/
|   |-- bsdd.py
|   |-- bsdd_dictionary.py
|   |-- catalog.py
|   |-- cde.py
|   |-- config_profile.py
|   |-- decomposition_views.py
|   |-- ifc_utils.py
|   `-- tree.py
|-- modules/
|   |-- __init__.py
|   |-- og_properties.py
|   |-- common/
|   |-- dictionary/
|   |-- decomposition/
|   |-- catalog/
|   |-- analysis/
|   |-- connections/
|   |-- props/
|   |-- settings/
|   `-- types/
|-- resources/
|-- libs311/
`-- libs313/
```

## Quick Code Reference

### Access the Main State

```python
props = bpy.context.scene.og_props
print(len(props.classes))
```

### Access Add-on Preferences

```python
prefs = bpy.context.preferences.addons["InfoVis"].preferences
print(prefs.cde_url)
```

If the package was installed with another folder name, the key in
`addons[...]` must match the real package name loaded by Blender.

### Call Common Operators

```python
bpy.ops.bsdd.get_prop()
bpy.ops.props.load_properties()
bpy.ops.og.login()
```

### Add an Item to a Blender Collection

```python
item = props.classes.add()
item.name = "New item"
```

### Check Authentication

```python
import InfoVis.auth as auth
print(auth.is_authenticated())
```

## Code Conventions

### Blender Classes

```python
class Operator_get_properties(bpy.types.Operator):
    ...

class Panel_Properties(bpy.types.Panel):
    ...
```

### `bl_idname`

```python
bl_idname = "bsdd.get_prop"
bl_idname = "props.load_properties"
bl_idname = "og.login"
```

### Helper Functions

```python
refresh_classes()
refresh_props()
build_classes()
```

## Recurring Patterns

**Centralized state**
- panels and operators mainly read and write through `context.scene.og_props`

**Refresh after mutation**
- collection or selection changes are often followed by `refresh_*()` calls in
  `data/tree.py` or `data/ifc_utils.py`

**Centralized registration**
- every new Blender class must be added to `modules/__init__.py`

**Domain separation**
- UI, operators, and data are organized by functional domain in `modules/`

## Quick Debugging

### Blender Python Console

```python
import bpy
import importlib
import InfoVis.auth as auth
from InfoVis.modules import get_classes

props = bpy.context.scene.og_props
print(len(get_classes()))
print(auth.is_authenticated())
print(hasattr(props, "classes"))
```

### Reload a Module

```python
import importlib
import InfoVis.data.bsdd as bsdd

importlib.reload(bsdd)
```

## Common Problems

**Operator does not appear in the UI**
- the class was not added to `modules/__init__.py`
- the file was not reloaded in Blender after the change

**PropertyGroup does not persist**
- the type was not registered before `OG_Properties`
- the property was not correctly attached to the central aggregator or to
  `Scene`

**Blender context error**
- an operator or function was called outside the expected UI or active-object
  context

**Scientific dependency ImportError**
- the Blender environment did not find the bundled libraries or dynamic
  installation outside Windows failed

**Data does not update when selection changes**
- check handlers, the `msgbus` subscription, and `refresh_*()` functions

## External Resources

| Resource | Link |
|----------|------|
| Blender API | https://docs.blender.org/api/current/ |
| IfcOpenShell | https://docs.ifcopenshell.org/ |
| buildingSMART | https://www.buildingsmart.org/ |
| Matplotlib | https://matplotlib.org/ |
| SciPy | https://scipy.org/ |
