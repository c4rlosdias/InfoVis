# Panels: modules/*/panels.py

## Overview

The Add-on UI panels are distributed across the domain modules inside
`modules/`. Each module contains its own `panels.py` with the panels, UILists,
and layouts for that domain.

| Module | Responsibility |
|--------|----------------|
| `modules/dictionary/panels.py` | bSDD panel and class/property UILists |
| `modules/decomposition/panels.py` | Decomposition panel and tree UILists |
| `modules/catalog/panels.py` | Catalog panel, LI Mapping panel, product UILists, LI UILists, and layer UIList |
| `modules/connections/panels.py` | Connection panel |
| `modules/props/panels.py` | IFC properties panel |
| `modules/types/panels.py` | Constructive type panel |
| `modules/settings/panels.py` | Settings panel, IFC label UIList, and decomposition-view UILists |
| `modules/analysis/panels.py` | Analysis coloring panel |

## Helper Functions

### `_label_multiline(context, text, parent)`

Splits long text into multiple UI labels.

```python
def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)
```

### `get_product_attribute(context, index, attribute)`

Returns a specific product attribute by index.

### `_draw_catalog_type_tree(layout, item, icon)`

Draws one catalog tree item, including indentation, expand/collapse controls,
quantity, unit, selection action, and layer-report action.

### `_active_decomposition_view(props)` and `_active_decomposition_relation(props, view)`

Return the active decomposition view and relation in the settings panel.

## Sidebar Categories

The panels are organized into these Blender 3D Viewport sidebar categories:

| Category | Panels |
|----------|--------|
| `InfoVis-Dictionary` | `Subsea Classes` |
| `InfoVis-Occurrence` | `Decompositions`, `Properties`, `Constructive Type`, `Connect Elements` |
| `InfoVis-Catalog` | `Catalog`, `LI Mapping` |
| `InfoVis-Analysis` | `Analysis` |
| `InfoVis-Settings` | `Settings` |

## Authentication

Panels and operators that mutate IFC data check editor authentication through
`auth.is_authenticated()`. Read-only sections remain available, while editing
controls are hidden or disabled until the user logs in through the Add-on
preferences.

Typical pattern:

```python
from ... import auth

class SomePanel(bpy.types.Panel):
    def draw(self, context):
        layout = self.layout
        if not auth.is_authenticated():
            layout.label(text="Login required")
            return
        # editable content
```

## Panel_Connect: Subsea Classes

Defined in `modules/dictionary/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_connect` |
| `bl_category` | `InfoVis-Dictionary` |
| `bl_label` | `Subsea Classes` |
| `bl_order` | `0` |
| Mode | Object Mode |
| Default | Closed |

Features:

1. Selects a bSDD dictionary.
2. Runs `bsdd.get_class` through `get classes from bSDD`.
3. Displays classes with `BIM_UL_classes`.
4. Opens class URIs in the browser.
5. Loads class metadata with `Get Class Information`.
6. Loads class properties with `Get Class Properties`.
7. Displays selected property metadata.
8. Adds selected properties as Pset templates.
9. Exports IDS files.

## Panel_Decompositions

Defined in `modules/decomposition/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_decompositions` |
| `bl_category` | `InfoVis-Occurrence` |
| `bl_label` | `Decompositions` |

Features:

1. Loads the configured IFC decomposition tree.
2. Uses the selected `Tree Type`.
3. Draws a hierarchy through `tree.draw_tree()`.
4. Expands or collapses all items.
5. Exports the tree to `.xlsx`.
6. Selects individual elements or elements with children.
7. Moves elements between parents when authenticated.
8. Reorders leaf elements when authenticated.

## Panel_Connect_Elements

Defined in `modules/connections/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_connect_elements` |
| `bl_category` | `InfoVis-Occurrence` |
| `bl_label` | `Connect Elements` |

Features:

1. Lists connections for the active object.
2. Lets the user pick objects through eyedropper-style selection.
3. Creates IFC connection relationships.
4. Removes existing connections.

Supported connection relationship types include:

- `IfcRelConnectsPorts`
- `IfcRelConnectsElements`
- `IfcRelConnectsWithRealizingElements`

## Panel_Catalog

Defined in `modules/catalog/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_catalog` |
| `bl_category` | `InfoVis-Catalog` |
| `bl_label` | `Catalog` |

Features:

1. Runs `catag.load_products` through `Load type products`.
2. Displays type products in `BIM_UL_products`.
3. Shows quantity and unit for leaf items.
4. Selects all instances of a type.
5. Opens an HTML layer report.
6. Displays layers with `BIM_UL_layers`.
7. Exports quantities with `Export Quantities`.

## Panel_LI_Mapping

Defined in `modules/catalog/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_li_mapping` |
| `bl_category` | `InfoVis-Catalog` |
| `bl_label` | `LI Mapping` |

Features:

1. Loads `resources/li_mapping.json` with `Load`.
2. Saves changes back to the JSON with `Save`.
3. Exports the Item List with `Export LI`.
4. Edits mapping header fields: `Schema`, `Reference Sheet`, and `Description`.
5. Displays LI columns with `BIM_UL_li_mapping_columns`.
6. Adds or removes columns.
7. Edits common column fields: `Column`, `Source`, and `Notes`.
8. Shows guided source fields according to `source_type`.
9. Provides a bSDD picker for `ifc_property` and `manual` sources.
10. Adds/removes extra source fields through `BIM_UL_li_mapping_source_items`.
11. Edits support tables through `BIM_UL_li_support_tables` and
    `BIM_UL_li_support_table_rows`.

Guided source behavior:

| Source type | Fields displayed |
|-------------|------------------|
| `ifc_attribute` | `Class`, `Attribute`, `Fallback`, `Format` |
| `ifc_property` | `Class`, `Pset`, `Property`, `Allowed Values`, bSDD picker |
| `manual` | `Class`, `Pset`, `Property`, `Allowed Values`, bSDD picker |
| `spatial` | `Level (IFC class)`, `Attribute` |
| `aggregation_parent` | `Level (1=direct parent, 2=grandparent, ...)`, `Attribute`, `Fallback` |
| `ifc_class` | `Attribute`, `Mapping Table` |
| `ifc_quantity` | `Modo`, and when mapping: `Mapping Table`, `Selected By` |
| `computed` | `Selected By`, `Template Table`, `Derived From`, `Method`, `Format` |
| `not_applicable` | no guided source field |

## Panel_Properties

Defined in `modules/props/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_properties` |
| `bl_category` | `InfoVis-Occurrence` |
| `bl_label` | `Properties` |

Features:

1. Shows property sets for the active object.
2. Loads properties with `props.load_properties`.
3. Separates occurrence properties and inherited type properties.
4. Toggles property descriptions.
5. Edits scalar, list, enum, and table values when authenticated.
6. Shows and edits IFC document references when authenticated.
7. Opens document URLs or local paths.
8. Generates charts from CSV/table data.
9. Toggles table visibility and axis inversion.
10. Adds `Pset.Property` fields to viewport IFC labels.

## Panel_Types: Constructive Type

Defined in `modules/types/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_types` |
| `bl_category` | `InfoVis-Occurrence` |
| `bl_label` | `Constructive Type` |

Features:

1. Shows the constructive IFC type related to the active object.
2. Displays `ElementType`, type name, and description.
3. Shows type documents.
4. Selects all occurrences of the same type.
5. Opens the layer report for the type.
6. Selects type layers/components.
7. Selects the IFC type object.

## Panel_Settings: Settings

Defined in `modules/settings/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_settings` |
| `bl_category` | `InfoVis-Settings` |
| `bl_label` | `Settings` |

Features:

1. Imports and exports the portable InfoVis config profile.
2. Toggles `Show IFC label`.
3. Edits `Fields to display` with `BIM_UL_ifc_label_attrs`.
4. Adds IFC attributes to labels.
5. Removes label fields.
6. Adjusts label display text and offset.
7. Loads decomposition views.
8. Saves decomposition views.
9. Resets views to defaults.
10. Adds, duplicates, or removes views.
11. Edits view ID, label, root IFC class, and relation rows.

## Panel_Analysis

Defined in `modules/analysis/panels.py`.

| Property | Value |
|----------|-------|
| `bl_idname` | `VIEW3D_PT_og_color_mapping_analysis` |
| `bl_category` | `InfoVis-Analysis` |
| `bl_label` | `Color Mapping Analysis` |

Features:

1. Selects `Discipline`, `Element`, `Property set`, and `Property`.
2. Shows object type and property set metadata.
3. Selects color mode:
   - distinct values;
   - exact value;
   - numeric range.
4. Suggests numeric range bounds when possible.
5. Applies analysis colors.
6. Resets colors.
7. Displays a legend and status text.

## UIList Classes

| Class | Use |
|-------|-----|
| `BIM_UL_ifc_properties` | IFC property entries |
| `BIM_UL_property_class` | Property classes |
| `BIM_UL_classes` | bSDD classes with hierarchy indentation |
| `BIM_UL_class_prop` | Class properties |
| `BIM_UL_decomposition` | IFC decomposition items |
| `BIM_UL_tree` | Generic tree list |
| `BIM_UL_products` | Product/type tree |
| `BIM_UL_layers` | Type layers/components |
| `BIM_UL_li_mapping_columns` | LI mapping columns |
| `BIM_UL_li_mapping_source_items` | LI mapping extra source fields |
| `BIM_UL_li_support_tables` | LI mapping support tables |
| `BIM_UL_li_support_table_rows` | Rows inside a LI support table |
| `BIM_UL_ifc_label_attrs` | Viewport label fields |
| `BIM_UL_decomposition_views` | Decomposition views |
| `BIM_UL_decomposition_view_relations` | Relations for one decomposition view |

### UIList Pattern

```python
class BIM_UL_classes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # indentation based on item.level
        # expansion icon when item.has_children
        # item name and action buttons
```

## Interaction Flow

```text
User clicks "get classes from bSDD"
        |
        v
Operator bsdd.get_class runs
        |
        v
Connects to the bSDD server
        |
        v
ifc_utils.build_classes() builds the hierarchy
        |
        v
tree.refresh_classes() filters visible classes
        |
        v
Panel redraws
        |
        v
BIM_UL_classes shows the updated list
```

## Layout Patterns

### Box Layout

```python
box = layout.box()
row = box.row(align=True)
row.label(text="Title", icon='INFO')
```

### Template List

```python
self.layout.template_list(
    "BIM_UL_classes",
    "",
    props,
    "classes_shown",
    props,
    "active_class_index",
    rows=10
)
```

### Operator with Property

```python
op = row.operator("bsdd.get_class_info", text="Info")
op.uri = active_class.uri
```

## Integration with Other Modules

- `modules/og_properties.py`: defines `OG_Properties` and callbacks used by
  panels.
- `modules/*/properties.py`: defines domain PropertyGroups referenced by
  UILists.
- `modules/*/operators.py`: provides the operators called by panel buttons.
- `data/tree.py`: provides `draw_tree()` and `refresh_*()` helpers.
- `data/ifc_utils.py`: provides IFC utility functions.
- `data/decomposition_views.py`: provides settings data for decomposition
  views.
- `auth`: checks authentication before protected editing controls are shown.
