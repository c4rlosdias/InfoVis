# Subsea JSON Structure and Audit Guide

This guide documents the structural pattern of the `resources/subsea_*_completo.json` files and provides a repeatable checklist for future audits.

## Scope

- `resources/subsea_flexible_pipes_2.1_completo.json`
- `resources/subsea_rigid_pipes_1.0_completo.json`

## Current Snapshot

- `subsea_flexible_pipes_2.1_completo.json`
  - classes (`classType` occurrences): 110
  - class-level `propertySets` blocks: 110
  - class-level `properties` blocks: 180
  - property `units` fields: 1008
- `subsea_rigid_pipes_1.0_completo.json`
  - classes (`classType` occurrences): 280
  - class-level `propertySets` blocks: 280
  - class-level `properties` blocks: 1085
  - property `units` fields: 2977

## Top-Level Structure

Expected top-level keys:

```json
{
  "dictionary": {
    "uri": "...",
    "code": "...",
    "name": "...",
    "version": "...",
    "organizationNameOwner": "...",
    "defaultLanguageCode": "en-GB",
    "license": "MIT license",
    "status": "Active|Preview|...",
    "releaseDate": "YYYY-MM-DDTHH:MM:SSZ",
    "classesTotalCount": 0
  },
  "exportLanguage": null,
  "classes": [ ... ]
}
```

## Class Object Structure

Each item in `classes` should follow this shape:

```json
{
  "uri": ".../class/<ClassCode>",
  "code": "ClassCode",
  "name": "ClassName",
  "classType": "Class|Material|...",
  "definition": "...",
  "description": "...",
  "parentClassReference": {
    "uri": "...",
    "name": "...",
    "code": "..."
  },
  "relatedIfcEntityNames": ["Ifc..."],
  "synonyms": ["..."] ,
  "status": "Active|...",
  "propertySets": [ ... ]
}
```

Notes:

- `parentClassReference`, `relatedIfcEntityNames`, `synonyms`, and `propertySets` may be `null`, empty arrays, or populated.
- A few class objects may be sparse/incomplete in source dictionaries and should be flagged during audits.

## Property Set Structure

Each item in `propertySets` typically follows:

```json
{
  "name": "OGSubPset_...",
  "properties": [ ... ]
}
```

## Property Structure

Each item in `properties` typically follows:

```json
{
  "code": "...",
  "name": "...",
  "description": "...",
  "definition": "...",
  "dataType": "String|Boolean|Integer|Real|...",
  "units": null,
  "allowedValues": null,
  "isRequired": null,
  "propertyUri": ".../prop/<PropertyCode>",
  "uri": ".../class/<Class>/prop/<Pset>/<Property>"
}
```

Notes:

- `units` can be `null` or an array of symbols (for example `["m"]`, `["MPa"]`, `["W/(m·K)"]`).
- `allowedValues` can be `null`, an empty array, or an array of objects with keys like `code`, `value`, and `description`.
- `isRequired` is often `null` in current datasets.

## Audit Checklist

1. Top-level integrity
- File is valid JSON.
- Top-level keys `dictionary`, `exportLanguage`, and `classes` exist.
- `dictionary.classesTotalCount` matches the actual number of class objects whenever possible.

2. Class integrity
- Every class has non-empty `uri`, `code`, and `name`.
- `uri` and `code` are consistent (last URI segment should match code semantics).
- `status` is present.

3. Property set integrity
- `propertySets` is present (allow empty array).
- Each pset has `name` and `properties`.

4. Property integrity
- Every property has `code`, `name`, `dataType`, `propertyUri`, and `uri`.
- `units` format is consistent (`null` or string array).
- `allowedValues` content matches `dataType` expectations.

5. Unit mapping integrity
- Every unit symbol used in subsea files exists in `resources/units.json`.
- Equivalent notation variants are either standardized or explicitly mapped as aliases in `resources/units.json`.

## Recommended Periodic Checks

- Re-run unit coverage check after every dictionary update.
- Re-run structural counts (`classType`, `propertySets`, `properties`, `units`) and compare with previous baseline.
- Flag sudden drops/increases as potential export issues.

## Related Files

- `resources/subsea_flexible_pipes_2.1_completo.json`
- `resources/subsea_rigid_pipes_1.0_completo.json`
- `resources/units.json`
- `docs/extra/UNITS_IFC_MAPPING_REPORT.md`
