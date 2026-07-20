# InfoVis

Central documentation for the InfoVis Blender add-on.

## Overview

The project is distributed as a Python add-on with its entry point in
`__init__.py`, functional organization in `modules/`, and support logic in
`data/`. This documentation reflects the repository structure, the Blender
installation flow, and the current release process.

> Recommended starting point for maintenance: read Architecture first, then
> Development, then the technical guide for the domain you plan to change.

## What You Will Find Here

- add-on architecture and initialization flow
- Blender add-on user guide and panel workflows
- development and release guide
- reference material for operators, panels, properties, and the data layer
- glossary of recurring terms and components
- supporting material for documentation maintenance and follow-up

## Reading Paths

| Goal | Start here | Next step |
|------|------------|-----------|
| Use the add-on in Blender | [User Guide](guides/GUIA_DE_UTILIZACAO.md) | [Glossary](reference/GLOSSARY.md) |
| Configure the Item List | [LI Mapping Guide](guides/LI_MAPPING_GUIDE.md) | [User Guide](guides/GUIA_DE_UTILIZACAO.md) |
| Understand the add-on structure | [Architecture](ARCHITECTURE.md) | [Glossary](reference/GLOSSARY.md) |
| Implement code changes | [Development](DEVELOPMENT.md) | Guides in `guides/` |
| Review operators and panels | [Operators](guides/OPERATORS_DOCUMENTATION.md) | [Panels](guides/PANELS_DOCUMENTATION.md) |
| Review the data model | [Properties](guides/PROPERTIES_DOCUMENTATION.md) | [Data](guides/DATA_DOCUMENTATION.md) |
| Get executive context | [Executive Summary](extra/SUMARIO_EXECUTIVO.md) | [Next Steps](extra/PROXIMOS_PASSOS.md) |

## Start by Role

### To Understand the Project

- [Architecture](ARCHITECTURE.md)
- [Glossary](reference/GLOSSARY.md)

### To Develop

- [Development](DEVELOPMENT.md)
- [Operators](guides/OPERATORS_DOCUMENTATION.md)
- [Panels](guides/PANELS_DOCUMENTATION.md)
- [Properties](guides/PROPERTIES_DOCUMENTATION.md)
- [Data](guides/DATA_DOCUMENTATION.md)

### To Install and Validate Quickly

1. read the [User Guide](guides/GUIA_DE_UTILIZACAO.md) for the general usage flow
2. generate a zip with `build_release.bat` or `build_release.sh`
3. install the add-on in Blender with `Install from Disk`
4. validate it with `Example/C3388.8_UN-31.ifc`

### To Review Documentation

1. validate the main documents in this folder
2. run `mkdocs build --strict` from the repository root
3. review the generated navigation in `site/`

### For Executive Context or Follow-Up

- [Executive Summary](extra/SUMARIO_EXECUTIVO.md)
- [Next Steps](extra/PROXIMOS_PASSOS.md)
- [Documentation Completed](extra/DOCUMENTACAO_CONCLUIDA.md)

## Quick Structure

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- data/
|-- docs/
|-- modules/
|-- resources/
`-- wheels/
```

## Publishing the Documentation

The `docs/` folder can be published with MkDocs using the configuration in
`mkdocs.yml`.

Run the commands from the repository root.

### Local Environment

Basic commands:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

For a static build:

```powershell
mkdocs build
```

If the repository is hosted on GitHub, the `.github/workflows/docs.yml`
workflow can automatically publish the documentation to GitHub Pages for the
configured branch.

## Quick Checklist

- `README.md` aligned with `docs/`
- `mkdocs build --strict` without blocking warnings
- local links resolve correctly
- documentation workflow points to the active branch
