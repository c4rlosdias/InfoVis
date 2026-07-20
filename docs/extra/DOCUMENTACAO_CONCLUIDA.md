# Documentation Completed

## Status

This file records that the project's main documentation base has been
consolidated and updated to match the current `InfoVis` repository structure.

Documents that should be treated as primary sources:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/guides/OPERATORS_DOCUMENTATION.md`
- `docs/guides/PANELS_DOCUMENTATION.md`
- `docs/guides/PROPERTIES_DOCUMENTATION.md`
- `docs/guides/DATA_DOCUMENTATION.md`
- `docs/reference/GLOSSARY.md`

## What Was Adjusted

- removed references to files that no longer exist, such as
  `README_DOCUMENTATION.md`, `DOCUMENTATION.md`, and `INDICE_COMPLETO.md`
- aligned the product name to `InfoVis`
- reviewed the real repository structure, based on `modules/`, `data/`,
  `resources/`, and `wheels/`
- corrected the Blender add-on installation and packaging flow
- added architecture and maintenance references that match the current codebase

## Expected Result

After this review, the main documentation should:

- correctly guide installation and usage of the add-on
- reflect the real class registration and modular code organization
- serve as a technical onboarding base for maintenance and evolution
- support MkDocs publication without broken navigation

## Notes

- `docs/extra/` should be read as complementary material, not as the normative
  source for architecture
- whenever there is a structural change in the project, update
  `README.md`, `docs/ARCHITECTURE.md`, and `docs/DEVELOPMENT.md` first
- the guides in `docs/guides/` should follow relevant changes in operators,
  panels, properties, and the data layer

## Recommended Next Maintenance

1. review the documentation whenever `bl_info`, the release flow, or module
   structure changes
2. add visual interface examples when the panel layout stabilizes
3. keep supporting files in `docs/extra/` short and historically accurate
