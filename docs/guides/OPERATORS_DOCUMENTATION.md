# Operators: modules/*/operators.py

## Overview

Blender operators are distributed by functional domain inside `modules/`. Each
domain has its own `operators.py` with the business logic for that part of the
Add-on.

| Module | Responsibility |
|--------|----------------|
| `modules/common/operators.py` | Shared utilities, tree expansion, object selection, labels, and error popups |
| `modules/dictionary/operators.py` | bSDD dictionary and IDS operators |
| `modules/decomposition/operators.py` | IFC decomposition loading, selection, export, movement, and ordering |
| `modules/catalog/operators.py` | Catalog types, quantities, LI mapping, layer reports, and LI export |
| `modules/connections/operators.py` | IFC connection creation and removal |
| `modules/props/operators.py` | IFC property editing, document handling, tables, and charts |
| `modules/settings/operators.py` | IFC viewport labels and decomposition-view configuration |
| `modules/analysis/operators.py` | Viewport analysis coloring and reset |

All operator classes are registered centrally through `modules/__init__.py` and
`get_classes()`.

## modules/common/operators.py

Shared utility functions and operators used by multiple modules.

### Functions

| Function | Description |
|----------|-------------|
| `_pset_name_variants(pset_name)` | Builds possible Pset name variants for lookup |
| `_get_ifc_label_value(entity, field_name)` | Reads an attribute or `Pset.Property` for viewport labels |
| `_draw_ifc_label()` | Draws IFC labels in the 3D Viewport |
| `register_ifc_label_overlay()` | Registers the viewport label draw handler |
| `unregister_ifc_label_overlay()` | Removes the viewport label draw handler |
| `reorder_element(context, index, chg)` | Reorders nested IFC elements |
| `_open_in_browser(url)` | Opens a URL or file URI in the browser/OS |
| `get_options(self, context)` | EnumProperty callback for dynamic items |

### Operators

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_expand_tree` | `element.expand_tree` | Expands one tree item |
| `Operator_contract_tree` | `element.contract_tree` | Collapses one tree item |
| `ErrorMessage` | `og.error_message` | Displays an error popup |
| `Operator_select_object` | `element.select_object` | Selects an IFC object in Blender |
| `Operator_common_set_tree_expansion` | `common.set_tree_expansion` | Expands or collapses the decomposition tree |

### PropertyGroup

- `Columns`: `name` (`StringProperty`) and `selected` (`BoolProperty`) for chart
  column selection.

## modules/dictionary/operators.py

Operators for bSDD integration and IDS export.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_clear_properties` | `object.clear_prop` | Clears the selected property list |
| `Operator_assign_all` | `object.assign_all` | Selects all properties |
| `Operator_unassign_all` | `object.unassign_all` | Clears all property selections |
| `Operator_get_properties` | `bsdd.get_prop` | Fetches bSDD properties |
| `Operator_uri` | `object.uri` | Opens a URI in the browser |
| `Operator_get_classes` | `bsdd.get_class` | Fetches bSDD classes |
| `Operator_add_properties` | `object.add_prop` | Adds Pset templates from bSDD metadata |
| `Operator_get_prop_info` | `property.get_prop_info` | Fetches property metadata |
| `Operator_get_class_info` | `bsdd.get_class_info` | Fetches class metadata |
| `Operator_get_class_prop` | `bsdd.get_class_prop` | Fetches class properties |
| `Operator_export_ids` | `ids.export` | Exports an IDS XML file |

Dependencies:

- `tqdm`: progress bars.
- `ifctester.ids`: IDS validation/export support.
- `data.bsdd`: bSDD client.
- `data.catalog`: property templates.
- `data.ifc_utils`: hierarchy and property helpers.

## modules/decomposition/operators.py

Operators for IFC decomposition views.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_decomposition_load` | `decomposition.load` | Loads the IFC decomposition tree |
| `Operator_decomposition_export` | `decomposition.export_tree` | Exports the current decomposition tree to `.xlsx` |
| `Operator_decomposition_select_element` | `decomposition.select_element` | Selects one element |
| `Operator_decomposition_select_components` | `decomposition.select_components` | Selects an element and its children recursively |

Dependencies:

- `data.tree`: `load_contained_elements_by_decomposition()`,
  `refresh_tree()`, and tree drawing/selection helpers.

## modules/catalog/operators.py

Operators for IFC product type catalogs, quantities, layer reports, and LI
Mapping.

### LI Mapping Operators

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_load_li_mapping` | `catag.load_li_mapping` | Loads `resources/li_mapping.json` into `scene.og_props` |
| `Operator_save_li_mapping` | `catag.save_li_mapping` | Saves the UI state back to `resources/li_mapping.json` |
| `Operator_add_li_mapping_column` | `catag.add_li_mapping_column` | Adds one LI column |
| `Operator_remove_li_mapping_column` | `catag.remove_li_mapping_column` | Removes the selected LI column |
| `Operator_li_mapping_pick_property` | `catag.li_mapping_pick_property` | Copies the selected bSDD Pset/property into the selected column |
| `Operator_add_li_mapping_source_item` | `catag.add_li_mapping_source_item` | Adds an extra `source` key/value field |
| `Operator_remove_li_mapping_source_item` | `catag.remove_li_mapping_source_item` | Removes the selected extra `source` field |
| `Operator_add_li_support_table_row` | `catag.add_li_support_table_row` | Adds a row to a support table |
| `Operator_remove_li_support_table_row` | `catag.remove_li_support_table_row` | Removes a support-table row |
| `Operator_export_li` | `catag.export_li` | Exports the Item List to `.xlsx` |

### Catalog Operators

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_load_products` | `catag.load_products` | Loads `IfcTypeProduct` entities grouped by `ElementType` |
| `Operator_catalog_show_layers` | `catag.show_layers` | Generates and opens the HTML layer report |
| `Operator_catalog_select_layer` | `catag.select_layer` | Selects a layer/component object |
| `Operator_catalog_select_elements` | `catag.select_elements` | Selects all instances of a type |
| `Operator_export_qtds` | `catag.export_qtds` | Exports type quantities to `.xlsx` |

### LI Mapping Helper Functions

| Function | Description |
|----------|-------------|
| `_get_li_mapping_path()` | Returns the mapping JSON path |
| `_load_li_mapping_into_props(props)` | Loads JSON columns and support tables into UI collections |
| `_save_li_mapping_from_props(props)` | Writes UI collections back to JSON |
| `_build_source_from_column(column)` | Builds the JSON `source` object from guided and extra fields |
| `_resolve_column_value(...)` | Resolves one exported cell value |
| `_build_li_rows(model, mapping_data)` | Builds all exported Item List rows |
| `_resolve_ifc_quantity(...)` | Resolves count or length quantities |
| `_resolve_computed(...)` | Resolves computed values and templates |
| `_render_template(...)` | Replaces attribute and Pset placeholders |

Dependencies:

- `data.catalog`: catalog lookup and IFC import helpers.
- `data.ifc_utils`: hierarchy, products, and units.
- `data.tree`: type refresh.
- `pandas` and `openpyxl`: spreadsheet export.
- `ifcopenshell`: IFC traversal and property reading.

## modules/connections/operators.py

Operators for IFC connection management.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_disconnect` | `conn.disconnect` | Removes an IFC connection relationship |

Pattern:

- Supports review and removal of existing IFC connection relationships.

## modules/props/operators.py

Operators for IFC property editing, document handling, table display, and chart
generation.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_props_load` | `props.load_properties` | Loads properties for the active object |
| `Operator_props_expand` | `props.expand` | Toggles Pset expansion |
| `Operator_docs_expand` | `docs.expand` | Toggles the document section |
| `Operator_props_graph` | `props.graph` | Generates a matplotlib chart from table/CSV data |
| `Operator_props_invert` | `props.invert` | Inverts X/Y axes in graph settings |
| `Operator_document_edit` | `props.doc_edit` | Edits IFC document references |
| `Operator_document_load` | `props.load_doc` | Opens a file picker for document paths |
| `Operator_document_open` | `props.open_doc` | Opens a document in the browser/OS |
| `Operator_show_table` | `props.show_table` | Toggles table visibility |

Analysis libraries:

- `pandas`: tabular data processing.
- `matplotlib`: 2D chart generation.
- `numpy`: vectorized operations.
- `scipy.interpolate`: curve interpolation.

Pattern:

- Uses `invoke_props_dialog` for chart configuration.
- Uses `Columns` collections for selecting chart columns.

## modules/settings/operators.py

Operators for viewport IFC labels and decomposition-view configuration.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_add_ifc_label_attr` | `settings.add_ifc_label_attr` | Adds an IFC attribute label field |
| `Operator_add_ifc_label_property` | `settings.add_ifc_label_property` | Adds the selected `Pset.Property` label field |
| `Operator_remove_ifc_label_attr` | `settings.remove_ifc_label_attr` | Removes a label field |
| `Operator_load_decomposition_views` | `settings.load_decomposition_views` | Loads views from `resources/decomposition_view.json` |
| `Operator_save_decomposition_views` | `settings.save_decomposition_views` | Validates and saves views |
| `Operator_reset_decomposition_views` | `settings.reset_decomposition_views` | Loads default views into the UI |
| `Operator_add_decomposition_view` | `settings.add_decomposition_view` | Adds a new decomposition view |
| `Operator_duplicate_decomposition_view` | `settings.duplicate_decomposition_view` | Duplicates the selected view |
| `Operator_remove_decomposition_view` | `settings.remove_decomposition_view` | Removes the selected view |
| `Operator_add_decomposition_relation` | `settings.add_decomposition_relation` | Adds a relation to the selected view |
| `Operator_remove_decomposition_relation` | `settings.remove_decomposition_relation` | Removes the selected relation |
| `Operator_export_config_profile` | `settings.export_config_profile` | Exports editable settings to a portable JSON profile |
| `Operator_import_config_profile` | `settings.import_config_profile` | Imports a portable JSON profile and refreshes the UI |

Dependencies:

- `data.decomposition_views`: normalization, defaults, validation, and saving.
- `data.config_profile`: portable profile validation, reading, and writing.
- `modules.catalog.operators`: LI mapping payload serialization.

## modules/analysis/operators.py

Operators for coloring the 3D Viewport based on IFC property values.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `Operator_analysis_apply_colors` | `analysis.apply_colors` | Applies analysis colors and legend entries |
| `Operator_analysis_reset_colors` | `analysis.reset_colors` | Restores original object colors |

Dependencies:

- `modules/analysis/service.py`: value collection, validation, color palettes,
  gradients, legend entries, and reset behavior.

## Typical Flow

```text
1. User selects an IFC object or clicks a panel button
        |
2. Operator runs, for example bsdd.get_class or props.load_properties
        |
3. Authentication is checked when the operation requires editor access
        |
4. Data is extracted through ifcopenshell and Bonsai
        |
5. pandas/numpy/scipy process tabular or numeric data when needed
        |
6. data.ifc_utils and data.tree build or refresh collections
        |
7. modules/og_properties.py state is updated
        |
8. modules/*/panels.py redraws the UI
```

## Expected bSDD Class JSON Shape

```json
{
  "code": "001",
  "name": "Flexible Pipe",
  "descriptionPart": "Description",
  "uri": "http://bsdd.buildingsmart.org/...",
  "classType": "IfcPipeSegmentFlexible",
  "children": [
    {
      "code": "001.001",
      "name": "Tensioner"
    }
  ]
}
```

## Debugging

### Print Classes

```python
props = context.scene.og_props
for classe in props.classes:
    print(f"{classe.name} (level: {classe.level})")
```

### Inspect IFC Properties

```python
import ifcopenshell.util.element as element

element_obj = ifc_file[123]
props_dict = element.get_psets(element_obj)
```

## Integration with Other Packages

- `data/`: provides `bSDD`, `Catalog`, `tree`, `ifc_utils`, and decomposition
  view helpers.
- `modules/*/properties.py` and `modules/og_properties.py`: define
  `Class_info`, `Class_type`, `OG_Properties`, LI mapping structures, and other
  UI data containers.
- `modules/*/panels.py`: calls operators from UI buttons and renders the
  resulting state.
- Root `__init__.py`: registers all operators for Blender.
