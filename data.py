import requests
import os
import ifcopenshell
import ifcopenshell.util.selector as selector
import bonsai.tool as tool
from bonsai.bim.ifc import IfcStore
import json


def refresh(context):
    props = context.scene.my_props
    props.classes_shown.clear()
    for classe in props.classes:
        if not classe.is_hidden:
            new_item = props.classes_shown.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level_index = classe.level_index
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type

def refresh_container(context):
    props = context.scene.my_props
    props.containers_show.clear()
    for classe in props.elements_containers:
        if not classe.is_hidden:
            new_item = props.containers_show.add()            
            new_item.name = classe.name            
            new_item.level = classe.level 
            new_item.id = classe.id           
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type  
            new_item.is_selected = classe.is_selected  

class bSDD:
    data_dic =[]
    data_info_prop =[]
    data_info_class={}
    properties = []
    data_prop = {}
    data_class = {}
    response = ''
    is_loaded = False
    endpoint = 'https://api.bsdd.buildingsmart.org/api/'
    uri = 'https://identifier.buildingsmart.org/uri/bimcerti/subsea-flexible-pipes'
        

    @classmethod
    def load_dictionaries(cls):
        cls.is_loaded = True
        params = {'Uri' : cls.uri}
        response = requests.get(f'{cls.endpoint}/Dictionary/v1', params=params)
        if response.status_code == 200:            
            dictionaries = response.json()['dictionaries']            
            for dic in dictionaries:
                cls.data_dic.append((dic['version'],f"{dic['name']} V{dic['version']}",dic['version']))
        else:
            cls.data_dic = [('0', 'ERROR connecting to bSDD', '')]

    @classmethod
    def load_classes(cls, version : str) -> bool:        
        params = {
            'uri' : f'{cls.uri}/{version}',
            'UseNestedClasses' : True
        }
        response = requests.get(f'{cls.endpoint}Dictionary/v1/Classes', params=params)        
        if response.status_code == 200:            
            cls.data_class = response.json()['classes']
            return True
        else:
            cls.response = response.text
            return False
        
    @classmethod
    def load_properties(cls, version : str) -> bool:        
        params = {'uri' : f'{cls.uri}/{version}'}
        response = requests.get(f'{cls.endpoint}Dictionary/v1/Properties', params=params)        
        if response.status_code == 200:            
            cls.data_prop = response.json()['properties']
            return True
        else:
            cls.response = response.text
            return False
    
    @classmethod
    def get_class(cls, uri : str) -> bool:        
        params = {'uri' : uri}
        response = requests.get(f'{cls.endpoint}Class/v1', params=params)        
        if response.status_code == 200:            
            cls.data_info_class = response.json()
            return True
        else:
            cls.response = response.text
            return False
    
    @classmethod
    def get_property(cls, uri : str) -> bool:        
        params = {'uri' : uri, 'includeClasses' : True}
        response = requests.get(f'{cls.endpoint}Property/v4', params=params)        
        if response.status_code == 200:            
            cls.data_info_prop = response.json()
            return True
        else:
            cls.response = response.text
            return False
        
class PropTempl:
    template = None
    filepath = None
    # Obtem o arquivo template de propriedades
    @classmethod
    def get_template(cls):   
        cls.filepath = (tool.Blender.get_data_dir_path("pset") / "EPset_OG.ifc").__str__()             
        file_exist = os.path.exists(cls.filepath)
        if file_exist:
            cls.template = ifcopenshell.open(cls.filepath)
        else:
            cls.template = ifcopenshell.file() 

    # Checa se a property template existe associada ao property set template
    @classmethod
    def get_prop(cls, prop_name, pset_name, template):
        result = None
        props = selector.filter_elements(template, f"IfcPropertyTemplate, Name={prop_name}")
        for prop in props:
            if prop.PartOfPsetTemplate[0].Name == pset_name:
                result = prop
        return result


    # Add properties and unit to elements
    @classmethod
    def add_pset_template(cls, metadata):
        # Verificar se o arquivo existe, se não criar um
        if cls.template is None:
            cls.get_template()

        # Abre o arquivo com os tip[os dos valores de acordo com a unidade
        with open('./resources/units.json', 'r') as file:
            d_types = json.load(file)

        
        prop_type = {
            "single" : "P_SINGLEVALUE",
            "list"   : "P_LISTVALUE",
            "range"  : "P_BOUNDEDVALUE"
        }
        prop_name = metadata['code']
        data_type = metadata['dataType']
        units = metadata['units']    
        definition = metadata['definition']
        if metadata['propertyValueKind'] in prop_type:
            template_type = prop_type[metadata['propertyValueKind']]
        else:
            template_type = 'P_SINGLEVALUE'

        # Seleciona o data type correto
        if metadata['dataType'] == 'Boolean':
            data_type = 'IfcBoolean'
        elif metadata['dataType'] == 'String':
            data_type = 'IfcLabel'
        elif metadata['dataType'] == 'Integer':
            data_type == 'IfcInteger'
        else:
            if len(units) > 0:
                unit = units[0]
            else:
                unit = ''
            data_type = d_types[unit] if unit in d_types else 'IfcReal'

        # ser for uma propriedade com valores validos, cria uma propriedade enumedada
        if "allowedValues" in metadata:
            template_type = 'P_ENUMERATEDVALUE'
            values = []
            for allowed_value in metadata['allowedValues']:
                is_enumeration = True
                value = ifcopenshell.create_entity(data_type)
                value.wrappedValue = allowed_value['value']
                values.append(value)
            enumerations = ifcopenshell.create_entity('IfcPropertyEnumeration')
            enumerations.EnumerationValues=values
            cls.template.add(enumerations)
            enumerators = cls.template.add(enumerations)
        else:
            enumerators = None

        # Para cada classe criar a propriedade conforme o pset
        for classe in metadata['propertyClasses']:
            pset_name = classe['propertySet']
            object_type = classe['code']

            # verifica para qual classe ifc o pset deve ser usadado
            result = bSDD.get_class(classe['uri'])
            if result:
                if 'relatedIfcEntityNames' in bSDD.data_info_class:
                    if len(bSDD.data_info_class['relatedIfcEntityNames']) > 0:
                        ifc_class = bSDD.data_info_class['relatedIfcEntityNames'][0]
                    else:
                        ifc_class = 'IfcObject, IfcObjectType'
                else:
                    ifc_class = 'IfcObject, IfcObjectType'
            else:
                ifc_class = 'IfcObject, IfcObjectType'

            # se o pset já existe no arquivo, edita ele
            search = selector.filter_elements(cls.template, f"IfcPropertySetTemplate, Name={pset_name}")
            aplicable_entity = f'{ifc_class}/{object_type}' if ifc_class != 'IfcMaterial' else ifc_class
            if len(search) > 0:                 
                pset_templ = list(search)[0]
                attributes = {
                    'ApplicableEntity' : aplicable_entity,                    
                }
                ifcopenshell.api.pset_template.edit_pset_template(
                    cls.template,
                    pset_template = pset_templ,
                    attributes = attributes 
                )
            else:
                # caso contrario cria o pset
                pset_templ = ifcopenshell.api.pset_template.add_pset_template(
                    cls.template,
                    name=pset_name,
                    applicable_entity= aplicable_entity
                )

            # Se existe a propriedade naquele pset edita ela
            prop_templ = cls.get_prop(prop_name, pset_name, cls.template)
            if prop_templ is not None:
                prop_templ.Description=definition
                prop_templ.PrimaryMeasureType=data_type
                prop_templ.TemplateType=template_type
                prop_templ.Enumerators=enumerators
            

            else:
                # caso contrario cria a propriedade
                property_template = ifcopenshell.api.pset_template.add_prop_template(
                    cls.template,
                    description=definition,
                    pset_template=pset_templ,
                    name=prop_name,
                    primary_measure_type = data_type,
                    template_type = template_type,                    
                )
                property_template.Enumerators=enumerators            
        # grava o template
        
        if cls.filepath is not None:
            cls.template.write(cls.filepath)
            return True
        else:
            return False

class Catalog:

    @classmethod
    def get_type(cls, product):
        with open(f'./resources/{product}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(data)
        return data






