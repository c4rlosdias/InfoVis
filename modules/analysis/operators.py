import bpy

from .service import apply_analysis_colors, invalidate_analysis_value_cache, reset_analysis_colors


class Operator_analysis_apply_colors(bpy.types.Operator):
    bl_idname = "analysis.apply_colors"
    bl_label = "Apply colors"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.og_props
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
        self.report({'INFO'}, props.analysis_status)
        return {'FINISHED'}


class Operator_analysis_reset_colors(bpy.types.Operator):
    bl_idname = "analysis.reset_colors"
    bl_label = "Reset colors"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        reset_analysis_colors()
        context.scene.og_props.analysis_status = "Viewport object colors reset."
        self.report({'INFO'}, "Viewport object colors reset")
        return {'FINISHED'}