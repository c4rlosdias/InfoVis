import os
import platform
import subprocess
import math
import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader
import bonsai.tool as tool
import bpy_extras.view3d_utils

from ...data.tree import refresh_tree


# ---------------------------------------------------------------------------
# IFC element name overlay — drawn in the 3D viewport next to the active obj
# ---------------------------------------------------------------------------

_ifc_label_handle = None


def _draw_ifc_label():
    context = bpy.context
    og_props = getattr(context.scene, 'og_props', None)
    if og_props is None:
        return
    
    if not og_props.show_ifc_label:
        return

    attrs = [item.attr_name for item in og_props.ifc_label_attributes if item.attr_name]
    if not attrs:
        return

    objs = context.selected_objects
    if not objs:
        return

    offset_x = og_props.label_offset_x
    offset_y = og_props.label_offset_y

    font_id = 0
    pad     = 6
    line_h  = 18
    blf.size(font_id, 14)

    for obj in objs:
        try:
            entity = tool.Ifc.get_entity(obj)
            if entity is None:
                continue
        except Exception:
            continue

        region = context.region
        rv3d   = context.region_data
        if region is None or rv3d is None:
            return

        coords_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(
            region, rv3d, obj.location
        )
        if coords_2d is None:
            continue

        obj_x, obj_y = coords_2d

        # --- Build text lines ---
        lines = []
        for attr_name in attrs:
            if '.' in attr_name:
                pset_name, _, prop_name = attr_name.partition('.')
                try:
                    import ifcopenshell.util.element as ifc_util
                    psets = ifc_util.get_psets(entity)
                    value = psets.get(pset_name, {}).get(prop_name)
                except Exception:
                    value = None
            else:
                value = getattr(entity, attr_name, None)
            if value is None:
                continue
            lines.append(f"{attr_name}: {value}")

        if not lines:
            continue

        # --- Measure ---
        n     = len(lines)
        max_w = max(blf.dimensions(font_id, ln)[0] for ln in lines)
        rw    = max_w + pad * 2
        rh    = n * line_h + pad

        # Rect bottom-left
        base_x = obj_x + offset_x
        base_y = obj_y + offset_y
        rx = base_x - pad
        ry = base_y - pad

        # Corner of the rect nearest to the object (anchor for leader line)
        anchor_x = rx      if offset_x >= 0 else rx + rw
        anchor_y = ry      if offset_y >= 0 else ry + rh

        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')

        # --- Leader line + arrowhead ---
        dx     = obj_x - anchor_x
        dy     = obj_y - anchor_y
        length = math.sqrt(dx * dx + dy * dy)
        if length > 1.0:
            ndx = dx / length
            ndy = dy / length
            px  = -ndy
            py  =  ndx

            # Line ends 10px before the object to leave room for arrowhead
            le_x = obj_x - ndx * 10
            le_y = obj_y - ndy * 10

            gpu.state.line_width_set(1.5)
            b_line = batch_for_shader(shader, 'LINES', {"pos": (
                (anchor_x, anchor_y), (le_x, le_y)
            )})
            shader.bind()
            shader.uniform_float("color", (0.85, 0.85, 0.85, 0.9))
            b_line.draw(shader)

            # Arrowhead (filled triangle)
            tip   = (obj_x,            obj_y)
            wing1 = (le_x + px * 5,    le_y + py * 5)
            wing2 = (le_x - px * 5,    le_y - py * 5)
            b_arrow = batch_for_shader(shader, 'TRIS', {"pos": (tip, wing1, wing2)})
            shader.bind()
            shader.uniform_float("color", (0.85, 0.85, 0.85, 0.9))
            b_arrow.draw(shader)

        # --- Background rect ---
        rv = ((rx, ry), (rx + rw, ry), (rx + rw, ry + rh), (rx, ry + rh))
        b_rect = batch_for_shader(shader, 'TRIS', {"pos": rv},
                                  indices=((0, 1, 2), (2, 3, 0)))
        shader.bind()
        shader.uniform_float("color", (0.08, 0.08, 0.08, 0.80))
        b_rect.draw(shader)

        # --- Border ---
        bv = (rv[0], rv[1], rv[2], rv[3], rv[0])
        b_border = batch_for_shader(shader, 'LINE_STRIP', {"pos": bv})
        shader.bind()
        shader.uniform_float("color", (0.60, 0.60, 0.60, 0.90))
        gpu.state.line_width_set(1.0)
        b_border.draw(shader)

        gpu.state.blend_set('NONE')
        gpu.state.line_width_set(1.0)

        # --- Text ---
        blf.enable(font_id, blf.SHADOW)
        blf.shadow(font_id, 3, 0.0, 0.0, 0.0, 0.8)
        blf.shadow_offset(font_id, 1, -1)
        blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
        for i, line in enumerate(lines):
            blf.position(font_id, base_x, base_y + (n - 1 - i) * line_h, 0)
            blf.draw(font_id, line)
        blf.disable(font_id, blf.SHADOW)


def register_ifc_label_overlay():
    global _ifc_label_handle
    if _ifc_label_handle is None:
        _ifc_label_handle = bpy.types.SpaceView3D.draw_handler_add(
            _draw_ifc_label, (), 'WINDOW', 'POST_PIXEL'
        )


def unregister_ifc_label_overlay():
    global _ifc_label_handle
    if _ifc_label_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_ifc_label_handle, 'WINDOW')
        _ifc_label_handle = None


dynamic_items = []


def reorder_element(context, index, chg):
    import ifcopenshell
    import bonsai.tool as tool

    props = context.scene.og_props
    model = tool.Ifc.get() 
    element = model.by_id(props.containers_show[index].id)
    if element is not None:
        if hasattr(element, "Nests") and element.Nests:
            parent_rel = element.Nests[0]
            elements = parent_rel.RelatedObjects
            element_index = elements.index(element)
            if chg + element_index < 0 or chg + element_index >= len(elements):
                return False
            ifcopenshell.api.nest.reorder_nesting(
                model,
                element,
                old_index=element_index,
                new_index=element_index + chg
            )
    return True        


def _open_in_browser(url):
    """Open a URL or file URI in the default browser. Works inside Blender."""
    try:
        if platform.system() == 'Windows':
            os.startfile(url)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
    except Exception:
        import webbrowser
        webbrowser.open(url)


def get_options(self, context):    
    return dynamic_items


class Operator_expand_tree(bpy.types.Operator):
    """"""
    bl_idname  = "element.expand_tree"
    bl_label   = "Expand item tree"
    bl_options = {"REGISTER", "UNDO"}

    index    : bpy.props.IntProperty(name="index")
    property : bpy.props.StringProperty(name="property")

    def execute(self, context):                
        props = context.scene.og_props
        item = getattr(props, self.property)[self.index]
        item.is_expanded = True
        imin = False
        level = item.level
        for classe in getattr(props, self.property):                 
            if classe.index > item.index:                 
                if classe.level == level + 1:
                    classe.is_hidden = False 
                    classe.is_expanded = False 
                    imin = True
                if classe.level <= level and imin:
                    break
        refresh_tree(context, property=self.property)  
        return {"FINISHED"}   
     

class Operator_contract_tree(bpy.types.Operator):
    """"""
    bl_idname  = "element.contract_tree"
    bl_label   = "Contract item tree"
    bl_options = {"REGISTER", "UNDO"}

    index    : bpy.props.IntProperty(name="index")
    property : bpy.props.StringProperty(name="property")

    def execute(self, context):                
        props = context.scene.og_props       
        item = getattr(props, self.property)[self.index]               
        level = item.level
        item.is_expanded = False
        for element in getattr(props, self.property):
            if element.index > self.index:
                if element.level > level:
                    element.is_hidden = True 
                    element.is_expanded = False              
                else:
                    break
        refresh_tree(context, property=self.property)          
        return {"FINISHED"} 


class Columns(bpy.types.PropertyGroup):
    name     : bpy.props.StringProperty(name='column name')
    selected : bpy.props.BoolProperty(name='selected', default=True)


class ErrorMessage(bpy.types.Operator):
    bl_idname = "og.error_message"
    bl_label = "Erro!"

    message: bpy.props.StringProperty()
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text='ERROR:')

        row = layout.row()
        row.label(text=self.message, icon='ERROR')

class Select_object(bpy.types.Operator):
    bl_idname = "element.select_object"
    bl_label = "Select Object"

    id: bpy.props.IntProperty()

    def execute(self, context):
        if self.id is None:
            self.report({'WARNING'}, "No object ID provided.")
            return {'CANCELLED'}
        obj = tool.Ifc.get_object_by_identifier(self.id)
        if obj:
            context.selected_objects.clear()
            context.view_layer.objects.active = obj
            obj.select_set(True)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, f"Object '{self.obj_name}' not found.")
            return {'CANCELLED'}