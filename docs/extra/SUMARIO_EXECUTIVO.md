# Executive Summary

## Summary

InfoVis is a Blender add-on for visualizing and enriching IFC information. The
project combines object-data navigation, bSDD lookup, decomposition structures,
type catalogs, element connections, and property inspection.

## Essential Information

| Aspect | Description |
|--------|-------------|
| Add-on name | InfoVis |
| Current version in code | 0.1.3 |
| Target environment | Blender 5.0+ |
| Language | Python |
| Structure | Modular, based on `modules/` and `data/` |
| Distribution | Installable zip generated in `releases/` |

## What the Project Delivers

- reading and organizing IFC information
- bSDD lookup and classification support
- navigation through hierarchies and decomposition trees
- selection of catalog types and layers
- inspection of properties, documents, and associated attributes
- complementary visualization support through scientific libraries
- configuration profiles for labels, decomposition views, and LI Mapping

## Executive Structure

The project is organized into four main blocks:

1. `__init__.py`
Responsible for add-on registration, preferences, authentication, lifecycle, and
dependency loading.

2. `modules/`
Contains operators, panels, `PropertyGroup`s, and the central `OG_Properties`
aggregator.

3. `data/`
Contains support logic for bSDD, catalog, CDE, trees, configuration profiles,
and IFC utilities.

4. `resources/` and bundled libraries
Hold static data and packaged dependencies required at runtime, especially on
Windows.

## Technical Value

- clear separation between Blender UI and support logic
- `PropertyGroup` usage for state persistence and synchronization
- packaged dependencies to reduce installation friction
- domain-oriented architecture that supports incremental evolution
- documentation structure maintained directly in Markdown

## Risks and Attention Points

- behavior depends on the Blender environment and embedded Python versions
- changes to `modules/__init__.py`, `OG_Properties`, or build scripts directly
  affect add-on operation
- documentation must track every structural, registration, or installation-flow
  change
- bundled libraries can increase release size and require platform-specific
  validation

## Decision Guidance

For maintenance and evolution, the priority documents are:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/guides/`

For executive follow-up, this file should stay short and focused on purpose,
structure, value, and risk, without duplicating the technical detail from the
other documents.
