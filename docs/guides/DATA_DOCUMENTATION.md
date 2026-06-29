# Package: data/

## Overview

The `data/` package manages shared data access, callbacks, event handling, and
IFC/bSDD integration features. It coordinates synchronization between the
Blender scene, Bonsai's active IFC model, dictionary resources, and the
application data structures exposed through `scene.og_props`.

The package is organized into these main modules:

| Module | Responsibility |
|--------|----------------|
| `bsdd.py` | REST client for the buildingSMART Data Dictionary |
| `bsdd_dictionary.py` | Local dictionary helpers for analysis and LI property pickers |
| `catalog.py` | IFC import helpers, catalog lookup, and property templates |
| `cde.py` | CDE API mock/stub for future integration |
| `decomposition_views.py` | Decomposition-view defaults, validation, loading, and saving |
| `tree.py` | Tree loading, refresh functions, callbacks, and UI tree helpers |
| `ifc_utils.py` | IFC utilities for properties, units, visibility, hierarchy, and connections |

`data/__init__.py` re-exports the main submodules:

```python
from .bsdd import *
from .catalog import *
from .cde import *
from .tree import *
from .ifc_utils import *
```

## Module: bsdd.py

### Class `bSDD`

Static client, implemented with `@classmethod`, for the buildingSMART Data
Dictionary.

Class variables:

- `data_dic`: available dictionaries.
- `data_info_prop`: property metadata.
- `data_class`: class data.
- `data_prop`: property data.
- `endpoint`: base API URL.
- `uri`: active dictionary URI.
- `is_loaded`: loaded-state flag.

Methods:

| Method | Description |
|--------|-------------|
| `load_dictionaries()` | Fetches dictionary versions from the bSDD server |
| `load_classes(version, use_nested)` | Fetches classes for a dictionary version |
| `load_properties(version)` | Fetches properties for a dictionary version |
| `get_class(uri, include_properties)` | Fetches one specific class |
| `get_class_prop(uri)` | Fetches the properties of a class |
| `get_property(uri)` | Fetches one individual property |

Example:

```python
from data.bsdd import bSDD

if not bSDD.is_loaded:
    bSDD.load_dictionaries()

bSDD.load_classes(version_uri, use_nested=True)
```

## Module: bsdd_dictionary.py

`bsdd_dictionary.py` reads local dictionary JSON resources used by the analysis
panel and by the LI Mapping bSDD picker.

Main responsibilities:

- locate dictionary files in `resources/`;
- normalize object-type, Pset, and property entries;
- build enum items for Blender UI fields;
- provide friendly labels while preserving technical names.

Key functions:

| Function | Description |
|----------|-------------|
| `get_dictionary(discipline_key)` | Loads the selected local dictionary |
| `get_object_type_entry(discipline_key, object_type_key)` | Returns metadata for one object type |
| `get_pset_entry(discipline_key, object_type_key, pset_key)` | Returns metadata for one Pset |
| `get_object_type_items(discipline_key)` | Builds Blender enum items for object types |
| `get_pset_items(discipline_key, object_type_key)` | Builds Blender enum items for Psets |
| `get_property_items(discipline_key, object_type_key, pset_key)` | Builds Blender enum items for properties |

Relevant resource files:

```text
resources/subsea_flexible_pipes_2.1_completo.json
resources/subsea_rigid_pipes_1.0_completo.json
```

## Module: catalog.py

### Class `Import_ifc`

Imports IFC type elements into Blender through Bonsai.

| Method | Description |
|--------|-------------|
| `import_type_from_ifc()` | Imports an element type |
| `import_materials()` | Imports materials |
| `import_styles()` | Imports visual styles |
| `import_material_styles()` | Imports material styles |

### Class `Catalog`

Reads `resources/ifc_types.json`.

| Method | Description |
|--------|-------------|
| `get_ifc_type()` | Returns the IFC type catalog |

### Class `PropTempl`

Manages IFC property set templates, including `EPset_OG.ifc`.

| Method | Description |
|--------|-------------|
| `get_template()` | Gets an existing template |
| `get_prop()` | Gets a template property |
| `add_pset_template(metadata)` | Creates or edits a Pset template from bSDD metadata |

Pattern: all classes use `@classmethod`.

## Module: cde.py

### Class `CDE_Api`

Stub/mock CDE API for future Common Data Environment integration.

```python
cde = CDE_Api(endpoint="https://api.cde.example.com")
projects = cde.get_projects()   # real HTTP call
contracts = cde.get_contracts() # mocked data
assets = cde.get_assets()       # mocked data
inventory = cde.get_inventory() # mocked data
```

Status: placeholder for a future real CDE integration.

## Module: decomposition_views.py

`decomposition_views.py` owns the decomposition view configuration used by the
`Settings` and `Decompositions` panels.

Configuration file:

```text
resources/decomposition_view.json
```

Default views:

| ID | Label | Root class | Main relations |
|----|-------|------------|----------------|
| `assets` | `Assets` | `IfcProject` | group assignment, spatial containment, aggregation, nesting |
| `contracts` | `Contracts` | `IfcProjectOrder` | control assignment, group assignment, aggregation, nesting |
| `inventory` | `Inventory` | `IfcInventory` | group assignment |

Key functions:

| Function | Description |
|----------|-------------|
| `get_config_path()` | Returns the JSON configuration path |
| `get_preset(key)` | Returns a relation preset |
| `normalize_relation(relation)` | Normalizes one relation definition |
| `normalize_view(view)` | Normalizes one decomposition view |
| `normalize_payload(payload)` | Normalizes a full payload |
| `load_views()` | Loads configured views from disk |
| `default_views()` | Returns built-in default views |
| `payload_from_collection(collection)` | Converts Blender UI collection data to JSON payload |
| `validate_payload(payload)` | Validates views before saving |
| `save_payload(payload)` | Writes the normalized payload to disk |

## Module: tree.py

### Callback Functions

#### `call_back()`

Simple callback that triggers property loading.

```python
def call_back():
    bpy.ops.props.load_properties()
```

Triggered by msgbus when the active object changes.

#### `on_active_object_change(scene)`

Detects active-object changes and updates properties.

```python
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    if obj != last_active:
        last_active = obj
        bpy.ops.props.load_properties()
```

Triggered by `bpy.app.handlers.depsgraph_update_post`.

### Refresh Functions

The refresh functions follow the same pattern:

```text
1. Get props = context.scene.og_props
2. Clear the visible collection
3. Iterate over the complete collection
4. Copy non-hidden items into the visible collection
```

| Function | Source to destination |
|----------|----------------------|
| `refresh_classes(context)` | `classes` to `classes_shown` |
| `refresh_products(context)` | `products` to `products_show` |
| `refresh_types(context)` | `types` to `types_show` |
| `refresh_container(context)` | `elements_containers` to `containers_show` |
| `refresh_tree(context, property)` | Generic refresh for a collection pair |
| `refresh_layers(context)` | Refreshes the layer collection |
| `refresh_tree_containers(context)` | Refreshes decomposition tree containers |

### Decomposition Functions

#### `load_contained_elements_by_decomposition(container, view_id, name_props, context)`

Recursively loads the IFC decomposition for the selected view into Blender
collections.

Uses configured relationships such as:

- `IfcRelAssignsToGroup`
- `IfcRelContainedInSpatialStructure`
- `IfcRelAggregates`
- `IfcRelNests`
- `IfcRelAssignsToControl`

#### `draw_tree(layout, item, operators, attributes, property, only_children)`

Draws a hierarchical tree in the Blender UI.

#### `move_to_assembly(parent, children, type)`

Moves IFC elements through the nesting or aggregation APIs.

## Module: ifc_utils.py

`ifc_utils.py` is the main utility module for IFC property handling, visibility,
hierarchy construction, units, and connections.

### Property Type Functions

| Function | Description |
|----------|-------------|
| `set_prop_type(prop, value_prop)` | Polymorphic setter for string, integer, float, and boolean values |
| `get_prop_type(prop)` | Polymorphic getter |

### Unit Functions

| Function | Description |
|----------|-------------|
| `get_unit_symbol(unit)` | Returns the IFC unit symbol |
| `get_unit(ifc_obj, pset_name, prop_name)` | Resolves the unit of a property |

### IFC Property Functions

| Function | Description |
|----------|-------------|
| `get_property(ifc_obj, pset_name, prop_name)` | Gets or creates a property set |
| `get_pset(ifc_obj, pset_name)` | Gets an existing property set |
| `get_pset_items(pset)` | Converts Pset content into UI-friendly items |
| `set_properties(props, ifc_obj, is_a, i)` | Loads all properties, including tables, enums, lists, and documents |
| `refresh_props(context)` | Reloads properties for the active object |

### Visibility Functions

| Function | Description |
|----------|-------------|
| `set_hide_class(context, index, is_hidden)` | Hides or shows subclasses recursively |
| `set_hide_product(context, index, is_hidden)` | Hides or shows subproducts recursively |

Visibility algorithm:

```text
For each class after the selected index:
  If its level is deeper than the selected item's level:
    Apply the is_hidden state
  If its level is equal to or above the selected item's level:
    Stop
```

### Hierarchy Construction Functions

| Function | Description |
|----------|-------------|
| `build_classes(context, classe, c, level, parent, hide)` | Builds the class hierarchy in `props.classes` |
| `build_products(context, classe, c, level, parent, hide, children)` | Builds the product/type hierarchy in `props.types` |

Example input for `build_classes`:

```python
classe_dict = {
    "code": "001",
    "name": "Pipe",
    "descriptionPart": "Subsea pipe",
    "uri": "http://bsdd.buildingsmart.org/...",
    "classType": "IfcPipeSegment",
    "children": [...]
}
build_classes(context, classe_dict, 0, 1, "", False)
```

### Connection Functions

| Function | Description |
|----------|-------------|
| `add_connections(obj_a, obj_b, obj_c, connect_type)` | Creates IFC connection relationships |

Supported connection types:

- `IfcRelConnectsPorts`
- `IfcRelConnectsElements`
- `IfcRelConnectsWithRealizingElements`

## Event Flow

```text
User selects a Blender object
        |
        v
msgbus / depsgraph_update_post handler
        |
        v
tree.call_back() or tree.on_active_object_change()
        |
        v
bpy.ops.props.load_properties()
        |
        v
ifc_utils.refresh_props()
        |
        v
tree.refresh_*()
        |
        v
Panels redraw from visible collections
```

## Registering Handlers

In the root `__init__.py`, the Add-on subscribes to object changes during
registration.

```python
bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=owner,
    args=(bpy.context,),
    notify=_data_tree.call_back,
)
```

## Dependencies

### Bonsai and IfcStore Integration

```python
from bonsai.bim.ifc import IfcStore
import bonsai.tool as tool
```

### Data Processing

- `ifcopenshell`: IFC manipulation.
- `numpy`: matrix and numeric operations used by `ifc_utils.py`.
- `pandas`: tabular analysis for property tables, quantities, and exports.

## Best Practices

### Clear Before Populating

```python
props.classes_shown.clear()
for item in data:
    new = props.classes_shown.add()
```

### Check State Before Processing

```python
if props.classes_loaded:
    # use loaded data
else:
    # load required data first
```

### Avoid Callback Loops

```python
self.updating = True
# apply changes
self.updating = False
```

## Integration with Other Packages

- `modules/*/operators.py`: calls `tree.refresh_*()` and `ifc_utils.*` after
  operations.
- `modules/*/panels.py`: displays data from `classes_shown`, `types_show`,
  `containers_show`, and related collections.
- `modules/*/properties.py` and `modules/og_properties.py`: define the
  PropertyGroups manipulated by the data layer.
- Root `__init__.py`: registers handlers through msgbus and connects
  `tree.call_back`.
