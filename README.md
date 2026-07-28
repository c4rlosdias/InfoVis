# InfoVis

InfoVis is an open-source Blender add-on, developed together with IfcOpenShell, with the goal of making the information contained in IFC files for the oil and gas industry clear and accessible. The tool was created in the context of the IFC schema extension project for subsea engineering, developed by Fundação CERTI in partnership with Petrobras, and enables visualization and analysis of the data mapped in this standardization effort.

More than a viewer, InfoVis was designed as an open tool intended to serve the entire sector supply chain. Manufacturers, designers, integrators, and operators often face barriers to technical information access because they rely on proprietary solutions and closed formats. By adopting the OpenBIM standard and providing a free customization that translates the IFC data structure into understandable visualizations, InfoVis reduces these barriers and promotes interoperability across the different links of the chain, from component suppliers to subsea asset operators.

This initiative is aligned with Brazil's Innovation Law (Law No. 10,973/2004, updated by the Legal Framework for Science, Technology, and Innovation - Law No. 13,243/2016), which encourages cooperation between Scientific, Technological, and Innovation Institutions (ICTs) and companies to develop technological solutions of national interest. The partnership between CERTI and Petrobras materializes this spirit: it transforms research and development investment into an open technological asset whose benefits extend beyond the institutions involved, strengthening the competitiveness and technological capabilities of the entire Brazilian oil and gas ecosystem.

## Short description

Explore and analyze oil and gas IFC models using Bonsai.

## Description

InfoVis is a Blender extension for exploring, visualizing, and analyzing information stored in IFC models for the oil and gas industry.

The extension integrates with the active Bonsai IFC session and provides specialized tools for navigating model decomposition, inspecting IFC properties and types, exploring connections, querying bSDD dictionaries, managing catalogs, and performing engineering-oriented analyses.

InfoVis is designed as a companion extension for Bonsai 0.8.5 and requires Bonsai to be installed and enabled. It does not replace Bonsai or maintain a separate IFC session.

## Main features

- IFC spatial and functional decomposition views
- Property set, attribute, and type inspection
- IFC element and connection visualization
- Oil and gas equipment catalog tools
- bSDD dictionary integration
- Spreadsheet import and export
- Engineering data analysis and visualization
- CDE integration for uploading and downloading IFC information
- Integration with the IFC model currently open in Bonsai

## Requirements

- Blender 5.1 or newer
- Windows x64
- Bonsai 0.8.5 installed and enabled

## Installation

1. Install and enable Bonsai 0.8.5.
2. Install the InfoVis extension package.
3. Enable InfoVis in Blender.
4. Open or create an IFC project using Bonsai.
5. Access the InfoVis tools from the 3D View sidebar.

## Permissions

### Network

Used for optional CDE and bSDD integrations, including uploading and downloading IFC-related information.

### Files

Used to read and write spreadsheet files selected by the user and to work with IFC-related project data.

### Clipboard

Used only when the user explicitly copies diagnostic or error information.

## Notes for reviewers

InfoVis depends on the Python package distributed with Bonsai 0.8.5 and accesses the active Bonsai IFC session through its public Python modules.

The extension bundles the required Python wheels using the Blender Extensions manifest mechanism. Packages already provided by Blender 5.1—including NumPy, Requests, Packaging, Certifi, Charset Normalizer, IDNA, urllib3, Click, attrs, importlib-metadata, typing-extensions, and zipp—are intentionally not bundled.

Wheels shared with Bonsai use the exact versions distributed by Bonsai 0.8.5. This prevents binary package conflicts in Blender's shared extension environment, particularly for pandas, Pillow, IfcOpenShell, FontTools, ElementPath, and XMLSchema.

The package was validated with Blender 5.1 on Windows x64. A clean installation test was performed by installing and enabling Bonsai 0.8.5 first, followed by InfoVis.

## License

InfoVis is distributed under the GNU General Public License, version 3.0 or later (`GPL-3.0-or-later`).