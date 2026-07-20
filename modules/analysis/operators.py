import bpy

from .service import apply_analysis_colors, invalidate_analysis_value_cache, reset_analysis_colors


def _set_legend_items(props, legend):
    props.analysis_legend.clear()
    for entry in legend:
        item = props.analysis_legend.add()
        item.label = entry["label"]
        item.color = entry["color"]


class Operator_analysis_apply_colors(bpy.types.Operator):
    bl_idname = "analysis.apply_colors"
    bl_label = "Apply colors"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
        props.analysis_legend.clear()
        try:
            invalidate_analysis_value_cache()
            result = apply_analysis_colors(props)
        except Exception as exc:
            props.analysis_status = str(exc)
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}

        props.analysis_status = (
            f"Colored {result['matched_count']} of {result['target_count']} objects "
            f"across {result['category_count']} group(s)."
        )
        _set_legend_items(props, result.get("legend", []))
        self.report({'INFO'}, props.analysis_status)
        return {'FINISHED'}


class Operator_analysis_reset_colors(bpy.types.Operator):
    bl_idname = "analysis.reset_colors"
    bl_label = "Reset colors"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        reset_analysis_colors()
        props = context.scene.og_props
        props.analysis_legend.clear()
        props.analysis_status = "Viewport object colors reset."
        self.report({'INFO'}, "Viewport object colors reset")
        return {'FINISHED'}
