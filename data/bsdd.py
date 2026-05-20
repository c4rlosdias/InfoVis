import os

import requests
import ifcopenshell
import ifcopenshell.util.selector as selector
import json
import os.path


class bSDD:
    data_dic =[] #(Version, Name, Version)
    data_info_prop =[]# (URI, Name, Description, DataType, Unit, AllowedValues) 
    data_info_class={} # (URI, Name, Description, RelatedIfcEntityNames, IsAbstract, IsDeprecated)
    data_class_prop = [] # (ClassUri, PropertyUri, Name, Description, DataType, Unit, AllowedValues)
    properties = [] # (URI, Name, Description, DataType, Unit, AllowedValues)
    data_prop = {} # (URI, Name, Description, DataType, Unit, AllowedValues)
    data_class = {} # (URI, Name, Description, RelatedIfcEntityNames, IsAbstract, IsDeprecated)
    response = ''
    is_loaded = False
    endpoint = 'https://api.bsdd.buildingsmart.org/api/'
    uri = None    

    @classmethod
    def set_uri(cls, uri):
        cls.uri = uri

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
    def load_classes(cls, use_nested : bool) -> bool: 
          
        params = {
            'uri' : f'{cls.uri}',
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
    def load_properties(cls) -> bool:        

        params = {'uri' : f'{cls.uri}'}
        response = requests.get(f'{cls.endpoint}Dictionary/v1/Properties', params=params)        
        if response.status_code == 200:            
            cls.data_prop = response.json()['properties']
            return True
        else:
            cls.response = response.text
            return False
    
    @classmethod
    def get_class(cls, uri : str, include_properties : bool = False) -> bool:        

        params = {'uri' : uri, 'includeClassProperties' : include_properties}
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
