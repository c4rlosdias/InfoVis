# Next Steps

## Purpose

This document lists the most useful actions for keeping the InfoVis
documentation consistent with add-on evolution.

## Immediate Priority

1. validate in Blender the workflows described in `README.md` and
   `docs/DEVELOPMENT.md`
2. review whether the documented panels and operators still match current
   behavior
3. update examples whenever the interface, naming, or release flow changes

## Short Term

### 1. Add Visual Evidence

- include screenshots of the main add-on panels
- document the installation flow using the zip generated in `releases/`
- show an example with `Example/C3388.8_UN-31.ifc`

### 2. Refine Technical Onboarding

- add a short first-contribution walkthrough
- document registration conventions in `modules/__init__.py`
- include small examples of extending `OG_Properties`

### 3. Improve Traceability

- connect version changes in `bl_info` with relevant documentation changes
- record in the release process when bundled libraries are changed

## Medium Term

### 1. Documentation Governance

Keep the Markdown documentation set synchronized with code changes.

Main documents:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/guides/*.md`
- `docs/reference/GLOSSARY.md`

### 2. Automated Markdown Validation

- add internal link checks
- validate that referenced files exist
- standardize naming for headings and main sections

## Long Term

- maintain a documentation changelog per add-on version
- split user guides and maintenance guides if the documentation base grows
- generate demo material for new team members

## Maintenance Checklist

- [ ] add-on folder structure changed
- [ ] build or release process changed
- [ ] displayed name in `bl_info` changed
- [ ] Blender installation flow changed
- [ ] `OG_Properties` composition changed
- [ ] operators, panels, or `PropertyGroup`s were reorganized

If any item above occurs, review at least:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`

## Main References

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/reference/GLOSSARY.md`
