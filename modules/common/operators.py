import os
import platform
import subprocess
import bpy
import bonsai.tool as tool

from ...data.tree import refresh_tree


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