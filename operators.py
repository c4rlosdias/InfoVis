import bonsai.core
import bonsai.core.geometry
import bonsai.core.material
import bonsai.core.type
import webbrowser
import json
import base64
from io import BytesIO
import os
import bpy
from ifctester import ids
from tqdm import tqdm
import ifcopenshell.util.element as element
import ifcopenshell.util.representation as representation
import ifcopenshell.util.selector as selector
import ifcopenshell.api.root.create_entity as create_entity
import ifcopenshell.api.material as material
import ifcopenshell.api.geometry as geometry
import ifcopenshell.api.style as style
import ifcopenshell
import webbrowser
from .data import *
import bonsai.core as core
import bonsai
import bonsai.tool as tool
from bonsai.bim import import_ifc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib
import numpy as np
from scipy.interpolate import interp1d

dynamic_items = []

def save_json(dados):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dados.json")
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)

def get_options(self, context):    
    return dynamic_items

def set_hide_class(context, index, is_hidden):
    props = context.scene.og_props
    level = props.classes[index].level_index
    for classe in props.classes:
        if classe.index > index:
            if classe.level_index > level:
                classe.is_hidden = is_hidden                
            else:
                return

def set_hide_product(context, index, is_hidden):
    props = context.scene.og_props
    level = props.products[index].level_index
    for product in props.products:
        if product.index > index:
            if product.level_index > level:
                product.is_hidden = is_hidden                
            else:
                return
                
def build_classes(context, classe, c, level, parent, hide):
    c += 1 
    props = context.scene.og_props
    new_class = props.classes.add()
    new_class.code        = classe["code"]                 
    new_class.name        = classe["name"]                
    new_class.description = classe['descriptionPart']   
    new_class.uri         = classe["uri"]  
    new_class.type        = classe["classType"]  
    new_class.index       =   c  
    new_class.level_index = level
    new_class.parent = parent
    new_class.is_expanded = False
    #new_class.is_hidden = False if level == 1 else True
    new_class.is_hidden = hide
    
    if 'children' in classe:   
        level = level + 1     
        new_class.has_children = True
    # new_class.is_expanded = True
        for child in classe['children']:            
            c = build_classes(context, child , c, level, classe['name'], True)
            set_hide_class(context, c, True)
    else:
        new_class.has_children = False
    return c

def build_products(context, classe, c, level, parent, hide, children):
    c += 1 
    props = context.scene.og_props
    new_product = props.types.add()
    new_product.id        = classe["id"]                 
    new_product.name        = classe["name"]
    new_product.description = classe['description']   
    new_product.element_type         = classe["element_type"] 
    new_product.index       =   c  
    new_product.level_index = level
    new_product.parent = parent
    new_product.is_expanded = False
    new_product.is_hidden = hide
    new_product.has_children = children
    return c

def _build_products(context, classe, c, level, parent, hide, children):
    c += 1 
    props = context.scene.og_props
    new_product = props.types.add()
    new_product.code        = classe["code"]                 
    new_product.name        = classe["name"]                
    new_product.description = classe['description']   
    new_product.element_type = classe["ElementType"] 
    new_product.index       =   c  
    new_product.level_index = level
    new_product.parent = parent
    new_product.is_expanded = False
    new_product.is_hidden = hide
    new_product.has_children = children
    
    # if 'children' in classe:   
    #     level = level + 1     
    #     new_product.has_children = True
    #     for child in classe['children']:            
    #        c = build_products(context, child , c, level, classe['name'], True)
   
    # else:
    #     new_product.has_children = False
    return c


   
# ==================================================================================================
# ==================================================================================================
# 
# O&G Dictionary
# 
# ==================================================================================================
# ==================================================================================================

# clear the list of properties loaded
class Operator_clear_properties(bpy.types.Operator):
    """"""
    bl_idname  = "object.clear_prop"
    bl_label   = "Clear properties"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props
        props.ifc_prop.clear()              
        return {"FINISHED"}    

# assign all objects
class Operator_assign_all(bpy.types.Operator):
    """"""
    bl_idname  = "object.assign_all"
    bl_label   = "Assign all objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props
        for obj in props.ifc_prop:
            obj.is_selected = True              
        return {"FINISHED"}         

# unassign all objects
class Operator_unassign_all(bpy.types.Operator):
    """"""
    bl_idname  = "object.unassign_all"
    bl_label   = "Assign all objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props
        for obj in props.ifc_prop:
            obj.is_selected = False              
        return {"FINISHED"}    

# connect to bSDD and get the properties of Oil & Gas Subsea data dictionary
class Operator_get_properties(bpy.types.Operator):
    """connect to bSDD and get the properties of Oil & Gas Subsea data dictionary"""
    bl_idname  = "bsdd.get_prop"
    bl_label   = "Get properties from bSDD"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props
        props.add_prop_clicked = False        
        props.ifc_prop.clear()
        result = bSDD.load_properties(props.dictionary)
        if result:
            for property in bSDD.data_prop:  
                new_prop = props.ifc_prop.add() 
                new_prop.code        = property["code"]                 
                new_prop.name        = property["name"]                
                new_prop.description = property['descriptionPart']   
                new_prop.uri         = property["uri"] 
            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}

# acerra a uri na propriedade no bSDD
class Operator_uri(bpy.types.Operator):
    """acerra a uri na propriedade no bSDD"""
    bl_idname  = "object.uri"
    bl_label   = "uri property"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    @classmethod
    def description(cls, context, properties):
        return f"Open the URL in your web Browser: '{properties.uri}'"
    
    def execute(self, context):                
        webbrowser.open(self.uri)        
        return {"FINISHED"}
    
# connect to bSDD and get the classes of Oil & Gas Subsea data dictionary
class Operator_get_classes(bpy.types.Operator):
    """ connect to bSDD and get the classes of Oil & Gas Subsea data dictionary"""
    bl_idname  = "bsdd.get_class"
    bl_label   = "Get classes from bSDD"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props               
        props.classes.clear()
        props.classes_loaded = False
        c = -1
        result = bSDD.load_classes(props.dictionary, True)
        if result:
            for classe in bSDD.data_class:  
                new_c = build_classes(context, classe, c, 1, '', False)
                c = new_c
            refresh(context)
            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}

# expand container
class Operator_expand_classes(bpy.types.Operator):
    """"""
    bl_idname  = "object.expand_classes"
    bl_label   = "Expand classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props  
        props.classes[self.index].is_expanded = True
        imin = False
        #set_hide(context, self.index, False)
        level = props.classes[self.index].level_index
        for classe in props.classes:                 
            if classe.index > self.index:                 
                if classe.level_index == level+1:
                    classe.is_hidden = False 
                    classe.is_expanded = False 
                    imin = True
                if classe.level_index <= level and imin:
                    break

        refresh(context)  
        return {"FINISHED"} 

# contract container
class Operator_contract_classes(bpy.types.Operator):
    """"""
    bl_idname  = "object.contract_classes"
    bl_label   = "Contract classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props  
        props.classes[self.index].is_expanded = False 
        #set_hide(context, self.index, True)  
        level = props.classes[self.index].level_index
        for classe in props.classes:
            if classe.index > self.index:
                if classe.level_index > level:
                    classe.is_hidden = True                
                else:
                    break
        refresh(context)          
        return {"FINISHED"} 

# Add selected properties to Pset template
class Operator_add_properties(bpy.types.Operator):
    """"""
    bl_idname  = "object.add_prop"
    bl_label   = "Add properties to selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                        
        props = context.scene.og_props
        try:
            for prop in tqdm(props.ifc_prop, total= len(props.ifc_prop), desc='Processing properties'):
                if prop.is_selected == True:
                    result = bSDD.get_property(prop.uri)
                    bSDD.data_info_prop
                    if result:
                        flag = PropTempl.add_pset_template(bSDD.data_info_prop)
                        if not flag:
                            self.report({'ERROR'}, "Error creating pset template")
                            return {"CANCELLED"} 

                    else:
                       self.report({'ERROR'}, "Error connecting to bSDD")
                       return {"CANCELLED"}                 
            return {"FINISHED"} 
        except Exception as ex:
            print(ex)
            self.report({'ERROR'}, str(ex))
            return {"CANCELLED"}

# get property metadata 
class Operator_get_prop_info(bpy.types.Operator):
    """"""
    bl_idname  = "property.get_prop_info"
    bl_label   = "get property metadata"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    def execute(self, context):                
        props = context.scene.og_props
        props.info_prop_loaded = False
        result = bSDD.get_property(self.uri)
        if result:
            prop_info = bSDD.data_info_prop
            props.prop_datatype = prop_info['dataType']
            props.prop_units = prop_info['units'][0] if len(prop_info['units']) > 0 else ''
            props.prop_definition = prop_info['definition']
            props.prop_description = prop_info['description']
            props.prop_type = prop_info['propertyValueKind']
            props.info_prop_loaded = True
            for classe in prop_info['propertyClasses']:
                newitem = props.class_info.add()
                newitem.code = classe['code']
                newitem.name = classe['name']
                newitem.description = classe['description']
                newitem.uri = classe['uri']
                newitem.propertyset = classe['propertySet']

            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}

# get class metadata 
class Operator_get_class_info(bpy.types.Operator):
    """Get active class information"""
    bl_idname  = "bsdd.get_class_info"
    bl_label   = "get class metadata"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    def execute(self, context):                
        props = context.scene.og_props
        props.info_prop_loaded = False
        result = bSDD.get_class(self.uri)
        if result:
            props.classes_loaded = True
            class_info = bSDD.data_info_class
            props.class_description = class_info['description']
            props.class_definition  = class_info['definition']
            props.class_type  = class_info['classType']
            
            if "relatedIfcEntityNames" in class_info:
                props.class_ifctype = class_info["relatedIfcEntityNames"][0]
            else:
                props.class_ifctype = ''

            if 'versionDateUtc' in class_info:
                props.class_version = class_info['versionDateUtc']
            else:
                props.class_version = ''

            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}  


# get class metadata 
class Operator_get_class_prop(bpy.types.Operator): 
    """Get active class properties"""
    bl_idname  = "bsdd.get_class_prop"
    bl_label   = "get class properties"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    def execute(self, context):                
        props = context.scene.og_props
        props.info_class_prop_loaded = False
        result = bSDD.get_class_prop(self.uri)
        if result:
            props.info_class_prop_loaded = True   
            props.class_prop_info.clear()         
            properties = bSDD.data_class_prop
            for pro_info in properties['classProperties']:
                newitem = props.class_prop_info.add()
                newitem.name = pro_info['name']
                newitem.description = pro_info['description']
                newitem.definition = pro_info['definition']
                newitem.datatype = pro_info['dataType']
                newitem.uri = pro_info['uri']
                newitem.propertyset = pro_info['propertySet']

            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}  
           
# export IDS file 
class Operator_export_ids(bpy.types.Operator):
    """"""
    bl_idname  = "ids.export"
    bl_label   = "Export ids file"
    bl_options = {"REGISTER", "UNDO"}
    filepath : bpy.props.StringProperty(subtype="FILE_PATH")
    filte_glob : bpy.props.StringProperty(default='*.ids', options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.og_props
        props.ids_file = self.filepath
        # obtem o template
        PropTempl.get_template()
        template = PropTempl.template
         
        # Cria o ids
        my_ids = ids.Ids(
            title='Oil & Gas Subsea',
            copyright='Petrobras',
            author='ÇERTI',
            description='Requirements for properties at subsea projects Oil&Gas',
            purpose='',
            milestone=''
        )

        # povoa ids
        pset_templates = template.by_type('IfcPropertySetTemplate')
        for pset_template in tqdm(pset_templates, total=len(pset_templates), desc='Processing specifications:'):
            applicability = pset_template.ApplicableEntity.split('/') 
            # define a especificação
            my_spec = ids.Specification(
                name=pset_template.Name,
                description='',
                minOccurs=1,
                maxOccurs='unbounded',
                ifcVersion='IFC4'
            )

            #define a aplicabilidade
            entity = ids.Entity(
                name=applicability[0],
                predefinedType='USERDEFINED'
            )

            my_spec.applicability.append(entity)
            if len(applicability) > 1:
                attribute = ids.Attribute(
                    name='ObjectType',
                    value=applicability[1]
                )                
                my_spec.applicability.append(attribute)
            props_templ = pset_template.HasPropertyTemplates

            # requisitos
            for prop_templ in props_templ:
                print(prop_templ.Name)
                property = ids.Property(
                    baseName= prop_templ.Name,
                    propertySet= pset_template.Name,
                    dataType= prop_templ.PrimaryMeasureType.upper(),
                    cardinality='required' 
                )
            
                my_spec.requirements.append(property)

            my_ids.specifications.append(my_spec)
        
        try:
            my_ids.to_xml(self.filepath)
            return {'FINISHED'}
        except Exception as ex:
            self.report({'ERROR'}, str(ex))
            return {"CANCELLED"}

    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

# ==================================================================================================
# ==================================================================================================
# DECOMPOSITION
# ==================================================================================================
# ==================================================================================================
   
# load decomposition
class Operator_load_decomposition(bpy.types.Operator):
    """Get active class information"""
    bl_idname  = "elements.decomposition"
    bl_label   = ""
    bl_options = {"REGISTER", "UNDO"}

    
    @classmethod
    def load_contained_elements_by_decomposition(cls, container: ifcopenshell.entity_instance, context) -> None:
        props = context.scene.og_props
        
        def get_decomposition(element: ifcopenshell.entity_instance, is_recursive : bool) -> set[ifcopenshell.entity_instance]:
            queue = [element]
            #results = set()
            results = []

            while queue:
                element = queue.pop()
                for rel in getattr(element, "ContainsElements", []):                    
                    related = rel.RelatedElements                    
                    queue.extend(related)
                    results.extend(related)
                for rel in getattr(element, "IsDecomposedBy", []):
                    related = rel.RelatedObjects
                    queue.extend(related)
                    results.extend(related)
                for rel in getattr(element, "IsNestedBy", []):
                    related = rel.RelatedObjects
                    related = [x for x in related if not x.is_a('IfcDistributionPort')]
                    queue.extend(related)
                    results.extend(related)
                if not is_recursive:
                    break
            return results
        

        def add_elements(elements, level=1):
            #l_elements = [x for x in elements]
            for element in elements:                        
                # if not props.should_include_children and tool.Root.is_spatial_element(element):
                #     continue
                # ifc_definition_id = element.id()
                new = props.elements_containers.add()
                new.name = element.Name or 'Unnamed'
                new.type = element.is_a()
                new.level = level 
                new.id = element.id()                
                new.object_type = element.ObjectType or 'Unnamed'                            
                children = [
                    e
                    for e in get_decomposition(element, is_recursive=False)
                    if not e.is_a("IfcFeatureElement")
                ]
                if children:
                    new.has_children = True                    
                    new.is_expanded = False
                    add_elements(children, level=level + 1)
        
        elements = get_decomposition(container, is_recursive=False) 
        add_elements([container])
           

    def execute(self, context):                       
        props = context.scene.og_props
        props.elements_containers.clear()
        model = tool.Ifc.get()

        elements = model.by_type("IfcProject")
        if len(elements) > 0:
            for element in elements:
                self.load_contained_elements_by_decomposition(element, context)              
            i = 0          
            for element in props.elements_containers:
                element.index = i
                element.is_hidden = False if element.level==1 else True
                element.is_expanded = False if element.level==1 else True  
                i += 1   
            refresh_container(context)
        return {"FINISHED"} 

# expand decomposition container
class Operator_expand_decomposition(bpy.types.Operator):
    """"""
    bl_idname  = "element.expand_decomposition"
    bl_label   = "Expand classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props  
        item = props.elements_containers[self.index]
        item.is_expanded = True
        imin = False
        #set_hide(context, self.index, False)
        level = item.level
        for classe in props.elements_containers:                 
            if classe.index > item.index:                 
                if classe.level == level + 1:
                    classe.is_hidden = False 
                    classe.is_expanded = False 
                    imin = True
                if classe.level <= level and imin:
                    break

                

        refresh_container(context)  
        return {"FINISHED"} 

# contract decomposition container
class Operator_contract_decomposition(bpy.types.Operator):
    """"""
    bl_idname  = "element.contract_decomposition"
    bl_label   = "Contract classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props       
        item =  props.elements_containers[self.index]                  
        level = item.level
        item.is_expanded = False
        for element in props.elements_containers:
            if element.index > self.index:
                if element.level > level:
                    element.is_hidden = True 
                    element.is_expanded = False              
                else:
                    break
        refresh_container(context)          
        return {"FINISHED"} 

# element decomposition select element
class Operator_decomposition_select_element(bpy.types.Operator):
    """"""
    bl_idname  = "decomposition.select_element"
    bl_label   = "Select object"
    bl_options = {"REGISTER", "UNDO"}    
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):   
        props = context.scene.og_props       
        item =  props.elements_containers[self.index]                                   
        model = tool.Ifc.get()        
        ifc_element = model.by_id(item.id)         
        obj = tool.Ifc.get_object(ifc_element)  
        print(f'id: {item.id}')   
        print(f'elemento: {ifc_element}')
        print(f'objeto: {obj}')   
        if obj:
            obj.select_set(item.is_selected)            
            bpy.context.view_layer.objects.active =  obj
       
        refresh_container(context) 
        return {"FINISHED"} 

# element decomposition selection
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
    type  : bpy.props.StringProperty(name="type", default="nest")

    def execute(self, context):   
        props = context.scene.og_props       
        model = tool.Ifc.get() 
        item =  props.elements_containers[self.index]   
        entity_children = model.by_id(item.id)
        parent = props.containers_show[props.active_element_index]  
        entity_parent = model.by_id(parent.id)  

             
        print(f'entity_parent: {entity_parent}')
        print(f'entity_children: {entity_children}')
        move_to_assembly(entity_parent, entity_children, self.type)
        self.report({'OPERATOR'}, 'Moved successfully!')

       
        refresh_container(context) 
        bpy.ops.elements.decomposition()
        return {"FINISHED"}
# ==================================================================================================
# ==================================================================================================
# CATALOG
# ==================================================================================================
# ==================================================================================================
 
# Load catalog products
class Operator_load_products(bpy.types.Operator):
    """"""
    bl_idname  = "catag.load_products"
    bl_label   = "load products from catalog"
    bl_options = {"REGISTER", "UNDO"}    

    def execute(self, context): 
        props = context.scene.og_props               
        props.types.clear()
        props.types_loaded = True
        model = tool.Ifc.get()
        types = model.by_type('IfcTypeProduct')
        c = -1
        result = {}
        data = Catalog.get_ifc_type()
        classe_title = {
            'name': '',
            'description' : '',
            'element_type': '',
            'id' : 0
        }

        for type in types:
            dic = {}   
            dic['id'] = type.id()         
            dic['name'] = type.Name or  ''
            dic['description'] = type.Description or ''
            dic['element_type'] = type.ElementType or ''

            if type.is_a() not in result:
                result[type.is_a()] = []
            else:
                result[type.is_a()].append(dic)
        save_json(result)

        for key, values in  result.items():
                if key in data:
                    classe_title['name'] = data[key]
                else:
                    classe_title['name'] = key
                new_c = build_products(context, classe_title, c, 1, '', False, True)
                c += 1
                print(values)
                for value in values:
                    new_c = build_products(context, value, c, 2, '', True, False)
                    c = new_c
        refresh_types(context)
        return {"FINISHED"} 
        
# contract products
class Operator_contract_products(bpy.types.Operator):
    """"""
    bl_idname  = "object.contract_products"
    bl_label   = "Contract products"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props  
        props.types[self.index].is_expanded = False 
        #set_hide(context, self.index, True)  
        level = props.types[self.index].level_index
        for classe in props.types:
            if classe.index > self.index:
                if classe.level_index > level:
                    classe.is_hidden = True                
                else:
                    break
        refresh_types(context)          
        return {"FINISHED"} 
    
# expand products
class Operator_expand_products(bpy.types.Operator):
    """"""
    bl_idname  = "object.expand_products"
    bl_label   = "Expand products"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.og_props  
        props.types[self.index].is_expanded = True
        imin = False
        #set_hide(context, self.index, False)
        level = props.types[self.index].level_index
        for product in props.types:                 
            if product.index > self.index:                 
                if product.level_index == level+1:
                    product.is_hidden = False 
                    product.is_expanded = False 
                    imin = True
                if product.level_index <= level and imin:
                    break

        refresh_types(context)  
        return {"FINISHED"} 

# Create a ifc entity from Json
class Operator_catalog_select_type(bpy.types.Operator):
    """"""
    bl_idname  = "catag.select_type"
    bl_label   = "export element in json"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="uri")

            
    def execute(self, context): 
            props = context.scene.og_props                     
            model = bonsai.tool.Ifc.get()        
            type = model.by_id(self.id)           

            if type is not None:
                obj = tool.Ifc.get_object(type)
                # bpy.ops.object.select_all(action='DESELECT')
                # context.view_layer.objects.active = obj
                # obj.select_set(True)

                if obj:
                    if obj.hide_get():
                        obj.hide_set(False)
                    obj.select_set(True)
                    context.view_layer.objects.active = obj
                    #bpy.ops.props.load_properties()

                self.report({'OPERATOR'}, 'Done!')
                return {"FINISHED"} 



# ==================================================================================================
# ==================================================================================================
# PROPERTIES
# ==================================================================================================
# ==================================================================================================

# Load object properties
class Operator_props_edit(bpy.types.Operator):
    """"""
    bl_idname  = "props.edit"
    bl_label   = "edit object properties"
    bl_options = {"REGISTER", "UNDO"} 
    pset_index : bpy.props.IntProperty(name='pset index')
    prop_index : bpy.props.IntProperty(name='prop index')   
    type_prop  : bpy.props.StringProperty(name='prop type') 
    
    def change_prop(self, pset, props):        
        model = tool.Ifc.get() 
        for name_prop, values in props.items():
            for prop in pset.HasProperties:
                if prop.Name == name_prop:
                    if prop.is_a() == 'IfcPropertyListValue':
                        list_values = prop.ListValues
                        new_list_values = []
                        for value in values:    
                            if value is not None:
                                new_value = model.create_entity(list_values[values.index(value)].is_a(), value) 
                                new_list_values.append(new_value)

                        prop.ListValues = new_list_values
                    elif prop.is_a() == 'IfcPropertyEnumeratedValue':
                        list_values = prop.EnumerationReference.EnumerationValues
                        new_list_values = set()                        
                        for value in values:    
                            if value is not None:
                                new_value = model.create_entity(list_values[values.index(value)].is_a(), value)                                 
                                new_list_values.add(new_value)
                        print(new_list_values)
                        prop.EnumerationValues = list(new_list_values)
                    else:                        
                        new_value = model.create_entity(prop.NominalValue.is_a(), values[0])                        
                        prop.NominalValue = new_value

    def get_prop_type( self, prop):
        res = None
        if prop.type_value == "str":
            res = prop.valuestr
        elif prop.type_value == "int":
            res = prop.valueint
        elif prop.type_value == "bool":
            res = prop.valuebool
        elif prop.type_value == "float":
            res = prop.valuefloat
        return res
    
    
    def execute(self, context):
        props = context.scene.og_props 
        props.icon_edit_prop = 'CHECKMARK'
        model = tool.Ifc.get()
        new_pset = ''
        new_values = []
        new_props = {}
        print(100*'_')
        # cria um dicionario com as propriedades e valores
        for pset in props.prop_metadata:            
            if pset.index == self.pset_index:                              
                for prop in pset.props:                                   
                    if prop.index == self.prop_index:
                        product = model.by_id(pset.id_obj)
                        new_pset = pset.name

                        if prop.type_prop == 'IfcPropertyEnumeratedValue':
                            for enum in prop.enumerations:
                                if enum.enumerated:

                                    if prop.name in new_props:
                                        new_props[prop.name].append(get_prop_type(enum))                        
                                    else:
                                        new_props[prop.name] = [get_prop_type(enum)]
                        else:
                            if prop.name in new_props:
                                new_props[prop.name].append(get_prop_type(prop))                        
                            else:
                                new_props[prop.name] = [get_prop_type(prop)]
      
        _pset = ifcopenshell.api.pset.add_pset(model, product=product, name=new_pset) 

        self.change_prop(_pset, new_props)
        bpy.context.scene.update_tag()
        return {"FINISHED"} 
    
class Operator_props_load(bpy.types.Operator):
    """"""
    bl_idname  = "props.load_properties"
    bl_label   = "load object properties"
    bl_options = {"REGISTER", "UNDO"} 

    def execute(self, context):
        try:
            if tool.Ifc.get() is None:
                bpy.ops.og.error_message('INVOKE_DEFAULT', message='No Ifc file loaded')
                return {"CANCELLED"}
            else:                
                refresh_props(context)
                return {"FINISHED"} 
        except Exception as e:
            bpy.ops.og.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}
    
class Operator_props_expand(bpy.types.Operator):
    """"""
    bl_idname  = "props.expand"
    bl_label   = "expand properties / documents"
    bl_options = {"REGISTER", "UNDO"}   

    index : bpy.props.IntProperty(name="index")  
   
    def execute(self, context):
        props = context.scene.og_props 
        for pset in props.prop_metadata:
            if pset.index == self.index:                    
                    pset.is_expanded = not(pset.is_expanded)
                    pass
        return {"FINISHED"} 

class Operator_docs_expand(bpy.types.Operator):
    """"""
    bl_idname  = "docs.expand"
    bl_label   = "expand properties / documents"
    bl_options = {"REGISTER", "UNDO"}   

    index : bpy.props.IntProperty(name="index")  
    type  : bpy.props.StringProperty(name='type')

    def execute(self, context):
        props = context.scene.og_props         
        if self.type == 'property':
            for pset in props.prop_metadata:
                if pset.index == self.index:                    
                        pset.docs_expanded = not(pset.docs_expanded)
                        pass
        else:
            props.docs_expanded = not(props.docs_expanded)

        return {"FINISHED"} 

class Columns(bpy.types.PropertyGroup):
    name     : bpy.props.StringProperty(name='column name')
    selected : bpy.props.BoolProperty(name='selected', default=True)

class Operator_props_graph(bpy.types.Operator):
    """Generate a curve based on the information from the table"""
    bl_idname  = "props.graph"
    bl_label   = "Plot Graph"
    bl_options = {"REGISTER", "UNDO"} 
    pset_index : bpy.props.IntProperty(name='')
    prop_index : bpy.props.IntProperty(name='')   
    document   : bpy.props.StringProperty(name='document') 
    x_axis     : bpy.props.EnumProperty(items=get_options, name='property for x axis')
    order_x    : bpy.props.BoolProperty(name='Order X Axis', default=False)
    min_x      : bpy.props.FloatProperty(name='Min X Axis')
    max_x      : bpy.props.FloatProperty(name='Max X Axis') 
    min_y      : bpy.props.FloatProperty(name='Min Y Axis')
    max_y      : bpy.props.FloatProperty(name='Max Y Axis') 
    mult_x     : bpy.props.FloatProperty(name='Grid Interval X')         
    mult_y     : bpy.props.FloatProperty(name='Grid Interval Y')     
    interpoled : bpy.props.BoolProperty(name='Intepoled Curve')
    columns    : bpy.props.CollectionProperty(name='columns', type=Columns)
    intpl_type : bpy.props.EnumProperty(
        items=[
            ('cubic','cubic','cubic'),
            ('linear', 'linear', 'linear')
        ],
        name='type',
        description='Get interpoled type'
    )

    table : dict
    title : str
    lista : list 
    csv   : str 
    df : None 
    
    def draw(self, context):
        props = context.scene.og_props
        layout = self.layout
        cols = self.df.columns.to_list()
        
        # se tem documento anexado
        if self.prop_index == -1:
            if props.show_table:
                icon = 'TRIA_DOWN_BAR'
            else:
                icon = 'TRIA_RIGHT_BAR'

            row = layout.row()
            row.operator("props.show_table", icon=icon, text="")
            row.label(text='Imported Table :', icon='VIEW_ORTHO')
            if props.show_table:
                box = layout.box()
                rowb = box.row() 
                for c in cols:
                    col = rowb.column(align=True)
                    col.label(text=c)
                    

                for index, row in self.df.iterrows():
                    rowb = box.row() 
                    for c in cols:
                        col = rowb.column(align=True)
                        col.label(text=str(row[c]))
                        
     
        box = layout.box()
        box.prop(self, "min_x")
        box.prop(self, "max_x")
        box.prop(self, "min_y")
        box.prop(self, "max_y")
        box.prop(self, "mult_x")
        box.prop(self, "mult_y")

        row = layout.row(align=True)
        row.prop(self, "interpoled")
        row.prop(self, "intpl_type")
        layout.prop(self, "x_axis")

        layout.label(text='Select Columns to plot')
        box = layout.box()
        for col in self.columns:
            if col.name != self.x_axis:
                row = box.row()
                row.prop(col, 'selected', text=col.name)
            else:
                col.selected = True

        layout.prop(self, "order_x") 

    def invoke(self, context, event):     
        self.table={}
        self.title = ''
        dynamic_items.clear()
        self.columns.clear()

        # cria um dicionario com as propriedades e valores
        props = context.scene.og_props
        # se o documento esta associado a propriedade
        if self.pset_index > -1:
            for pset in props.prop_metadata:            
                if pset.index == self.pset_index:    
                    # se não for documento externo
                    if self.prop_index == -1:           
                        self.csv = pset.document
                    else:
                        for prop in pset.props:                                   
                            if prop.index == self.prop_index:
                                self.title = prop.name.split('_')[0]
                                col =  f"{prop.name.split('_')[1]} {prop.datatype}"                      
                                if col in self.table:
                                    self.table[col].append(get_prop_type(prop)) 
                                else:
                                    self.table[col] = [get_prop_type(prop)]
            # cria o dataframe
            if self.prop_index == -1:
                if os.path.exists(self.csv): 
                    self.df = pd.read_csv(self.csv) 
                else:
                    self.report({'ERROR'}, 'FILE NOT FOUND!')
                    return {"CANCELLED"}
            else:
                self.df = pd.DataFrame(self.table)

        # se o documento está aasociado ao elemento
        else:
            if os.path.exists(self.document): 
                self.df = pd.read_csv(self.document)
            else:
                self.report({'ERROR'}, 'FILE NOT FOUND!')
                return {"CANCELLED"}


        # imprime a opcao de colunas para o eixo x
        for c in self.df.columns.to_list():
            if (c,c,c) not in dynamic_items:
                dynamic_items.append((c,c,c))
            newcolumn = self.columns.add()
            newcolumn.name = c
            
        return context.window_manager.invoke_props_dialog(self, width=500)

    def execute(self, context):
        for item in self.columns:
            if not item.selected:
                self.df = self.df.drop(columns=item.name) 

        cols = self.df.columns.to_list()
        # Criar gráfico com Matplotlib
        fig, ax = plt.subplots()              
        x = self.x_axis if self.x_axis != '' else cols[0]
        if self.order_x:
            self.df = self.df.sort_values(by=x)
        lines = []
        for col in cols:
            if col != x:
                if self.interpoled:
                    cubic_interpoletion_model = interp1d(self.df[x], self.df[col], kind=self.intpl_type)
                    x_ = np.linspace(self.df[x].min(), self.df[x].max(), 600)
                    y_ = cubic_interpoletion_model(x_)
                    lines.append(ax.plot(x_, y_, label=col))
                else:
                    lines.append(ax.plot(self.df[x],self.df[col], label=col))
      
        # configura o grafico
        ax.set_title(self.title)
        ax.set_xlabel(x)      
        ax.grid(True) 
        ax.xaxis.set
        ax.set_box_aspect(0.5)

        if self.mult_x > 0:
            ax.xaxis.set_major_locator(MultipleLocator(self.mult_x))
        if self.mult_y > 0:
            ax.yaxis.set_major_locator(MultipleLocator(self.mult_y))
        if self.max_x > 0:
            ax.set_xlim(self.min_x, self.max_x)
        if self.max_y > 0:
            ax.set_ylim(self.min_y, self.max_y)  

        fig.legend()

        # Salvar imagem em memória
        buffer = BytesIO()        
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Criar HTML com a imagem embutida
        html = f"""
        <html>
        <head><title>BIM Report</title></head>
        <body>
        <h2>{self.title}</h2>
        <img src="data:image/png;base64,{img_base64}" />
        </body>
        </html>
        """

        # Salvar HTML e abrir no navegador
        with open("graphic.html", "w") as f:
            f.write(html)
        webbrowser.open("graphic.html")
        return {"FINISHED"} 
    
class Operator_props_invert(bpy.types.Operator):
    """"""
    bl_idname  = "props.invert"
    bl_label   = "invert x y"
    bl_options = {"REGISTER", "UNDO"} 

    def execute(self, context):
        props = context.scene.og_props
        props.invert_xy = not(props.invert_xy)
        return {"FINISHED"}
    
class Operator_document_edit(bpy.types.Operator):
    """"""
    bl_idname  = "props.doc_edit"
    bl_label   = "edit reference document"
    bl_options = {"REGISTER", "UNDO"} 
    ifc_id   : bpy.props.IntProperty(name='ifc id')
    id : bpy.props.StringProperty(name='id')
    name : bpy.props.StringProperty(name='name')
    location : bpy.props.StringProperty(name='location')

    def execute(self, context):
        model = tool.Ifc.get()
        ifc_obj = model.by_id(self.ifc_id)
        ifc_type = ifcopenshell.util.element.get_type(ifc_obj)
        if ifc_type:
            rel = ifc_type.HasAssociations
        else:
            rel = ifc_obj.HasAssociations
        if rel:
            doc = rel[0].RelatingDocument
            doc.Identification = self.id
            doc.Name = self.name
            doc.Location.wrappedValue = self.location

        return {"FINISHED"}
    
class Operator_document_load(bpy.types.Operator):
    """"""
    bl_idname  = "props.load_doc"
    bl_label   = "load reference document"
    bl_options = {"REGISTER", "UNDO"} 
    filepath   : bpy.props.StringProperty(subtype='FILE_PATH')
    index      : bpy.props.IntProperty(name='índex')
    doc_index : bpy.props.IntProperty(name="doc index")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        props = context.scene.og_props
        if self.index == -1:
            props.documents[self.doc_index].location = self.filepath
        else:
            props.prop_metadata[self.index].documents[self.doc_index].location = self.filepath
        return {"FINISHED"}
    
class Operator_document_open(bpy.types.Operator):
    """"""
    bl_idname  = "props.open_doc"
    bl_label   = "open reference document"
    bl_options = {"REGISTER", "UNDO"} 
    location      : bpy.props.StringProperty(name='location')

    
    def execute(self, context):   
        if os.path.exists(self.location):     
            webbrowser.open(self.location)
            return {"FINISHED"}
        else:
            self.report({'ERROR'}, 'FILE NOT FOUND!')
            return {"CANCELLED"}
    
class Operator_show_table(bpy.types.Operator):
    """"""
    bl_idname  = "props.show_table"
    bl_label   = "show data table"
    bl_options = {"REGISTER", "UNDO"} 

   
    def execute(self, context):
        props = context.scene.og_props
        props.show_table = not props.show_table
        return {"FINISHED"}

#============================================================================================
# Geral
#============================================================================================

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

# class Operator_catalog_insert_type(bpy.types.Operator):
#     """"""
#     bl_idname  = "catag.select_type"
#     bl_label   = "export element in json"
#     bl_options = {"REGISTER", "UNDO"}  

#     id : bpy.props.IntProperty(name="uri")

#     def v_type(self, uri):
#         result = uri.split('#')
#         return result[1]
    
#     # Create a IFC entity 
#     def make_entity_(self, model, json):
#         context = representation.get_context(model, "Model", "Body", "MODEL_VIEW")
#         #verify if entity exists in file
#         if 'Name' in json:
#             exist_ents = [e for e in model.by_type(json['ifc_class']) if e.Name == json['Name']]
#         else:
#             exist_ents = []

#         # if not exists create entity, if exists return found entity
#         if not len(exist_ents) > 0:
#             ent = model.create_entity(json['ifc_class'])
#             if hasattr(ent, 'GlobalId'):
#                 ent.GlobalId = ifcopenshell.guid.new()

#             for key, value in json.items():
#                 if key != 'ifc_class':   

#                     if isinstance(value, list) and isinstance(value[0], dict):
#                         l = []
#                         for item in value:
#                             ent2 = self.make_entity(model, item)
#                             l.append(ent2)
#                             setattr(ent, key, l)

#                     elif isinstance(value, dict) :
#                         ent2 = self.make_entity(model, value)
#                         setattr(ent, key, ent2)
#                     else:
#                         if value == "@Body":
#                             setattr(ent, key, context)
#                         else:
#                             setattr(ent, key, value)
            
#         else:
#             ent = exist_ents[0]

#         return ent
    
#     def make_entity(self, model, json):
#         context = representation.get_context(model, "Model", "Body", "MODEL_VIEW")
#         #verify if entity exists in file
#         if 'Name' in json:
#             exist_ents = [e for e in model.by_type(json['ifc_class']) if e.Name == json['Name']]
#         else:
#             exist_ents = []

#         # if not exists create entity, if exists return found entity
#         if not len(exist_ents) > 0:
#             ent = model.create_entity(json['ifc_class'])
#             if hasattr(ent, 'GlobalId'):
#                 ent.GlobalId = ifcopenshell.guid.new()

#             for key, value in json.items():
#                 if key not in ['ifc_class', '@material']:   

#                     if isinstance(value, list) and isinstance(value[0], dict):
#                         l = []
#                         for item in value:
#                             ent2 = self.make_entity(model, item)
#                             l.append(ent2)
#                             setattr(ent, key, l)

#                     elif isinstance(value, dict) :
#                         ent2 = self.make_entity(model, value)
#                         setattr(ent, key, ent2)
#                     else:
#                         if value == "@Body":
#                             setattr(ent, key, context)
#                         else:
#                             setattr(ent, key, value)
            
#         else:
#             ent = exist_ents[0]

#         return ent
    
#     def split_name(self, uri):
#         if '#' in uri:
#             return uri.split('#')[-1]
#         else:
#             return uri
        
#     def execute(self, context): 
#             props = context.scene.og_props                     
#             model = bonsai.tool.Ifc.get()        
#             type = Catalog.get_type(self.uri)       
#             if type is not None:
#                 if 'entity' in type:
#                     obj_name = f"{type['entity']['ifc_class']}/{type['entity']['Name']}"
#                     lt = [f'{x.is_a()}/{x.Name}' for x in model.by_type('IfcTypeProduct')]
#                     if not obj_name in lt:
#                         sty = None

#                         # create element
#                         representation = None
#                         body = ifcopenshell.util.representation.get_context(model, "Model", "Body", "MODEL_VIEW") 
#                         element_type = model.create_entity(type['entity']['ifc_class'])
#                         element_type.GlobalId = ifcopenshell.guid.new()
#                         print(element_type)
                        
#                         # add values to attributes
#                         for key, value in type['entity'].items():
#                             if key != 'ifc_class':   
#                                 setattr(element_type, key, value)

                        
#                         # create the geometry associate
#                         if 'geometry' in type:                                                 
#                             vertices = [type['geometry']['vertices']]
#                             faces = [type['geometry']['faces']]  

#                             builder = ifcopenshell.util.shape_builder.ShapeBuilder(tool.Ifc.get())
#                             item = builder.mesh(vertices[0], faces[0])
#                             representation = builder.get_representation(body, [item])
#                             geometry.assign_representation(model, product=element_type, representation=representation)
            

#                         # create the associate material
#                         if 'material' in type:
#                             mat = self.make_entity(model, type['material'])
#                             print(mat)
#                             material.assign_material(model, products=[element_type], type=mat.is_a(), material=mat)

#                             # create the associate style
#                             if 'style' in type:
#                                 sty = self.make_entity(model, type['style'])
#                                 print(sty)
#                                 materials = [m for m in model.by_type('IfcMaterial') if m.Name == type['style']['@material']] 
#                                 print(materials)
#                                 if len(materials) > 0: 
#                                     style.assign_material_style(model, material=materials[0], style=sty, context=body)
#                                     if representation is not None:
#                                         sty.Item = representation.Items[0]
#                                     print(materials[0])
#                                 else:
#                                     print(f'material {materials["style"]["@material"]} não encontrado!')
                            
#                         # import element type in bonsai
#                         i = Import_ifc()
#                         i.import_type_from_ifc(element_type, context)                        
                    
#                         print('Done!')
#                         self.report({'OPERATOR'}, 'Done!')
#                         return {"FINISHED"} 

#                     else:
#                         print('The type already exists!')
#                         self.report({'ERROR'}, 'The type already exists!')
#                         return {"CANCELLED"}
#                 else:
#                     print('No entities was created')
#                     self.report({'ERROR'}, 'No entities was created!')
#                     return {"CANCELLED"}

                
#             else:
#                 self.report({'ERROR'}, 'Failing connect!')
#                 return {"CANCELLED"}