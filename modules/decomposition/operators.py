import bpy
import ifcopenshell
import bonsai.tool as tool

from ...data.tree import (
    load_contained_elements_by_decomposition,
    refresh_container,
    move_to_assembly,
)
from ..common.operators import reorder_element


class Operator_decomposition_load(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.load"
    bl_label   = "Load element decomposition"
    bl_options = {"REGISTER", "UNDO"}

    all_expanded : bpy.props.BoolProperty(name="all_expanded", default=False)

    def execute(self, context):   
        props = context.scene.og_props        
        model = tool.Ifc.get()
        elements = model.by_type('IfcProject')
        
        if len(elements) > 0:
            for element in elements: 
                load_contained_elements_by_decomposition(element, 'elements_containers', context)  
            i = 0          
            for element in props.elements_containers:
                element.index = i
                element.is_expanded = self.all_expanded
                element.is_hidden = not self.all_expanded if element.level!=1 else False                
                i += 1   
            refresh_container(context)
        return {"FINISHED"} 


class Operator_decomposition_select_element(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.select_element"
    bl_label   = "Select object"
    bl_options = {"REGISTER", "UNDO"}    
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):  
        try:
            props = context.scene.og_props       
            item = props.elements_containers[self.index]   

            model = tool.Ifc.get()
            if model is None:
                self.report({'ERROR'}, "No IFC model loaded")
                return {"CANCELLED"}

            ifc_element = model.by_id(item.id)
            if ifc_element is None:
                self.report({'ERROR'}, f"Element with id {item.id} not found")
                return {"CANCELLED"}

            obj = tool.Ifc.get_object(ifc_element)  
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
 
            return {"FINISHED"} 
        except Exception as ex:
            print(ex)
            self.report({'ERROR'}, str(ex))
            return {"CANCELLED"}


class Operator_decomposition_select_components(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.select_components"
    bl_label   = "Select objects"
    bl_options = {"REGISTER", "UNDO"}    
    index : bpy.props.IntProperty(name="index")

    def sel_objects(self, ifc_element):         
        objs = [] 
        objs.append(tool.Ifc.get_object(ifc_element))
        if len(ifc_element.IsNestedBy) > 0:
            for element in ifc_element.IsNestedBy[0].RelatedObjects:
                    if len(element.IsNestedBy)>0 or len(element.IsDecomposedBy)>0: 
                        objs += self.sel_objects(element)
                    else:
                        objs.append(tool.Ifc.get_object(element))
                    
        if len(ifc_element.IsDecomposedBy) > 0:
            for element in ifc_element.IsDecomposedBy[0].RelatedObjects:
                if len(element.IsNestedBy)>0 or len(element.IsDecomposedBy)>0: 
                        objs += self.sel_objects(element)
                else:
                    objs.append(tool.Ifc.get_object(element))
        print(objs)
        return objs

    def execute(self, context):   
        props = context.scene.og_props       
        item =  props.elements_containers[self.index] 
        item.is_selected = not item.is_selected                           
        model = tool.Ifc.get()        
        ifc_element = model.by_id(item.id) 
        print(ifc_element)
        objs = self.sel_objects(ifc_element) 
        for obj in objs:
            if obj:
                obj.select_set(item.is_selected)            
                if item.is_selected:
                    bpy.context.view_layer.objects.active =  obj
                else:
                    obj_i = context.selected_objects            
                    bpy.context.view_layer.objects.active =  obj_i[0] if len(obj_i) > 0 else None 
        

        refresh_container(context) 
        return {"FINISHED"} 
    

class Operator_decomposition_move(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.move"
    bl_label   = "Move object to selected parent"
    bl_options = {"REGISTER", "UNDO"}    
    index : bpy.props.IntProperty(name="index")
    type  : bpy.props.StringProperty(name="type", default="Nests")

    def execute(self, context):   
        props = context.scene.og_props       
        model = tool.Ifc.get() 
        parent_id =  props.elements_containers[self.index].id           
        entity_parent = model.by_id(parent_id) 
        children_id = props.containers_show[props.active_element_index].id        
        entity_children =  model.by_id(children_id)        

        if entity_parent != entity_children:     
            print(f'entity_parent: {entity_parent}')
            print(f'entity_children: {entity_children}')
            move_to_assembly(entity_parent, entity_children, self.type)
            self.report({'OPERATOR'}, 'Moved successfully!')       
            refresh_container(context) 
            bpy.ops.decomposition.load(all_expanded=True)
            return {"FINISHED"}
        else:
            self.report({'ERROR'}, 'Cannot move element to itself or its children!')
            return {"CANCELLED"}


class Operator_decomposition_chg_order(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.chg_order"
    bl_label   = "Move element"
    bl_options = {"REGISTER", "UNDO"}    
    
    index : bpy.props.IntProperty(name="index")
    chg   : bpy.props.IntProperty(name="change", default=-1)

    def execute(self, context):      
        props = context.scene.og_props     
        id = props.containers_show[self.index].id
        if reorder_element(context, self.index, self.chg):
            bpy.ops.decomposition.load(all_expanded=True)
            for c in props.containers_show:
                if c.id == id:  
                    props.active_element_index = c.index
                    break

        return {"FINISHED"}
