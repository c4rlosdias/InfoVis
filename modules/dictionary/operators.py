import os
import json
import bpy
from tqdm import tqdm
from ifctester import ids
import ifcopenshell
import ifcopenshell.util.selector as selector
import bonsai.tool as tool

from ...data.bsdd import bSDD
from ...data.catalog import PropTempl
from ...data.ifc_utils import build_classes, get_prop_type
from ...data.tree import refresh_classes
from ..common.operators import _open_in_browser


class Operator_clear_properties(bpy.types.Operator):
    """"""
    bl_idname  = "object.clear_prop"
    bl_label   = "Clear properties"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.og_props
        props.ifc_prop.clear()              
        return {"FINISHED"}    


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
        _open_in_browser(self.uri)        
        return {"FINISHED"}


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
        bSDD.set_uri(props.dictionary)
        result = bSDD.load_classes(True)        
        if result:
            for classe in bSDD.data_class:  
                new_c = build_classes(context, classe, c, 1, '', False)
                c = new_c
            refresh_classes(context)
            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}


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
                    bSDD.set_uri(props.dictionary)
                    result = bSDD.get_property()
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

           
class Operator_export_ids(bpy.types.Operator):
    """"""
    bl_idname  = "ids.export"
    bl_label   = "Export ids file"
    bl_options = {"REGISTER", "UNDO"}
    filepath : bpy.props.StringProperty(subtype="FILE_PATH")
    filte_glob : bpy.props.StringProperty(default='*.ids', options={'HIDDEN'})
    
    def get_data_type(self, units):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "resources", "units.json"), 'r', encoding='utf-8') as file:
            units_data = json.load(file)
        data_type = units_data[units] if units in units_data else 'IfcLabel'
        return data_type

    def get_children(self, classe):
            if 'children' in classe:
                leaves = []
                for child in classe['children']:
                    leaves.extend(self.get_children(child))
                return leaves
            else:
                return [classe]
            
    def execute(self, context):
        props = context.scene.og_props
        props.ids_file = self.filepath

        data = bSDD.data_class
        if len(data) == 0:
            self.report({'ERROR'}, "No data to export. Please load the classes from bSDD first.")
            return {"CANCELLED"}
        
        data_classes = []
        for classe in tqdm(data, total=len(data), desc='Processing classes:'):
            leaves = self.get_children(classe)
            for leave in leaves:
                response = bSDD.get_class(leave['uri'], True)
                if response:
                    data_classes.append(bSDD.data_info_class)

        my_ids = ids.Ids(
            title='Oil & Gas Subsea',
            copyright='Petrobras',
            author='ÇERTI',
            description='Requirements for properties at subsea projects Oil&Gas',
            purpose='',
            milestone=''
        )

        for classe in tqdm(data_classes, total=len(data_classes), desc='Processing specifications:'):
            if 'classProperties' in classe:             
                my_spec = ids.Specification(
                    name='Specification for ' + classe['referenceCode'],
                    description='',
                    minOccurs=1,
                    maxOccurs='unbounded',
                    ifcVersion='IFC4'
                )

                entity = ids.Entity(
                    name=classe['relatedIfcEntityNames'][0] if 'relatedIfcEntityNames' in classe and len(classe['relatedIfcEntityNames']) > 0 else 'Undefined',
                    predefinedType='USERDEFINED'
                )

                attribute = ids.Attribute(
                    name='ElementType' if classe['relatedIfcEntityNames'][0][-4:] == 'Type' else 'ObjectType',
                    value=classe['referenceCode']
                )

                my_spec.applicability.append(entity)
                my_spec.applicability.append(attribute)

                for prop in classe['classProperties']:                
                    property = ids.Property(
                        baseName= prop['name'],
                        propertySet= prop['propertySet'],
                        dataType= self.get_data_type(prop['units'][0]) if 'units' in prop else 'IfcLabel',
                        cardinality='required',
                        uri=prop['uri']
                    )

                    my_spec.requirements.append(property)

                my_ids.specifications.append(my_spec)
        
        try:
            my_ids.to_xml(self.filepath)
            self.report({'OPERATOR'}, f'IDS file exported successfully to {self.filepath}')
            return {'FINISHED'}
        except Exception as ex:
            self.report({'ERROR'}, str(ex))
            return {"CANCELLED"}

    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
