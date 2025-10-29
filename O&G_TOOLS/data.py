import requests
import logging
import pandas as pd
import os
import json
import bpy
import numpy as np
import ifcopenshell
import ifcopenshell.util.selector as selector
import bonsai.tool as tool
from bonsai.bim.ifc import IfcStore
from bonsai.bim import import_ifc
from bonsai.bim.ifc import IfcStore

# funções

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

def refresh_products(context):
    props = context.scene.my_props
    props.products_show.clear()
    for classe in props.products:
        if not classe.is_hidden:
            new_item = props.products_show.add()
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

def set_prop_type( prop, value_prop):
    res = ""
    if type(value_prop) == str:
        prop.valuestr = value_prop
        prop.type_value = "str"
    elif type(value_prop) == int:
        prop.valueint = value_prop
        prop.type_value = "int"
    elif type(value_prop) == float or type(value_prop) == np.float64:
        prop.valuefloat = value_prop
        prop.type_value = "float"
    elif type(value_prop) == bool:
        prop.valuebool = value_prop
        prop.type_value = "bool"
    else:
        prop.valuestr = str(value_prop)
        prop.type_value = "str"

def get_prop_type(prop):
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

def get_unit_symbol(unit):
    symbol = ''
    if unit.is_a() == 'IfcDerivedUnit':                    
        for sub_unit in unit.Elements: 
            sub_symbol = ifcopenshell.util.unit.get_unit_symbol(sub_unit.Unit)
            complement = str(sub_unit.Exponent)
            sep = '/' if '-'in complement else ''
            symbol += sep + sub_symbol + complement.replace('-', '')
    else:
        symbol=ifcopenshell.util.unit.get_unit_symbol(unit)
    return symbol.replace('1', '')

def get_unit(ifc_obj, pset_name, prop_name):
    model = tool.Ifc.get()
    psets = ifcopenshell.util.element.get_psets(ifc_obj, should_inherit=False)
    pset = model.by_id(psets[pset_name]['id'])
    symbol = ''
    for prop in pset.HasProperties:        
        if prop.Name == prop_name:
            unit = ifcopenshell.util.unit.get_property_unit(ifc_file=model, prop=prop)
            if unit is not None:
                symbol =f'[{get_unit_symbol(unit)}]'
            else:
                symbol=''
            return symbol
    return symbol

def get_property(ifc_obj, pset_name, prop_name):
    model = tool.Ifc.get()
    pset = ifcopenshell.api.pset.add_pset(model, product=ifc_obj, name=pset_name)
    for prop in pset.HasProperties:
        if prop.Name == prop_name:
            return prop
    return None

def get_pset(ifc_obj, pset_name):
    model = tool.Ifc.get()
    pset = ifcopenshell.api.pset.add_pset(model, product=ifc_obj, name=pset_name)
    return pset

def set_properties(props, ifc_obj, is_a, i):     
    id = ifc_obj.id()
    # get psets
    print(ifc_obj)
    psets = ifcopenshell.util.element.get_psets(ifc_obj, should_inherit=False)
    print(psets)
    for pset, _props in psets.items():             
        _pset = get_pset(ifc_obj, pset)        
        table = {}    

        # cria um novo item
        new_item = props.prop_metadata.add()            
        new_item.name = pset  
        new_item.is_a = is_a 
        new_item.id_obj = id          
        new_item.index = i     

        # se o pset tem algum documento associado
        if _pset.HasAssociations:
            new_item.has_document = True
            new_item.document = _pset.HasAssociations[0].RelatingDocument.Location.wrappedValue        
        j = 0   
           
        for prop, value in _props.items():           
            if prop != 'id':  
                if 'Table' in prop:
                    _prop = get_property(ifc_obj, pset, prop)
                    table[f'{prop}||{_prop.Description}']=value
                else:               
                    if type(value) == list:
                        # obtem a propriedade
                        _prop = get_property(ifc_obj, pset, prop)

                        # verifica o tipo da propriedade
                        if _prop is not None: 
                            type_prop = _prop.is_a()
                        else:
                            type_prop = ''

                        # se é uma propriedade de lista
                        if type_prop == 'IfcPropertyListValue':
                            #c = 0
                            for item_prop in value:    
                                new_prop = new_item.props.add() 
                                new_prop.name = prop
                                new_prop.description = _prop.Description
                                new_prop.datatype = get_unit(ifc_obj, pset, prop)
                                new_prop.index = j      
                                new_prop.type_prop = type_prop     
                                set_prop_type(new_prop, item_prop)
                                #c += 1

                        # se é uma propriedade enumerada
                        if type_prop == 'IfcPropertyEnumeratedValue':  
                            new_prop = new_item.props.add()                             
                            new_prop.name = prop  
                            new_prop.description = _prop.Description 
                            new_prop.index = j      
                            new_prop.type_prop = type_prop   
                            new_prop.datatype = get_unit(ifc_obj, pset, prop)                                                        
                            values = [x.wrappedValue for x in _prop.EnumerationValues ]
                            for enumval in  _prop.EnumerationReference.EnumerationValues:
                                new_value = new_prop.enumerations.add()
                                if enumval.wrappedValue in values:
                                    new_value.enumerated = True
                                else:
                                    new_value.enumerated = False
                                set_prop_type(new_value, enumval.wrappedValue) 
                    # se não é uma propriedade de lista nem enumerada
                    else:
                        _prop = get_property(ifc_obj, pset, prop)
                        # verifica se tem documento associado
                        

                        new_prop = new_item.props.add()  
                        new_prop.name = prop
                        new_prop.description = _prop.Description
                        new_prop.datatype = get_unit(ifc_obj, pset, prop)
                        new_prop.index = j                                                
                        set_prop_type(new_prop, value)        
            j += 1

        # trata a tabela
        if len(table) > 0:
            df = pd.DataFrame(table)
            dft = df.transpose()
            columns = df.columns.tolist()    
            nc = len(columns)  
            nr = len(df)
            for index, row in dft.iterrows():   
                for col, val in row.items():
                    name = index.split('||')[0]
                    description = index.split('||')[1]
                    new_prop = new_item.props.add()
                    new_prop.name = name
                    new_prop.description = description
                    new_prop.n_columns = nc 
                    new_prop.n_rows = nr                         
                    new_prop.index = j    
                    new_prop.type_prop = 'table'  
                    new_prop.datatype = get_unit(ifc_obj, pset, name)         
                    set_prop_type(new_prop, val)

        i += 1
    return i

def refresh_props(context):
    # get active object
    props = context.scene.my_props
    props.prop_metadata.clear() 
    props.has_document = False
    props.document = ''
    obj = context.active_object
    ifc_obj = tool.Ifc.get_entity(obj)

    # se o tipo do elemento tem algum documento associado
    ifc_obj_type = ifcopenshell.util.element.get_type(ifc_obj)
    if ifc_obj_type.HasAssociations:
        props.has_document = True
        props.document = ifc_obj_type.HasAssociations[0].RelatingDocument.Location.wrappedValue  

    ifc_type_obj = ifcopenshell.util.element.get_type(ifc_obj)

    i = set_properties(props, ifc_obj, "instance", 0)
    set_properties(props, ifc_type_obj, "type", i)

# classes

class Import_ifc():

    file : ifcopenshell.file

    @classmethod
    def import_type_from_ifc(self, element: ifcopenshell.entity_instance, context: bpy.types.Context) -> None:
        self.file = tool.Ifc.get()
        logger = logging.getLogger("ImportIFC")
        ifc_import_settings = import_ifc.IfcImportSettings.factory(context, IfcStore.path, logger)

        ifc_importer = import_ifc.IfcImporter(ifc_import_settings)
        ifc_importer.file = self.file
        ifc_importer.process_context_filter()
        ifc_importer.material_creator.load_existing_materials()
        self.import_materials(element, ifc_importer)
        self.import_styles(element, ifc_importer)
        ifc_importer.create_element_type(element)
        ifc_importer.place_objects_in_collections()

    @classmethod
    def import_materials(self, element: ifcopenshell.entity_instance, ifc_importer: import_ifc.IfcImporter) -> None:
        for material in ifcopenshell.util.element.get_materials(element):
            if tool.Ifc.get_object_by_identifier(material.id()):
                continue
            self.import_material_styles(material, ifc_importer)

    @classmethod
    def import_styles(self, element: ifcopenshell.entity_instance, ifc_importer: import_ifc.IfcImporter) -> None:
        if element.is_a("IfcTypeProduct"):
            representations = element.RepresentationMaps or []
        elif element.is_a("IfcProduct"):
            representations = [element.Representation] if element.Representation else []
        for representation in representations or []:
            for element in self.file.traverse(representation):
                if not element.is_a("IfcRepresentationItem") or not element.StyledByItem:
                    continue
                for element2 in self.file.traverse(element.StyledByItem[0]):
                    if element2.is_a("IfcSurfaceStyle") and not tool.Ifc.get_object_by_identifier(element2.id()):
                        ifc_importer.create_style(element2)

    @classmethod
    def import_material_styles(
        self,
        material: ifcopenshell.entity_instance,
        ifc_importer: import_ifc.IfcImporter,
    ) -> None:
        if not material.HasRepresentation:
            return
        for element in self.file.traverse(material.HasRepresentation[0]):
            if element.is_a("IfcSurfaceStyle") and not tool.Ifc.get_object_by_identifier(element.id()):
                ifc_importer.create_style(element)

class bSDD:
    data_dic =[]
    data_info_prop =[]
    data_info_class={}
    data_class_prop = []
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
    def load_classes(cls, version : str, use_nested : bool) -> bool:        
        params = {
            'uri' : f'{cls.uri}/{version}',
            'UseNestedClasses' : use_nested
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
    def get_class_prop(cls, uri : str) -> bool:        
        params = {'ClassUri' : uri}
        response = requests.get(f'{cls.endpoint}Class/Properties/v1', params=params)        
        if response.status_code == 200:                        
            cls.data_class_prop = response.json()
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
        description = metadata['description']   
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
                prop_templ.Description=description
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
    def get_type_(cls, product):
        with open(f'./resources/{product}.ttl', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @classmethod
    def get_type(cls, product):
        with open(f'./resources/{product}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data





