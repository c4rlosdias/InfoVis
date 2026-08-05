# Properties: modules/*/properties.py and modules/og_properties.py

## Overview

Custom Blender `PropertyGroup` classes are distributed across the domain modules
inside `modules/`. Each domain module defines its own PropertyGroups in
`properties.py`, and the central `OG_Properties` aggregator lives in
`modules/og_properties.py`.

| Module | Responsibility |
|--------|----------------|
| `modules/dictionary/properties.py` | bSDD classes, class properties, and basic IFC property entries |
| `modules/decomposition/properties.py` | Decomposition tree containers |
| `modules/catalog/properties.py` | Catalog types, layers, LI mapping columns, LI source items, and support tables |
| `modules/props/properties.py` | IFC property values, enumerations, Psets, documents, and graph settings |
| `modules/analysis/properties.py` | Analysis legend entries |
| `modules/cde/properties.py` | Runtime CDE credentials, status, projects, assets, submissions, and exports |
| `modules/og_properties.py` | `OG_Properties`, decomposition-view settings, IFC labels, and callbacks |

## modules/dictionary/properties.py

Defines PropertyGroups related to bSDD dictionaries.

### `Ifc_properties`

Basic IFC dictionary/property entry.

```python
class Ifc_properties(PropertyGroup):
    name        : StringProperty(name='name')
    code        : StringProperty(name='code')
    description : StringProperty(name='description')
    uri         : StringProperty(name="uri")
    is_selected : BoolProperty(name="is selected", default=True)
```

### `Class_info`

bSDD class information with tree support.

| Field | Type | Description |
|-------|------|-------------|
| `code` | String | Class code |
| `name` | String | Display name |
| `description` | String | Detailed description |
| `uri` | String | Unique bSDD identifier |
| `propertyset` | String | Property set name |
| `has_children` | Bool | Whether the class has subclasses |
| `is_hidden` | Bool | Whether the item is hidden in the UI |
| `is_expanded` | Bool | Whether the item is expanded in the UI |
| `index` | Int | Sequential index |
| `parent` | String | Parent class name |
| `level` | Int | Tree depth |
| `type` | String | IFC class type |

### `Class_prop_info`

Relationship between a bSDD class and one of its properties.

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Property name |
| `uri` | String | Property URI |
| `datatype` | String | Data type |
| `units` | String | Units |
| `propertyset` | String | Property set |
| `description` | String | Description |
| `definition` | String | Definition |

## modules/decomposition/properties.py

### `Container`

Tree item for spatial, decomposition, grouping, or assignment views.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Int | IFC element ID |
| `name` | String | Element name |
| `object_type` | String | IFC `ObjectType` |
| `type` | String | Element or relationship type |
| `has_children` | Bool | Whether the item has child nodes |
| `is_hidden` | Bool | Whether the item is hidden in the UI |
| `is_expanded` | Bool | Whether the item is expanded in the UI |
| `is_selected` | Bool | Selection state |
| `level` | Int | Tree depth |
| `index` | Int | Sequential index |
| `parent` | String | Parent identifier |
| `is_nested` | Bool | Whether the relation is nesting-based |

## modules/catalog/properties.py

### `Class_type`

IFC product type item used by the catalog panel.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Int | IFC entity ID |
| `tag` | String | Element tag |
| `name` | String | Type name |
| `description` | String | Type description |
| `element_type` | String | IFC `ElementType` |
| `has_children` | Bool | Tree state |
| `is_hidden` | Bool | Tree visibility |
| `is_expanded` | Bool | Expanded state |
| `index` | Int | Sequential index |
| `parent` | String | Parent item |
| `level` | Int | Tree level |
| `qtde` | Float | Quantity for this type |
| `unit` | String | Quantity unit |

### `Layer`

Layer or component item for product-type reports.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Int | IFC entity ID |
| `name` | String | Layer name |
| `description` | String | Layer description |

### `LIMappingSourceItem`

Extra `source` key/value pair for one LI mapping column.

| Field | Type | Description |
|-------|------|-------------|
| `key` | String | Source key |
| `value` | String | Source value as text or JSON |

### `LISupportTableRow`

One row inside a LI support table.

| Field | Type | Description |
|-------|------|-------------|
| `key` | String | Lookup key |
| `value` | String | Lookup value as text or JSON |

### `LISupportTable`

Editable support table loaded from `resources/li_mapping.json`.

| Field | Type | Description |
|-------|------|-------------|
| `table_name` | String | Top-level JSON table key |
| `description` | String | `_comment` saved in the table |
| `rows` | Collection[`LISupportTableRow`] | Table rows |
| `active_row_index` | Int | Active row index |

### `LIMappingColumn`

Editable LI mapping column.

| Field | Type | Description |
|-------|------|-------------|
| `column_name` | String | Exported Excel column name |
| `source_type` | Enum | Mapping source type |
| `notes` | String | Maintenance notes |
| `source_ifc_class` | String | Guided `ifc_class` metadata |
| `source_level` | String | Spatial class or aggregation level |
| `source_attribute` | String | IFC attribute |
| `source_fallback_attribute` | String | Fallback IFC attribute |
| `source_pset` | String | Pset name |
| `source_property` | String | Property name |
| `source_mapping_table` | String | Support table name |
| `source_quantity_mode` | Enum | `mapping`, `count`, or `length` |
| `source_selected_by` | String | Previously calculated column name |
| `source_template_table` | String | Template support table |
| `source_derived_from` | String | Base column for computed methods |
| `source_method` | String | Computed method |
| `source_format` | String | Formatting metadata |
| `source_allowed_values` | String | Allowed values metadata |
| `source_items` | Collection[`LIMappingSourceItem`] | Extra source fields |
| `picker_discipline` | Enum | bSDD picker discipline |
| `picker_object_type` | Enum | bSDD picker element |
| `picker_pset` | Enum | bSDD picker Pset |
| `picker_property` | Enum | bSDD picker property |

## modules/props/properties.py

### `Enumeration_values`

Typed value container for enumerated IFC property values.

| Field | Type | Description |
|-------|------|-------------|
| `enumerated` | Bool | Whether this is an enumerated value |
| `valuestr` | String | String value |
| `valueint` | Int | Integer value |
| `valuefloat` | Float | Float value |
| `valuebool` | Bool | Boolean value |
| `datatype` | String | Data type |
| `type_value` | String | Value type marker |

### `Property_info`

Metadata and value for one IFC property.

| Field | Type | Description |
|-------|------|-------------|
| `index` | Int | Property index |
| `name` | String | Property name |
| `description` | String | Property description |
| `valuestr/int/float/bool` | Mixed | Typed property values |
| `type_value` | String | Value type marker |
| `type_prop` | String | Property type marker |
| `n_columns` | Int | Table column count |
| `n_rows` | Int | Table row count |
| `datatype` | String | Data type |
| `enumerations` | Collection[`Enumeration_values`] | Enumerated values |

### `Documents`

IFC document references.

| Field | Type | Description |
|-------|------|-------------|
| `index` | Int | Document index |
| `identification` | String | Document ID |
| `location` | String | Path or URL |
| `name` | String | Document name |

### `Pset_info`

Property set with nested property and document collections.

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Pset name |
| `description` | String | Pset description |
| `is_a` | String | Source entity kind |
| `id_obj` | Int | IFC object ID |
| `index` | Int | Pset index |
| `props` | Collection[`Property_info`] | Pset properties |
| `is_expanded` | Bool | Expanded state |
| `min_x/max_x/min_y/max_y` | Float | Chart bounds |
| `mult_x/mult_y` | Int | Chart grid intervals |
| `interpoled` | Bool | Chart interpolation flag |
| `has_document` | Bool | Whether documents are present |
| `docs_expanded` | Bool | Document section state |
| `document` | String | Current document field |
| `documents` | Collection[`Documents`] | Document references |

## modules/analysis/properties.py

### `AnalysisLegendItem`

Legend item shown after analysis coloring.

| Field | Type | Description |
|-------|------|-------------|
| `label` | String | Legend label |
| `color` | FloatVector | RGBA color swatch |

## modules/cde/properties.py

CDE properties are attached to `WindowManager.cde_props` because credentials,
JWT session status, and remote query results are runtime UI state rather than
IFC model data.

| Class | Main fields | Purpose |
|-------|-------------|---------|
| `CDEProjectItem` | `local_id`, `global_id`, `name`, `description`, `assets_count` | One CDE project row |
| `CDEAssetItem` | `local_id`, `global_id`, `name`, `asset_type` | One asset row |
| `CDEIfcFileItem` | `local_id`, `global_id`, `asset_global_id`, `name`, `schema`, `status`, `file_size` | One IFC metadata row |
| `CDEExportItem` | `export_id`, `asset_global_id`, `source_ifc_file_id`, `status`, `filename`, `file_size`, `created_date`, `error_message` | One generated export row |
| `CDEProperties` | `base_url`, credentials, status fields, collections, active indices | Complete panel runtime state |

`client_secret` uses Blender's `PASSWORD` subtype and is cleared immediately
after successful authentication. Access and refresh tokens are not RNA
properties; they remain inside the in-memory `CDEClient`.

## modules/og_properties.py

### Decomposition View Settings

`modules/og_properties.py` defines two configuration PropertyGroups used by the
settings panel.

| Class | Purpose |
|-------|---------|
| `IFC_Label_Attribute` | One IFC label field and optional display name |
| `Decomposition_View_Relation` | One IFC relationship rule for a decomposition view |
| `Decomposition_View` | One named decomposition view with root class and relations |

### Update Callbacks

| Callback | Description |
|----------|-------------|
| `update_tree_type(self, context)` | Refreshes the decomposition tree type |
| `get_dictionaries(self, context)` | Dynamically loads bSDD dictionaries |
| `active_prop_changed(self, context)` | Clears data when the active property changes |
| `active_class_changed(self, context)` | Resets class state when the active class changes |
| `active_product_changed(self, context)` | Marks product data as not loaded |
| `active_type_changed(self, context)` | Marks type data as not loaded |
| `active_element_changed(self, context)` | Updates state when the active element changes |

### `OG_Properties`

Main PropertyGroup registered on `bpy.types.Scene`. It contains the central UI
state for the Add-on.

Dictionary state:

- `dictionary`
- `ifc_prop`
- `class_info`
- `classes`, `classes_shown`
- `class_prop_info`
- class metadata fields and load flags

Decomposition state:

- `tree_type`
- `elements_containers`, `containers_show`
- `elements_tree`, `elements_tree_show`
- `decomposition_views`
- active decomposition view and relation indices

Catalog and LI state:

- `products`, `products_show`
- `types`, `types_show`
- `layers`
- active product, type, and layer indices
- `li_mapping_schema_version`
- `li_mapping_description`
- `li_mapping_reference_sheet`
- `li_mapping_columns`
- `li_support_tables`
- active LI mapping and support-table indices
- `li_mapping_loaded`

Properties and documents state:

- `prop_metadata`
- active Pset and property indices
- graph settings
- `documents`
- `show_table`
- `show_description`

Analysis state:

- `analysis_discipline`
- `analysis_object_type`
- `analysis_pset`
- `analysis_property`
- `analysis_color_mode`
- `analysis_value`
- `analysis_range_min`, `analysis_range_max`
- `analysis_status`
- `analysis_legend`

Viewport label state:

- `show_ifc_label`
- `ifc_label_attributes`
- `label_offset_x`
- `label_offset_y`

Connections state:

- connection collections and selected objects managed by connection operators

## Relationship Between PropertyGroups

```text
scene.og_props (OG_Properties)
+-- classes: CollectionProperty[Class_info]
+-- classes_shown: CollectionProperty[Class_info]
+-- class_prop_info: CollectionProperty[Class_prop_info]
+-- types: CollectionProperty[Class_type]
+-- types_show: CollectionProperty[Class_type]
+-- products: CollectionProperty[Class_info]
+-- products_show: CollectionProperty[Class_info]
+-- elements_containers: CollectionProperty[Container]
+-- containers_show: CollectionProperty[Container]
+-- decomposition_views: CollectionProperty[Decomposition_View]
+-- prop_metadata: CollectionProperty[Pset_info]
|   +-- [i].props: CollectionProperty[Property_info]
|   |   +-- [j].enumerations: CollectionProperty[Enumeration_values]
|   +-- [i].documents: CollectionProperty[Documents]
+-- li_mapping_columns: CollectionProperty[LIMappingColumn]
|   +-- [i].source_items: CollectionProperty[LIMappingSourceItem]
+-- li_support_tables: CollectionProperty[LISupportTable]
|   +-- [i].rows: CollectionProperty[LISupportTableRow]
+-- analysis_legend: CollectionProperty[AnalysisLegendItem]
+-- ifc_label_attributes: CollectionProperty[IFC_Label_Attribute]
```

## Update Flow

```text
User interacts with UI
        |
        v
Property changes, for example active_class_index
        |
        v
Callback runs
        |
        v
Loaded flags or active collections are reset
        |
        v
tree.refresh_*() or a domain-specific refresh runs
        |
        v
Visible collection is repopulated
        |
        v
Panel redraws with updated data
```

## Registering PropertyGroups

In `modules/__init__.py`, `get_classes()` returns all classes in dependency
order. The root `__init__.py` registers them:

```python
from .modules import get_classes
from .modules.og_properties import OG_Properties

classes = [Prefs] + get_classes()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.og_props = PointerProperty(type=OG_Properties)

def unregister():
    del bpy.types.Scene.og_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

## Integration with Other Modules

- `data/`: uses PropertyGroups to store loaded IFC and bSDD data.
- `modules/*/operators.py`: reads and modifies properties during operations.
- `modules/*/panels.py`: renders PropertyGroups in the UI through labels,
  boxes, and `template_list`.
- `modules/__init__.py`: returns all classes in registration order.
- Root `__init__.py`: registers classes and attaches `Scene.og_props`.
