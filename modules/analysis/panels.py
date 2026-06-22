import bpy

from .service import get_numeric_bounds, get_object_type_entry, get_pset_entry


class Panel_Analisys(bpy.types.Panel):

    bl_label        = "Analisys"
    bl_idname       = "VIEW3D_PT_og_analisys"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "InfoVis-Analisys"
    bl_options      = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='GRAPH')

    def draw(self, context):
        props = context.scene.og_props
        layout = self.layout
        layout.prop(props, "analysis_discipline", text="Discipline")
        layout.prop(props, "analysis_object_type", text="Element")

        object_type_entry = get_object_type_entry(props.analysis_discipline, props.analysis_object_type)
        if object_type_entry:
            box = layout.box()
            box.label(text=object_type_entry["label"], icon='INFO')
            description = object_type_entry["description"] or ""
            if description:
                box.label(text=description[:140])

        layout.prop(props, "analysis_pset", text="Property set")
        pset_entry = get_pset_entry(props.analysis_discipline, props.analysis_object_type, props.analysis_pset)
        if pset_entry:
            is_type_level = pset_entry.get("source") == "type"
            box = layout.box()
            box.label(text="Property set label is derived", icon='INFO')
            box.label(text=pset_entry["label"])
            box.label(text=f"Technical name: {pset_entry['technical_name']}")
            if is_type_level:
                box.label(text="Type-level: same value for every occurrence of this Element", icon='CON_CHILDOF')
            else:
                box.label(text="Occurrence-level: can vary per object", icon='HOLDOUT_OFF')

        layout.prop(props, "analysis_property", text="Property")
        layout.prop(props, "analysis_color_mode", text="Mode")

        if props.analysis_color_mode == 'exact':
            layout.prop(props, "analysis_value", text="Value")
        elif props.analysis_color_mode == 'range':
            bounds = get_numeric_bounds(props)
            if bounds is not None:
                info = layout.box()
                info.label(text=f"Detected numeric values: {bounds[2]}", icon='DRIVER_DISTANCE')
                info.label(text=f"Suggested range: {bounds[0]:.4g} to {bounds[1]:.4g}")
            row = layout.row(align=True)
            row.prop(props, "analysis_range_min", text="Min")
            row.prop(props, "analysis_range_max", text="Max")
        else:
            layout.label(text="Objects will be grouped by distinct values.", icon='COLOR')

        row = layout.row(align=True)
        row.operator("analysis.apply_colors", icon='BRUSH_DATA')
        row.operator("analysis.reset_colors", icon='LOOP_BACK')

        if props.analysis_status:
            box = layout.box()
            box.label(text="Status", icon='TEXT')
            box.label(text=props.analysis_status)
