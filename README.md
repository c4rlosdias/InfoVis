# InfoVis

InfoVis is an open-source Blender add-on, developed together with IfcOpenShell, with the goal of making the information contained in IFC files for the oil and gas industry clear and accessible. The tool was created in the context of the IFC schema extension project for subsea engineering, developed by Fundação CERTI in partnership with Petrobras, and enables visualization and analysis of the data mapped in this standardization effort.

More than a viewer, InfoVis was designed as an open tool intended to serve the entire sector supply chain. Manufacturers, designers, integrators, and operators often face barriers to technical information access because they rely on proprietary solutions and closed formats. By adopting the OpenBIM standard and providing a free customization that translates the IFC data structure into understandable visualizations, InfoVis reduces these barriers and promotes interoperability across the different links of the chain, from component suppliers to subsea asset operators.

This initiative is aligned with Brazil's Innovation Law (Law No. 10,973/2004, updated by the Legal Framework for Science, Technology, and Innovation - Law No. 13,243/2016), which encourages cooperation between Scientific, Technological, and Innovation Institutions (ICTs) and companies to develop technological solutions of national interest. The partnership between CERTI and Petrobras materializes this spirit: it transforms research and development investment into an open technological asset whose benefits extend beyond the institutions involved, strengthening the competitiveness and technological capabilities of the entire Brazilian oil and gas ecosystem.

## Overview

The project is distributed as a Python add-on for Blender. The main entry point is `__init__.py`, which registers preferences, authentication operators, `OG_Properties`, and all classes loaded by `modules/get_classes()`.

Main capabilities:

- reading and navigating IFC data
- querying classes and properties through bSDD
- viewing decomposition and element trees
- selecting catalog types and layers
- editing and inspecting properties and documents
- displaying IFC attributes in the viewport

## Requirements

- Blender 5.0 or later
- Blender embedded Python compatible with the target environment
- Windows, Linux, or macOS

Dependency notes:

- on Windows, the add-on uses packaged libraries in `libs311/` and `libs313/`
- on Linux and macOS, missing packages can be installed into Blender's Python when the add-on starts

## Installation

### Using a zipped release

1. Generate or obtain a release `.zip` file.
2. In Blender, open `Edit > Preferences > Add-ons`.
3. Click `Install from Disk`.
4. Select the `.zip` file generated in `releases/`.
5. Enable the `InfoVis` add-on.

### Development installation

1. Clone or copy this repository into a working directory.
2. Generate a release package with one of the scripts below:

```powershell
.\build_release.bat release-name
```

```bash
./build_release.sh release-name
```

3. Install the generated zip in Blender using the `Install from Disk` flow.

If you prefer installing without a zip during development, copy the project folder to Blender's add-ons directory, keeping the current structure and package name consistent with `InfoVis`.

## Release Build

The build scripts copy the required files to `releases/InfoVis/` and generate a final zip in `releases/<name>.zip`.

Files and folders included in the package:

- `__init__.py`
- `auth.py`
- `modules/`
- `data/`
- `libs311/`
- `libs313/`
- `resources/`

## Repository Structure

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- build_release.bat
|-- build_release.sh
|-- data/
|-- docs/
|-- Example/
|-- libs311/
|-- libs313/
|-- modules/
|-- releases/
`-- resources/
```

### Main modules

- `modules/dictionary/`: bSDD integration and class properties
- `modules/decomposition/`: decomposition tree and IFC navigation
- `modules/catalog/`: product types and layers
- `modules/connections/`: creating and removing object connections
- `modules/props/`: properties, documents, and views
- `modules/types/`: types panel
- `modules/settings/`: add-on information and visual settings
- `modules/common/`: shared utilities
- `modules/og_properties.py`: central application property group

### Support layers

- `data/bsdd.py`: client for the bSDD API
- `data/catalog.py`: catalog reading and IFC import
- `data/cde.py`: CDE integration
- `data/tree.py`: tree refresh and callbacks
- `data/ifc_utils.py`: helper functions for IFC
- `resources/`: supporting JSON files

## Documentation

Main documents:

- [docs/guides/GUIA_DE_UTILIZACAO.md](docs/guides/GUIA_DE_UTILIZACAO.md): using the add-on in Blender, panels, flows, and exports
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): add-on architecture, initialization flow, and module organization
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): setup, workflow, and maintenance
- [docs/reference/GLOSSARY.md](docs/reference/GLOSSARY.md): recurring terms and conventions

Detailed guides:

- [docs/guides/LI_MAPPING_GUIDE.md](docs/guides/LI_MAPPING_GUIDE.md)
- [docs/guides/OPERATORS_DOCUMENTATION.md](docs/guides/OPERATORS_DOCUMENTATION.md)
- [docs/guides/PANELS_DOCUMENTATION.md](docs/guides/PANELS_DOCUMENTATION.md)
- [docs/guides/PROPERTIES_DOCUMENTATION.md](docs/guides/PROPERTIES_DOCUMENTATION.md)
- [docs/guides/DATA_DOCUMENTATION.md](docs/guides/DATA_DOCUMENTATION.md)

Additional documents:

- `docs/extra/` contains managerial supporting materials and documentation history

### Publishing with MkDocs

The repository already includes an initial base for publishing documentation:

- `mkdocs.yml`
- `docs/index.md`
- `requirements-docs.txt`

To publish locally:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

To generate the static site:

```powershell
mkdocs build
```

If the repository is hosted on GitHub, the workflow in `.github/workflows/docs.yml` can automatically publish the documentation through GitHub Pages.

## Development Flow

1. Adjust code in `modules/`, `data/`, or `resources/`.
2. Reinstall or reload the add-on in Blender.
3. Validate affected panels and operators with a sample IFC file.
4. Generate a new release zip when needed.

## Example Files

- `Example/C3388.8_UN-31.ifc`: IFC file for manual tests
- `graphic.html` and `layers.html`: supporting visualization artifacts

## Notes

- `requirements.txt` lists Python dependencies for the project, but Blender packaging also depends on the embedded libraries in `libs311/` and `libs313/`.
- The name displayed in Blender is defined in `bl_info` inside `__init__.py`.

