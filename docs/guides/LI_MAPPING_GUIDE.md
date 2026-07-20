# Detailed LI Mapping Guide

This guide documents every option in the `LI Mapping` panel, located at
`InfoVis-Catalog > LI Mapping`, and explains how those options affect
`resources/li_mapping.json` and the Excel export of the Item List.

## Purpose

`LI Mapping` defines how each Item List column is filled from the IFC model. The
panel lets users edit the mapping without opening the JSON manually, using
guided fields for IFC attributes, Pset properties, quantities, spatial
hierarchy, assembly chains, support tables, and calculated values.

The main workflow is:

1. Open an IFC model in Blender/Bonsai.
2. Open `InfoVis-Catalog > LI Mapping`.
3. Click `Load` to load `resources/li_mapping.json`.
4. Review or edit the LI columns.
5. Click `Save` to write the JSON.
6. Click `Export LI` to generate the `.xlsx`.

Important: `Export LI` reads the saved `resources/li_mapping.json` file. If you
changed anything in the UI, click `Save` before exporting.

## File Used by the Panel

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

Reserved keys:

| Key | Use |
|-----|-----|
| `$schema_version` | Mapping format version |
| `description` | General mapping description |
| `reference_sheet` | Reference sheet or baseline identifier |
| `source_types` | Explanatory dictionary for source types; preserved but not edited by the UI |
| `columns` | Ordered list of exported columns |

Any other top-level JSON object is treated as a support table, for example
`subsea_flexible_classes`, `description_templates`, or `quantity_by_class`.

## Panel Buttons

| Button | Action |
|--------|--------|
| `Load` | Loads `resources/li_mapping.json` into the UI and clears the previous state |
| `Save` | Saves header fields, columns, and support tables back to the JSON |
| `Export LI` | Opens a file picker and exports the Item List to `.xlsx` |
| `Add Column` | Creates a column named `New Column` with source type `manual` |
| `Remove Column` | Removes the selected column |
| `Use this property` | Copies the selected bSDD Pset and property into the selected column |
| `Add Field` | Adds an extra field to the selected column's `source` object |
| `Remove Field` | Removes the selected extra field |
| `Add Row` | Adds a row to the selected support table |
| `Remove Row` | Removes the selected support-table row |

There is no button for creating a new empty support table. To create a new
table, add it manually to `resources/li_mapping.json`, click `Load`, edit rows
if needed, then click `Save`.

## Mapping Header

After `Load`, the panel shows three general fields.

| UI field | JSON key | Description |
|----------|----------|-------------|
| `Schema` | `$schema_version` | Mapping schema version |
| `Reference Sheet` | `reference_sheet` | Reference sheet identifier |
| `Description` | `description` | General note about the mapping |

## Column List

The central list shows every configured item in `columns`.

Each list item shows:

| Displayed field | Source |
|-----------------|--------|
| column name | `column` |
| source type | `source_type` |

The list order is the export order. The first column in the list becomes the
first column in Excel.

## Common Column Fields

When a column is selected, the panel shows common fields before `Guided Source`.

| UI field | JSON key | Use |
|----------|----------|-----|
| `Column` | `column` | Column name in Excel |
| `Source` | `source_type` | Strategy used to fill the column |
| `Notes` | `notes` | Maintenance notes for the mapping |

Example:

```json
{
  "column": "Quantity",
  "source_type": "ifc_quantity",
  "source": {
    "mapping_table": "quantity_by_class",
    "quantity_mode": "mapping"
  },
  "notes": "Sums length for linear classes; counts occurrences for the others."
}
```

## How Export Rows Are Created

During export, InfoVis iterates over the current model's `IfcTypeProduct`
entities.

Important rules:

- each exported row represents an `IfcTypeProduct` with at least one
  occurrence;
- most values are read from the first occurrence of that type and, if empty,
  from the IFC type itself;
- quantity columns can use all occurrences of the type;
- the export uses the column order defined in the JSON;
- if no row can be generated, the operator reports that no LI rows are
  available for the current model.

## Source Types

The `Source` field controls which fields appear in `Guided Source` and how the
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

## Source: ifc_attribute

Use `ifc_attribute` to read direct IFC entity attributes.

Displayed fields:

| UI field | Key in `source` | Export use |
|----------|-----------------|------------|
| `Class` | `ifc_class` | Metadata saved in JSON; the current exporter does not filter by it |
| `Attribute` | `attribute` | Main attribute to read |
| `Fallback` | `fallback_attribute` | Alternative attribute if the main value is empty |
| `Format` | `format` | Metadata saved in JSON; the current exporter does not apply formatting |

Resolution order:

1. Read `attribute` from the occurrence.
2. If empty, read `attribute` from the IFC type.
3. If still empty and `fallback_attribute` exists, repeat the search for the
   fallback.
4. If `attribute` is `is_a`, return the normalized IFC class without the `Ifc`
   prefix and without the `Type` suffix.

Attribute examples:

| Attribute | Expected result |
|-----------|-----------------|
| `Name` | occurrence or type name |
| `Description` | description |
| `Tag` | IFC tag |
| `ObjectType` | IFC object type |
| `GlobalId` | IFC global identifier |
| `is_a` | normalized IFC class |

JSON example:

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

## Source: ifc_property

Use `ifc_property` to read a property from a Pset.

Displayed fields:

| UI field | Key in `source` | Export use |
|----------|-----------------|------------|
| `Class` | `ifc_class` | Metadata saved in JSON; the current exporter does not filter by it |
| `Pset` | `pset` | Technical property set name |
| `Property` | `property` | Technical property name |
| `Allowed Values` | `allowed_values` | Metadata saved in JSON; the current exporter does not validate values |

Resolution order:

1. Search for the Pset on the occurrence.
2. If no value is found, search for the Pset on the IFC type.
3. Return the first non-empty value.
4. If no value is found, export an empty cell.

JSON example:

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

## Source: manual

Use `manual` for LI columns that must exist but may not exist in the standard
IFC model. The UI and resolution behavior are the same as `ifc_property`.

Displayed fields:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Class` | `ifc_class` | Metadata saved in JSON |
| `Pset` | `pset` | Custom or future Pset |
| `Property` | `property` | Custom or future property |
| `Allowed Values` | `allowed_values` | Metadata for expected values |

Behavior:

- if the Pset/property exists in the IFC, the value is exported;
- if it does not exist, the column is exported empty for later filling;
- this type is suitable for procurement, supply, status, revision, or other
  fields that are not modeled yet.

JSON example:

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

## bSDD Picker for ifc_property and manual

When the source is `ifc_property` or `manual`, the `Pick from bSDD dictionary`
area appears.

Fields:

| Field | Options |
|-------|---------|
| `Discipline` | `Flexible Pipes` or `Rigid Pipes` |
| `Element` | classes from the selected dictionary, read from `resources/subsea_*_completo.json` |
| `Property set` | Psets associated with the selected element |
| `Property` | properties associated with the selected Pset |

Button:

| Button | Result |
|--------|--------|
| `Use this property` | sets `source_type` to `ifc_property`, copies `Property set` to `source.pset`, and copies `Property` to `source.property` |

If the column name is empty or `New Column`, the button also changes the column
name to the selected property name.

The picker uses these files:

```text
resources/subsea_flexible_pipes_2.1_completo.json
resources/subsea_rigid_pipes_1.0_completo.json
```

## Source: spatial

Use `spatial` to read information from the spatial or decomposition hierarchy.

Displayed fields:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Level (IFC class)` | `level` | IFC ancestor class to find, such as `IfcSite` or `IfcBuilding` |
| `Attribute` | `attribute` | Attribute to read from the matched ancestor |

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

JSON example:

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

## Source: aggregation_parent

Use `aggregation_parent` to read attributes from an ancestor in the assembly
chain, considering only nesting and decomposition relationships.

Displayed fields:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Level (1=direct parent, 2=grandparent, ...)` | `level` | Ancestor position in the chain |
| `Attribute` | `attribute` | Attribute to read |
| `Fallback` | `fallback_attribute` | Alternative attribute if the main value is empty |

Resolution order:

1. Walk up the chain through `Nests` and then `Decomposes`.
2. Do not use `ContainedInStructure` or spatial groups.
3. Interpret `level=1` as the immediate parent, `level=2` as the grandparent,
   and so on.
4. Read `attribute` from the matched ancestor.
5. If empty, try `fallback_attribute`.
6. If no ancestor exists at that level, export an empty cell.

JSON example:

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

## Source: ifc_class

Use `ifc_class` to derive a business class from an IFC attribute and translate
the value through a support table.

Displayed fields:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Attribute` | `attribute` | Attribute used to form the class key |
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

Example with table:

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

## Source: ifc_quantity

Use `ifc_quantity` to calculate the LI row quantity.

Always visible field:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Mode` | `quantity_mode` | Quantity strategy |

`Mode` options:

| UI mode | JSON value | Result |
|---------|------------|--------|
| `Mapping Table` | `mapping` | Uses a support table to decide whether to count or sum length |
| `Count Occurrences` | `count` | Counts IFC type occurrences |
| `Sum Length` | `length` | Sums length through `get_qtde()` |

When `Mode` is `Mapping Table`, the panel also shows:

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

JSON example:

```json
{
  "column": "Quantity",
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

## Source: computed

Use `computed` for calculated values. Behavior depends on `Method` or on the
combination of `Template Table` and `Selected By`.

Displayed fields:

| UI field | Key in `source` | Use |
|----------|-----------------|-----|
| `Selected By` | `selected_by` | Already calculated column used to choose a template |
| `Template Table` | `template_table` | Support table with templates |
| `Derived From` | `derived_from` | Base column for some methods |
| `Method` | `method` | Special calculation method |
| `Format` | `format` | Metadata saved in JSON; the current exporter does not apply formatting |

### Method: quantity_unit_symbol

Derives the unit from a quantity column.

Expected fields:

| Field | Value |
|-------|-------|
| `Method` | `quantity_unit_symbol` |
| `Derived From` | name of the quantity column, for example `Quantity` |

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
    "derived_from": "Quantity",
    "method": "quantity_unit_symbol"
  },
  "notes": ""
}
```

### Method: spatial_name_part

Extracts information from the occurrence `Name` or from an ancestor whose
`Name` contains a separator.

Expected fields:

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

### Template Table + Selected By

When `method` is not a special method, `computed` can render a text template.

Expected fields:

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

## Source: not_applicable

Use `not_applicable` for control columns that must exist in the LI but have no
IFC source.

Guided fields:

- no `Guided Source` field is displayed;
- metadata can be registered in `Extra Fields`, but the export always returns
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

## Extra Fields

`Extra Fields` adds `Key` / `Value` pairs to the selected column's `source`
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

## Support Tables

The `Support Tables` area edits first-level JSON objects that are not
reserved keys.

Table fields:

| UI field | JSON key | Use |
|----------|----------|-----|
| `Table` | top-level key name | Name referenced by `mapping_table` or `template_table` |
| `Comment` | `_comment` | Comment saved inside the table |

Row fields:

| UI field | JSON | Use |
|----------|------|-----|
| `Key` | object key | Lookup value |
| `Value` | key value | May be text, number, list, or JSON object |

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

When editing complex values in the UI, write valid JSON in `Value`.

Example `Value` for a row:

```json
{"qto": "Qto_FlexiblePipeSegment", "quantity": "Length"}
```

## Field Matrix by Source Type

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

## Complete Column Example

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

## Complete Workflow Example

To add a column that reads a bSDD property:

1. Click `Load`.
2. Click `Add Column`.
3. In `Column`, enter the name that should appear in Excel.
4. In `Source`, select `IFC Property`.
5. In `Pick from bSDD dictionary`, choose `Discipline`.
6. Choose `Element`.
7. Choose `Property set`.
8. Choose `Property`.
9. Click `Use this property`.
10. Review `Notes`.
11. Click `Save`.
12. Click `Export LI`.

## Pre-Export Checklist

- The IFC model is open in Bonsai/Blender.
- The model has `IfcTypeProduct` entities with occurrences.
- UI changes were saved with `Save`.
- Columns that depend on other columns appear after their base columns.
- `Selected By` exactly matches the name of an earlier column.
- `Mapping Table` and `Template Table` point to existing tables.
- Complex support-table values are valid JSON.
- `computed` columns using `quantity_unit_symbol` have `Derived From`.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| `Export LI` does not reflect a UI change | Click `Save` before exporting |
| Export reports that no row was generated | The IFC must have `IfcTypeProduct` entities with occurrences |
| A column is empty | Confirm `source_type`, Pset/property, attribute, or configured level |
| `Selected By` does not work | The referenced column must exist and be calculated earlier |
| A support table is not used | Confirm that `mapping_table` or `template_table` matches the table name |
| A complex value became text | The `Value` field must contain valid JSON |
| Unit is `un` but should be `m` | Check `quantity_by_class` and the `quantity: Length` rule |
| bSDD property does not appear in the picker | Check `Discipline`, `Element`, and whether the dictionary JSON contains the property |

## Maintenance Notes

- The UI preserves `source_types`, but does not edit it.
- `Save` removes and recreates support tables from the data loaded in the UI.
- `ifc_class`, `format`, and `allowed_values` are saved in some source types,
  but some of them currently act as metadata; the current exporter does not use
  them for filtering, formatting, or validation.
- `computed` columns can depend on values already calculated in `row_values`,
  so column order matters.
- For fields that are not supported by the UI yet, use `Extra Fields` or edit
  the JSON directly.
