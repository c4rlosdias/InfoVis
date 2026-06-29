# InfoVis Add-on User Guide

This guide explains how to use the InfoVis Add-on in Blender, with a focus on
the panels available in the 3D Viewport sidebar. It is intended for users who
need to inspect, classify, edit, analyze, and export information from IFC
models.

## Overview

InfoVis organizes its tools into Blender sidebar tabs:

| Tab | Panel | Main use |
|-----|-------|----------|
| `InfoVis-Dictionary` | `Subsea Classes` | Browse bSDD dictionaries, classes, and properties; export IDS files |
| `InfoVis-Occurrence` | `Decompositions` | Navigate IFC decomposition views and export the tree |
| `InfoVis-Occurrence` | `Properties` | Read and edit properties, documents, and CSV charts |
| `InfoVis-Occurrence` | `Constructive Type` | Inspect the active object's constructive type and layers |
| `InfoVis-Occurrence` | `Connect Elements` | View, create, and remove IFC connections |
| `InfoVis-Catalog` | `Catalog` | Load product types, quantities, and layer reports |
| `InfoVis-Catalog` | `LI Mapping` | Configure the Item List mapping and export the LI spreadsheet |
| `InfoVis-Analisys` | `Analisys` | Color objects by properties, exact values, or numeric ranges |
| `InfoVis-Settings` | `Settings` | Configure IFC labels and decomposition views |

Open the sidebar with `N` in the 3D Viewport, then select one of the
`InfoVis-*` tabs.

## Prerequisites

Before using panels that read IFC data, load an IFC model into Blender through
the Bonsai/BlenderBIM workflow. InfoVis depends on the active model returned by
Bonsai.

Main requirements:

- Blender 5.0 or newer.
- The `InfoVis` Add-on installed and enabled.
- An open IFC model whenever the action depends on elements, types,
  properties, quantities, documents, or connections.
- Internet access when querying bSDD.
- Authenticated editor permission to change properties, documents,
  connections, aggregations, element order, and other editable IFC content.

## Install and Enable

1. Generate or obtain the InfoVis release `.zip`.
2. In Blender, open `Edit > Preferences > Add-ons`.
3. Click `Install from Disk`.
4. Select the Add-on `.zip`.
5. Enable `InfoVis`.
6. Open or import the IFC file to analyze.
7. In the 3D Viewport, press `N` and open the `InfoVis-*` tabs.

## Editor Authentication

Some actions are visible or editable only after editor login.

To authenticate:

1. Open `Edit > Preferences > Add-ons`.
2. Find the `InfoVis` Add-on.
3. In `Autenticacao para status de editor`, enter the password configured for
   the project.
4. Click `Login`.

While authenticated, InfoVis enables actions such as editing IFC values, editing
documents, creating or removing connections, moving elements in decomposition
trees, and changing element order. Use `Logout` to end the Blender session's
editor access.

## Recommended Quick Workflow

1. Load the IFC model in Blender/Bonsai.
2. Open `InfoVis-Settings > Settings` and click `Load` under
   `Decomposition views`.
3. Open `InfoVis-Occurrence > Decompositions`, choose the `Tree Type`, and
   navigate the tree.
4. Select an element in the tree or in the 3D Viewport.
5. Open `InfoVis-Occurrence > Properties` and click `Load properties`.
6. Use `InfoVis-Catalog > Catalog` to load types and export quantities when
   needed.
7. Use `InfoVis-Catalog > LI Mapping` to review the Item List mapping before
   exporting the LI spreadsheet.
8. Use `InfoVis-Analisys > Analisys` to color the viewport by property, exact
   value, or numeric range.

## InfoVis-Dictionary: Subsea Classes

Use this panel to query bSDD dictionaries and turn dictionary properties into
IFC templates and specification artifacts.

### Load bSDD Classes

1. In `Select Dictionary`, choose the dictionary:
   - `Subsea Flexible Pipes v2.1`
   - `Subsea Rigid Pipelines v1.0`
2. Click `get classes from bSDD`.
3. Browse the class list.
4. Use the URL icon to open a class in the browser.

With a class selected:

- `Get Class Information` loads definition, description, version date, class
  type, and related IFC class.
- `Get Class Properties` lists the properties associated with the class.
- `Export IDS file` exports an `.ids` file with requirements derived from the
  loaded classes and properties.

### Load bSDD Properties

1. Choose the dictionary.
2. Click `get properties from bSDD`.
3. Select or clear properties in the list.
4. Use `Assing all`, `Unassign all`, or `Clear` to control the selection.
5. Select a property and click `Get Property Information` to view metadata,
   units, and related classes.
6. Click `Add selected properties` to generate or add Pset templates from the
   selected properties.

## InfoVis-Occurrence: Decompositions

The `Decompositions` panel shows the IFC decomposition tree according to the
configured view.

### Configure Decomposition Views

Views are read from `resources/decomposition_view.json`. They define:

- the view `id` and `label`;
- the root IFC class, such as `IfcProject`, `IfcProjectOrder`, or
  `IfcInventory`;
- the traversed IFC relationships, such as `IfcRelAggregates`, `IfcRelNests`,
  `IfcRelContainedInSpatialStructure`, and `IfcRelAssignsToGroup`.

To edit views in Blender:

1. Open `InfoVis-Settings > Settings`.
2. Under `Decomposition views`, click `Load`.
3. Edit, add, duplicate, or remove views and relationships.
4. Click `Save` to write `resources/decomposition_view.json`.
5. Use `Defaults` to load the default configuration into the interface before
   saving.

### Navigate the Tree

1. In `InfoVis-Occurrence > Decompositions`, choose the `Tree Type`.
2. Changing `Tree Type` reloads the tree automatically.
3. Use `Expand all` to open every node.
4. Use `Collapse children` to collapse child nodes.
5. Click a list item to select the corresponding object in the 3D Viewport.
6. Use the component-selection icon to select an element and its children.

### Export a Decomposition

Click `Export` and choose a file path. InfoVis creates an `.xlsx` containing:

- hierarchy level;
- IFC ID;
- name;
- IFC type;
- `ObjectType`;
- parent ID and name;
- child indicator.

If nothing is exported, load a decomposition view before clicking `Export`.

### Edit Aggregations and Order

After authenticating as editor, the panel shows:

- `change aggregations`: enables moving elements to another parent.
- `aggregation type`: chooses between `Nests` and `Aggregations`.
- `change order`: enables arrows for reordering leaf elements.

After moving or reordering, save the IFC through the normal Bonsai/Blender
workflow to preserve the changes in the file.

## InfoVis-Occurrence: Properties

The `Properties` panel works on the active object in the 3D Viewport.

1. Select an IFC object.
2. Click `Load properties`.
3. Review `Occurence Properties` and `Inherited Type Properties`.
4. Use `Show property description` to switch between technical names and
   descriptions.
5. Expand or collapse Psets with the triangular icon.

When authenticated:

- property fields become editable;
- the confirmation-icon button writes the value back to the IFC;
- referenced documents can be edited;
- the file picker can update document locations.

### Documents and Charts

When the object or Pset has referenced documents:

- use the open icon to access a URL or local file;
- use the file picker to change the path when authenticated;
- if the document is a `.CSV`, use the chart button to generate an HTML chart
  in `graphic.html`.

The chart dialog lets you choose the X axis, columns, limits, grid intervals,
ordering, and interpolation.

### Add a Property to Viewport Labels

For common properties in the panel, the `ADD` icon adds the field
`Pset.Property` to the IFC labels shown in the 3D Viewport. The displayed field
list is managed in `InfoVis-Settings > Settings`.

## InfoVis-Occurrence: Constructive Type

The `Constructive Type` panel shows information about the IFC type related to
the active object.

With an object selected, it displays:

- `ElementType`;
- type name and description;
- documents associated with the type;
- shortcuts to select all occurrences of the type;
- a shortcut to show type layers;
- a shortcut to select the type object.

When the type has components or layers, the `Layers` list lets you select the
corresponding layer in Blender.

## InfoVis-Occurrence: Connect Elements

Use `Connect Elements` to review and edit IFC connection relationships.

With objects selected, the panel lists the detected connections, including:

- `IfcRelConnectsElements`;
- `IfcRelConnectsPorts`;
- `IfcRelConnectsWithRealizingElements`.

When authenticated:

1. Choose `Connection Type`.
2. Select the desired active object in the 3D Viewport.
3. Use the `ADD` button beside `Relating Element A`.
4. Select another object and use `ADD` beside `Relating Element B`.
5. For connections that require a realizing element, fill `Realizing Element`.
6. Click `Add Connection`.

To remove an existing connection, use the disconnect icon beside the listed
connection.

## InfoVis-Catalog: Catalog

The `Catalog` panel organizes model `IfcTypeProduct` entities by element type.

1. Click `Load type products`.
2. Browse the type tree.
3. On leaf items, use:
   - the selection icon to select every occurrence of the type;
   - the information icon to open the layer report.

The layer report is generated as `layers.html` in the project root and opened in
the browser.

Click `Export Quantities` to export an `.xlsx` with type name, quantity, and
unit.

## InfoVis-Catalog: LI Mapping

The `LI Mapping` panel edits `resources/li_mapping.json` and uses that mapping
to generate an Item List spreadsheet in Excel. LI is kept as the project term
for `Lista de Itens`.

The mapping defines how each exported Item List column is filled from the IFC
model. It can read direct IFC attributes, Pset properties, quantities, spatial
hierarchy, assembly parents, lookup tables, calculated values, manual fields,
and columns that intentionally have no IFC source.

The main workflow is:

1. Open an IFC model in Blender/Bonsai.
2. Open `InfoVis-Catalog > LI Mapping`.
3. Click `Load` to load `resources/li_mapping.json`.
4. Review or edit the LI columns.
5. Click `Save` to write the JSON.
6. Click `Export LI` to generate the `.xlsx`.

Important: `Export LI` reads the saved `resources/li_mapping.json` file. If you
changed anything in the UI, click `Save` before exporting.

### Mapping File

The panel edits this file:

```text
resources/li_mapping.json
```

Main structure:

```json
{
  "$schema_version": "1.0",
  "description": "",
  "reference_sheet": "teste",
  "source_types": {},
  "columns": [],
  "subsea_flexible_classes": {},
  "description_templates": {},
  "quantity_by_class": {}
}
```

Reserved top-level keys:

| Key | Use |
|-----|-----|
| `$schema_version` | Mapping format version |
| `description` | General mapping description |
| `reference_sheet` | Reference sheet or baseline identifier |
| `source_types` | Explanatory dictionary for source types; preserved but not edited by the UI |
| `columns` | Ordered list of exported columns |

Any other top-level JSON object is treated as a support table, for example
`subsea_flexible_classes`, `description_templates`, or `quantity_by_class`.

### Panel Buttons

| Button | Action |
|--------|--------|
| `Load` | Loads `resources/li_mapping.json` into the UI and clears the previous state |
| `Save` | Saves header fields, columns, and support tables back to the JSON |
| `Export LI` | Opens a file picker and exports the Item List to `.xlsx` |
| `Add Column` | Creates a `Nova Coluna` column with source type `manual` |
| `Remove Column` | Removes the selected column |
| `Usar esta propriedade` | Copies the selected bSDD Pset and property into the selected column |
| `Add Field` | Adds an extra field to the selected column's `source` object |
| `Remove Field` | Removes the selected extra field |
| `Add Row` | Adds a row to the selected support table |
| `Remove Row` | Removes the selected support-table row |

The UI cannot create a new empty support table from scratch. To create a new
table, add it manually to `resources/li_mapping.json`, click `Load`, edit its
rows if needed, then click `Save`.

### Mapping Header

After `Load`, the panel shows three general fields.

| UI field | JSON key | Description |
|----------|----------|-------------|
| `Schema` | `$schema_version` | Mapping schema version |
| `Planilha` | `reference_sheet` | Reference sheet identifier |
| `Descricao` | `description` | General note about the mapping |

### Column List and Export Order

The central list shows every configured item in `columns`.

| Displayed field | JSON source |
|-----------------|-------------|
| column name | `column` |
| source type | `source_type` |

The list order is the Excel export order. The first item in the list becomes
the first column in the spreadsheet.

### Common Column Fields

When a column is selected, the panel shows common fields before `Source guiado`.

| UI field | JSON key | Use |
|----------|----------|-----|
| `Coluna` | `column` | Column name in Excel |
| `Origem` | `source_type` | Strategy used to fill the column |
| `Notas` | `notes` | Maintenance notes for the mapping |

Example:

```json
{
  "column": "Qtde",
  "source_type": "ifc_quantity",
  "source": {
    "mapping_table": "quantity_by_class",
    "quantity_mode": "mapping"
  },
  "notes": "Sums length for linear classes; counts occurrences for the others."
}
```

### How Export Rows Are Created

During export, InfoVis iterates over the current model's `IfcTypeProduct`
entities.

Key rules:

- each exported row represents an `IfcTypeProduct` with at least one
  occurrence;
- most values are read from the first occurrence of that type and, if empty,
  from the IFC type itself;
- quantity columns can use all occurrences of the type;
- the export uses the column order defined in the JSON;
- if no row can be generated, the operator reports that no LI rows were
  available for the current model.

### Source Types

The `Origem` field controls which fields appear in `Source guiado` and how the
exporter resolves the value.

| Source type | Use |
|-------------|-----|
| `ifc_attribute` | Reads a direct attribute from the occurrence or IFC type |
| `ifc_property` | Reads a property inside a Pset |
| `ifc_quantity` | Calculates quantity by count, length, or a support table |
| `ifc_class` | Reads an IFC class/key and translates it through a support table |
| `spatial` | Reads a value from an ancestor in the spatial/decomposition hierarchy |
| `aggregation_parent` | Reads a value from a parent or grandparent in the assembly chain |
| `computed` | Calculates a value by method or template |
| `manual` | Represents a manual or optional custom Pset column |
| `not_applicable` | Represents a column with no IFC source; exports empty |

### Source: ifc_attribute

Use `ifc_attribute` to read direct IFC entity attributes.

| UI field | Key in `source` | Export use |
|----------|-----------------|------------|
| `Classe` | `ifc_class` | Metadata saved in JSON; the current exporter does not filter by it |
| `Atributo` | `attribute` | Main attribute to read |
| `Fallback` | `fallback_attribute` | Alternative attribute if the main value is empty |
| `Format` | `format` | Metadata saved in JSON; the current exporter does not apply formatting |

Resolution order:

1. Read `attribute` from the occurrence.
2. If empty, read `attribute` from the IFC type.
3. If still empty and `fallback_attribute` exists, repeat the search for the
   fallback.
4. If `attribute` is `is_a`, return the normalized IFC class without the `Ifc`
   prefix and without the `Type` suffix.

Useful attributes:

| Attribute | Expected result |
|-----------|-----------------|
| `Name` | occurrence or type name |
| `Description` | description |
| `Tag` | IFC tag |
| `ObjectType` | IFC object type |
| `GlobalId` | IFC global identifier |
| `is_a` | normalized IFC class |

Example:

```json
{
  "column": "Name",
  "source_type": "ifc_attribute",
  "source": {
    "attribute": "Name",
    "fallback_attribute": "Tag"
  },
  "notes": ""
}
```

### Source: ifc_property

Use `ifc_property` to read a property from a Pset.

| UI field | Key in `source` | Export use |
|----------|-----------------|------------|
| `Classe` | `ifc_class` | Metadata saved in JSON; the current exporter does not filter by it |
| `Pset` | `pset` | Technical property set name |
| `Property` | `property` | Technical property name |
| `Allowed Values` | `allowed_values` | Metadata saved in JSON; the current exporter does not validate values |

Resolution order:

1. Search for the Pset on the occurrence.
2. If no value is found, search for the Pset on the IFC type.
3. Return the first non-empty value.
4. If no value is found, export an empty cell.

Example:

```json
{
  "column": "Nominal Length",
  "source_type": "ifc_property",
  "source": {
    "pset": "Pset_FlexiblePipeSegment",
    "property": "NominalLength"
  },
  "notes": ""
}
```

### Source: manual

Use `manual` for LI columns that must exist but may not exist in the standard
IFC model. The UI and resolution behavior are the same as `ifc_property`.

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Classe` | `ifc_class` | Metadata saved in JSON |
| `Pset` | `pset` | Custom or future Pset |
| `Property` | `property` | Custom or future property |
| `Allowed Values` | `allowed_values` | Metadata for expected values |

Behavior:

- if the Pset/property exists in the IFC, the value is exported;
- if it does not exist, the column is exported empty for later filling;
- this type is suitable for procurement, supply, status, revision, or other
  fields that are not modeled yet.

Example:

```json
{
  "column": "Observation",
  "source_type": "manual",
  "source": {
    "pset": "Pset_LI_Extra",
    "property": "Observation"
  },
  "notes": "Manual field if it does not exist in the IFC."
}
```

### bSDD Picker for ifc_property and manual

When the source is `ifc_property` or `manual`, the `Escolher do dicionario bSDD`
area appears.

| Field | Options |
|-------|---------|
| `Discipline` | `Flexible Pipes` or `Rigid Pipes` |
| `Element` | classes from the selected dictionary, read from `resources/subsea_*_completo.json` |
| `Property set` | Psets associated with the selected element |
| `Property` | properties associated with the selected Pset |

| Button | Result |
|--------|--------|
| `Usar esta propriedade` | sets `source_type` to `ifc_property`, copies `Property set` to `source.pset`, and copies `Property` to `source.property` |

If the column name is empty or `Nova Coluna`, the button also changes the column
name to the selected property name.

The picker uses:

```text
resources/subsea_flexible_pipes_2.1_completo.json
resources/subsea_rigid_pipes_1.0_completo.json
```

### Source: spatial

Use `spatial` to read information from the spatial or decomposition hierarchy.

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Nivel (classe IFC)` | `level` | IFC ancestor class to find, such as `IfcSite` or `IfcBuilding` |
| `Atributo` | `attribute` | Attribute to read from the matched ancestor |

Resolution order:

1. Build an ancestor chain from the occurrence.
2. Traverse `ContainedInStructure`, `Decomposes`, and `Nests`.
3. Find the first ancestor whose class equals `level`.
4. Return the configured attribute from that ancestor.
5. If no match is found, export an empty cell.

Useful extra fields:

| Extra key | Use |
|-----------|-----|
| `fallback_levels` | JSON list of alternative classes to search after `level` |
| `fallback_attribute` | Alternative attribute, although it is not exposed as a guided field for this source |

Example:

```json
{
  "column": "Site",
  "source_type": "spatial",
  "source": {
    "level": "IfcSite",
    "attribute": "Name",
    "fallback_levels": ["IfcBuilding"]
  },
  "notes": ""
}
```

### Source: aggregation_parent

Use `aggregation_parent` to read attributes from an ancestor in the assembly
chain, considering only nesting and decomposition relationships.

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Nivel (1=pai imediato, 2=avo, ...)` | `level` | Ancestor position in the chain |
| `Atributo` | `attribute` | Attribute to read |
| `Fallback` | `fallback_attribute` | Alternative attribute if the main value is empty |

Resolution order:

1. Walk up the chain through `Nests` and then `Decomposes`.
2. Do not use `ContainedInStructure` or spatial groups.
3. Interpret `level=1` as the immediate parent, `level=2` as the grandparent,
   and so on.
4. Read `attribute` from the matched ancestor.
5. If empty, try `fallback_attribute`.
6. If no ancestor exists at that level, export an empty cell.

Example:

```json
{
  "column": "Pipe Line",
  "source_type": "aggregation_parent",
  "source": {
    "level": "2",
    "attribute": "Name"
  },
  "notes": "Grandparent in the assembly chain."
}
```

### Source: ifc_class

Use `ifc_class` to derive a business class from an IFC attribute and translate
the value through a support table.

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Atributo` | `attribute` | Attribute used to form the class key |
| `Mapping Table` | `mapping_table` | Support table used to translate the key |

Resolution order:

1. Read `attribute` from the occurrence.
2. If empty, read `attribute` from the IFC type.
3. If still empty, use the normalized IFC class from the type.
4. Look up the value in the support table referenced by `mapping_table`.
5. If found, export the mapped value.
6. If not found, export the key itself.

Useful extra field:

| Extra key | Use |
|-----------|-----|
| `fallback_attribute` | Alternative attribute to form the key, although it is not exposed as a guided field for this source |

Example:

```json
{
  "column": "Class",
  "source_type": "ifc_class",
  "source": {
    "attribute": "ObjectType",
    "mapping_table": "subsea_flexible_classes"
  },
  "notes": ""
}
```

Matching support table:

```json
{
  "subsea_flexible_classes": {
    "FlexiblePipeSegment": "Pipe section",
    "EndFitting": "Connector"
  }
}
```

### Source: ifc_quantity

Use `ifc_quantity` to calculate the LI row quantity.

Always visible field:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Modo` | `quantity_mode` | Quantity strategy |

`Modo` options:

| UI mode | JSON value | Result |
|---------|------------|--------|
| `Mapping Table` | `mapping` | Uses a support table to decide whether to count or sum length |
| `Count Occurrences` | `count` | Counts IFC type occurrences |
| `Sum Length` | `length` | Sums length through `get_qtde()` |

When `Modo` is `Mapping Table`, the panel also shows:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Mapping Table` | `mapping_table` | Table with class-specific rules |
| `Selected By` | `selected_by` | Name of an already calculated column that may also select the rule |

Resolution order in `mapping` mode:

1. Read the table referenced by `mapping_table`.
2. Calculate a class key from the occurrence `ObjectType` or IFC class.
3. Also read the value of the column named by `selected_by`, when present.
4. Search for a rule in this order: class key, selected value, `_default`.
5. If the rule has `quantity` equal to `Length`, sum length.
6. Otherwise, count occurrences.

Current length rule:

- for `IfcPipeSegmentType`, sum `NominalLength` from occurrences in
  `OGSubPset_FlexiblePipeSegmentOccurence`;
- for other types, `get_qtde()` returns the occurrence count.

Example:

```json
{
  "column": "Qtde",
  "source_type": "ifc_quantity",
  "source": {
    "mapping_table": "quantity_by_class",
    "quantity_mode": "mapping",
    "selected_by": "Class"
  },
  "notes": ""
}
```

Support table:

```json
{
  "quantity_by_class": {
    "FlexiblePipeSegment": {
      "qto": "Qto_FlexiblePipeSegment",
      "quantity": "Length"
    },
    "_default": {
      "qto": "BaseQuantities",
      "quantity": "Count"
    }
  }
}
```

### Source: computed

Use `computed` for calculated values. Behavior depends on `Method` or on the
combination of `Template Table` and `Selected By`.

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Selected By` | `selected_by` | Already calculated column used to choose a template |
| `Template Table` | `template_table` | Support table with templates |
| `Derived From` | `derived_from` | Base column for some methods |
| `Method` | `method` | Special calculation method |
| `Format` | `format` | Metadata saved in JSON; the current exporter does not apply formatting |

#### Method: quantity_unit_symbol

Derives the unit from a quantity column.

| Field | Value |
|-------|-------|
| `Method` | `quantity_unit_symbol` |
| `Derived From` | name of the quantity column, for example `Qtde` |

Resolution order:

1. Read the already calculated value in `derived_from`.
2. If it is empty, export an empty cell.
3. If the derived column uses `quantity_mode=count`, return `un`.
4. If it uses `quantity_mode=length`, return `m`.
5. If it uses `mapping`, inspect `quantity_by_class`.
6. When possible, try to obtain the real IFC Qto unit.
7. If no unit can be read, use `m` for length and `un` for count.

Example:

```json
{
  "column": "Unit",
  "source_type": "computed",
  "source": {
    "derived_from": "Qtde",
    "method": "quantity_unit_symbol"
  },
  "notes": ""
}
```

#### Method: spatial_name_part

Extracts information from the occurrence `Name` or from an ancestor whose
`Name` contains a separator.

| Field | Use |
|-------|-----|
| `Method` | `spatial_name_part` |
| `separator` | extra field; separator used in `Name`; default `/` |
| `part_index` | optional extra field; index after `split` |

Behavior:

- search the occurrence first;
- then search ancestors through `ContainedInStructure`, `Decomposes`, and
  `Nests`;
- if a `Name` contains the separator and no `part_index` is set, return the
  full name;
- if `part_index` is set, return only the indexed part.

Example:

```json
{
  "column": "space",
  "source_type": "computed",
  "source": {
    "method": "spatial_name_part",
    "separator": "/",
    "part_index": 0
  },
  "notes": ""
}
```

#### Template Table + Selected By

When `method` is not a special method, `computed` can render a text template.

| Field | Use |
|-------|-----|
| `Selected By` | column name used as the key, for example `Class` |
| `Template Table` | support table name, for example `description_templates` |

Resolution order:

1. Read the already calculated value of the `selected_by` column.
2. Use that value to choose a template in the table.
3. If no match exists, use `_default`.
4. Replace placeholders in the template.
5. Export the final text.

Accepted placeholders:

| Placeholder | Result |
|-------------|--------|
| `{attr.Name}` | direct attribute from the occurrence or type |
| `{attr.Tag}` | occurrence or type tag |
| `{Pset_Name.Property}` | Pset property value from the occurrence or type |

Example:

```json
{
  "column": "Description",
  "source_type": "computed",
  "source": {
    "selected_by": "Class",
    "template_table": "description_templates"
  },
  "notes": ""
}
```

Support table:

```json
{
  "description_templates": {
    "Pipe section": "Pipe section {attr.Tag}; length {Pset_FlexiblePipeSegment.NominalLength} m",
    "_default": "{attr.Description}"
  }
}
```

### Source: not_applicable

Use `not_applicable` for control columns that must exist in the LI but have no
IFC source.

Guided fields:

- no `Source guiado` field is displayed;
- metadata can be registered in `Campos extras`, but the export always returns
  an empty value for this source.

Example:

```json
{
  "column": "Status",
  "source_type": "not_applicable",
  "source": null,
  "notes": "Spreadsheet control field."
}
```

### Extra Fields

`Campos extras` adds `Key` / `Value` pairs to the selected column's `source`
object.

Use it for:

- exporter-supported keys that are not exposed as guided fields;
- parameters required by `computed` methods;
- lists, objects, or scalar values that must be saved in JSON.

Rules:

- if `Value` is valid JSON, it is saved as JSON;
- otherwise, it is saved as text;
- extra fields are added after guided fields and can overwrite a guided key
  with the same name;
- empty keys are ignored during save.

Examples:

| Key | Value | Use |
|-----|-------|-----|
| `separator` | `/` | separator for `spatial_name_part` |
| `part_index` | `0` | index extracted by the method |
| `fallback_levels` | `["IfcBuilding", "IfcSite"]` | alternative spatial levels |
| `fallback_attribute` | `Tag` | fallback attribute for sources that do not expose this field |
| `allowed_values` | `["A", "B", "C"]` | expected values list |

### Support Tables

The `Tabelas de apoio` area edits first-level JSON objects that are not
reserved keys.

Table fields:

| UI field | JSON key | Use |
|----------|----------|-----|
| `Tabela` | top-level key name | Name referenced by `mapping_table` or `template_table` |
| `Comentario` | `_comment` | Comment saved inside the table |

Row fields:

| UI field | JSON | Use |
|----------|------|-----|
| `Chave` | object key | Lookup value |
| `Valor` | key value | May be text, number, list, or JSON object |

Simple table example:

```json
{
  "subsea_flexible_classes": {
    "FlexiblePipeSegment": "Pipe section",
    "EndFitting": "Connector"
  }
}
```

Table with objects:

```json
{
  "quantity_by_class": {
    "FlexiblePipeSegment": {
      "qto": "Qto_FlexiblePipeSegment",
      "quantity": "Length"
    },
    "_default": {
      "qto": "BaseQuantities",
      "quantity": "Count"
    }
  }
}
```

When editing complex values in the UI, write valid JSON in `Valor`.

Example `Valor` for a row:

```json
{"qto": "Qto_FlexiblePipeSegment", "quantity": "Length"}
```

### Guided Fields by Source Type

| Source type | Guided fields saved in `source` |
|-------------|---------------------------------|
| `ifc_attribute` | `ifc_class`, `attribute`, `fallback_attribute`, `format` |
| `ifc_property` | `ifc_class`, `pset`, `property`, `allowed_values` |
| `manual` | `ifc_class`, `pset`, `property`, `allowed_values` |
| `spatial` | `level`, `attribute` |
| `aggregation_parent` | `level`, `attribute`, `fallback_attribute` |
| `ifc_class` | `attribute`, `mapping_table` |
| `ifc_quantity` | `quantity_mode`, `mapping_table`, `selected_by` |
| `computed` | `selected_by`, `template_table`, `derived_from`, `method`, `format` |
| `not_applicable` | no guided field |

### Complete Column Example

```json
{
  "column": "Pipe Line",
  "source_type": "aggregation_parent",
  "source": {
    "level": "2",
    "attribute": "Name"
  },
  "notes": "Grandparent in the assembly chain."
}
```

### Add a bSDD Property Column

To add a column that reads a bSDD property:

1. Click `Load`.
2. Click `Add Column`.
3. In `Coluna`, enter the name to appear in Excel.
4. In `Origem`, select `IFC Property`.
5. In `Escolher do dicionario bSDD`, choose `Discipline`.
6. Choose `Element`.
7. Choose `Property set`.
8. Choose `Property`.
9. Click `Usar esta propriedade`.
10. Review `Notas`.
11. Click `Save`.
12. Click `Export LI`.

### Checklist Before Export

- The IFC model is open in Bonsai/Blender.
- The model has `IfcTypeProduct` entities with occurrences.
- UI changes were saved with `Save`.
- Columns that depend on other columns appear after their base columns.
- `Selected By` exactly matches the name of an earlier column.
- `Mapping Table` and `Template Table` point to existing tables.
- Complex support-table values are valid JSON.
- `computed` columns using `quantity_unit_symbol` have `Derived From`.

### LI Troubleshooting

| Symptom | Check |
|---------|-------|
| `Export LI` does not reflect a UI change | Click `Save` before exporting |
| Export reports that no row was generated | The IFC must have `IfcTypeProduct` entities with occurrences |
| A column is empty | Confirm `source_type`, Pset/property, attribute, or configured level |
| `Selected By` does not work | The referenced column must exist and be calculated earlier |
| A support table is not used | Confirm that `mapping_table` or `template_table` matches the table name |
| A complex value became text | The `Valor` field must contain valid JSON |
| Unit is `un` but should be `m` | Check `quantity_by_class` and the `quantity: Length` rule |
| bSDD property does not appear in the picker | Check `Discipline`, `Element`, and whether the dictionary JSON contains the property |

### Maintenance Notes

- The UI preserves `source_types`, but does not edit it.
- `Save` removes and recreates support tables from the data loaded in the UI.
- `ifc_class`, `format`, and `allowed_values` are saved in some source types,
  but some of them currently act as metadata; the current exporter does not use
  them for filtering, formatting, or validation.
- `computed` columns can depend on values already calculated in `row_values`,
  so column order matters.
- For fields that are not supported by the UI yet, use `Campos extras` or edit
  the JSON directly.

## InfoVis-Analisys: Analisys

The `Analisys` panel colors 3D Viewport objects based on IFC properties.

1. Choose `Discipline`.
2. Choose `Element`.
3. Choose `Property set`.
4. Choose `Property`.
5. Choose `Mode`:
   - `Distinct values`: creates one color per distinct value.
   - `Exact value`: highlights one specific value.
   - `Numeric range`: colors objects within a numeric range.
6. Click `Apply colors`.
7. Review `Legend` and `Status`.

Use `Reset colors` to restore object colors in the 3D Viewport.

## InfoVis-Settings: Settings

The `Settings` panel centralizes visual settings and decomposition views.

### IFC Labels in the Viewport

1. Enable or disable `Show IFC label`.
2. In `Fields to display`, add IFC attributes or properties.
3. Adjust `Display text` to control the label name shown on screen.
4. Adjust `Label offset (px)` to move the label on screen.

Property fields must use this format:

```text
PsetName.PropertyName
```

Example:

```text
Pset_FlexiblePipeSegment.NominalLength
```

## Generated and Edited Files

| Action | Output |
|--------|--------|
| `Export IDS file` | `.ids` file chosen by the user |
| `Decompositions > Export` | `.xlsx` file chosen by the user |
| `Catalog > Export Quantities` | `.xlsx` file chosen by the user |
| `LI Mapping > Export LI` | `.xlsx` file chosen by the user |
| `Catalog > show layers` | `layers.html` in the project root |
| `Properties > graph` | `graphic.html` in the project root |
| `LI Mapping > Save` | `resources/li_mapping.json` |
| `Settings > Decomposition views > Save` | `resources/decomposition_view.json` |

## Troubleshooting

| Symptom | Check |
|---------|-------|
| `No Ifc file loaded` | Load an IFC in Bonsai/Blender before using the panel |
| Empty decomposition tree | Check the `Tree Type` and the view `root_ifc_class` |
| bSDD does not load classes or properties | Check internet access and API availability |
| Fields appear read-only | Log in as editor in the Add-on preferences |
| Document does not open | Confirm that `Location` is a valid URL or existing path |
| Chart generation fails | The document must be CSV and the path must exist |
| LI export creates no rows | Confirm that the IFC has `IfcTypeProduct` entities with occurrences |
| Labels do not show a property | Use `Pset.Property` format and reload the object properties |

## Best Practices

- Load properties after selecting the object you want to inspect.
- Save the IFC in Bonsai/Blender after editing properties, connections, or
  decompositions.
- Before exporting LI, load, review, and save `LI Mapping`.
- Before exporting a decomposition, select the correct view in `Tree Type`.
- Use `Reset colors` after visual analyses to clean up the 3D Viewport.
