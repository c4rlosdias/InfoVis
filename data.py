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

last_active = None

# =======================================================================
# Functions
# =======================================================================
def load_contained_elements_by_decomposition(container: ifcopenshell.entity_instance, name_props: str, context : bpy.types.Context ) -> None:
            props = context.scene.og_props        
            def get_decomposition(element: ifcopenshell.entity_instance, is_recursive : bool) -> set[ifcopenshell.entity_instance]:

                queue = [element]            
                results = []

                while queue:
                    element = queue.pop()
                    for rel in getattr(element, "IsGroupedBy", []):
                        related = rel.RelatedObjects
                        queue.extend(related)
                        results.extend(related) 
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
                        #related = [x for x in related if not x.is_a('IfcDistributionPort')]
                        queue.extend(related)
                        results.extend(related)
                    if not is_recursive:
                        break
                return results

            def add_elements(elements, name_props, level=1):
                #l_elements = [x for x in elements]
                for element in elements:                        
                    # if not props.should_include_children and tool.Root.is_spatial_element(element):
                    #     continue
                    # ifc_definition_id = element.id()
                    print(getattr(props, name_props))
                    new = getattr(props, name_props).add()
                    
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
                        add_elements(children, name_props, level=level + 1)
            
            getattr(props, name_props).clear()
            elements = get_decomposition(container, is_recursive=False) 
            add_elements([container], name_props)

# Call back para carregar as propriedades ao mudar o objeto ativo
def call_back():
    bpy.ops.props.load_properties()

# Handler para carregar as propriedades ao mudar o objeto ativo
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    if obj != last_active:
        last_active = obj        
        bpy.ops.props.load_properties()

# Registra o handler
def refresh_classes(context):
    props = context.scene.og_props
    props.classes_shown.clear()
    for classe in props.classes:
        if not classe.is_hidden:
            new_item = props.classes_shown.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type

# Call back para carregar as propriedades ao mudar o objeto ativo
def refresh_products(context):
    props = context.scene.og_props
    props.products_show.clear()
    for classe in props.products:
        if not classe.is_hidden:
            new_item = props.products_show.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type

# Call back para carregar as propriedades ao mudar o objeto ativo
def refresh_types(context):
    props = context.scene.og_props
    props.types_show.clear()
    for classe in props.types:
        if not classe.is_hidden:
            new_item = props.types_show.add()
            new_item.id = classe.id
            new_item.tag = classe.tag
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.element_type = classe.element_type
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden

# Função para desenhar a árvore de classes, produtos ou tipos

def draw_tree(layout, item, operators, attributes, property, only_children = False):

    ''' Desenha uma árvore de classes, produtos ou tipos no layout do blender.
            layout: layout do blender
            item: item da coleção a ser desenhado
            operators: operadores a serem adicionados para cada item
            attributes: atributos a serem mostrados para cada item
            property: nome da propriedade onde a coleção está armazenada
            only_children: se True, mostra apenas os operadores para os itens que tem filhos, caso contrário, mostra para todos os itens
        retorna o layout com a árvore desenhada
    '''
    if not item.is_hidden:
        
        row = layout.row(align=True)
        # adiciona os ícones de hierarquia
        for _ in range(0, item.level - 1):
            row.label(text="", icon="BLANK1")

        # adiciona o ícone de expandir/contrair    
        if item.has_children:
            if item.is_expanded:
                op = row.operator("element.contract_tree", text="", emboss=False, icon="DISCLOSURE_TRI_DOWN")
                op.index = item.index
                op.property = property
            else:
                op=row.operator("element.expand_tree", text="", emboss=False, icon="DISCLOSURE_TRI_RIGHT")
                op.index = item.index
                op.property = property
        else:
            row.label(text="", icon="BLANK1")
  
        # adiciona os atributos do item
        for att in attributes:            
            row.label(text=att[0], icon=att[1])  
        
        # se não for para mostrar apenas os filhos ou se o item não tiver filhos, mostra os operadores
        if not only_children or not item.has_children:
            for opt in operators:
                op = row.operator(opt['name'], text="", icon=opt['icon'])
                for att, value in opt['att']:
                    setattr(op, att, value)

# Call back para carregar as propriedades ao mudar o objeto ativo
def refresh_container(context):
    props = context.scene.og_props
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
            new_item.object_type = classe.object_type  
            new_item.is_selected = classe.is_selected  

# Call back para carregar as propriedades ao mudar o objeto ativo
def refresh_tree(context, property):
    if property == 'classes':
        refresh_classes(context)
    elif property == 'products':
        refresh_products(context)
    elif property == 'types':
        refresh_types(context)
    elif property == 'elements_containers':
        refresh_container(context)

# Função para mover um elemento para dentro de um assembly ou nest
def move_to_assembly(parent, children, type):
    model = tool.Ifc.get()
    if type == 'nests':
        if children.Nests:
            ifcopenshell.api.nest.change_nest(
                model,
                item=children,
                new_parent=parent
            )
        else:
            if children.ContainedInStructure:
                ifcopenshell.api.spatial.unassign_container(model, products=[children])
            ifcopenshell.api.nest.assign_object(
                model,
                related_objects=[children],
                relating_object=parent
            )

    else:
        if children.Decomposes:
            ifcopenshell.api.aggregate.unassign_object(
                model,
                products=[children]
            )
        
        ifcopenshell.api.spatial.unassign_container(model, products=[children])
        ifcopenshell.api.aggregate.assign_object(
            model,
            products=[children],
            relating_object=parent
        )

# Função para mover um elemento para dentro de um assembly ou nest  
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

# Função para obter o valor da propriedade de acordo com o tipo
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

# Função para obter o símbolo da unidade
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

# Função para obter a unidade de uma propriedade
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

# Função para obter a propriedade de acordo com o nome e o pset
def get_property(ifc_obj, pset_name, prop_name):
    model = tool.Ifc.get()
    pset = ifcopenshell.api.pset.add_pset(model, product=ifc_obj, name=pset_name)
    for prop in pset.HasProperties:
        if prop.Name == prop_name:
            return prop
    return None

# Função para obter o pset de acordo com o nome
def get_pset(ifc_obj, pset_name):
    model = tool.Ifc.get()
    pset = ifcopenshell.api.pset.add_pset(model, product=ifc_obj, name=pset_name)
    return pset

# Função para obter as propriedades de um elemento e do seu tipo, e adicionar na coleção de propriedades do addon
def set_properties(props, ifc_obj, is_a, i):     
    if ifc_obj is None:
        return i
    id = ifc_obj.id()
    # get psets    
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
            c = 0
            for association in _pset.HasAssociations:
                document = association.RelatingDocument
                newdocument = new_item.documents.add()
                newdocument.name = document.Name
                newdocument.identification = document.Identification
                newdocument.location = document.Location.wrappedValue 
                newdocument.index = c
                c += 1
                   
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
                                new_prop.description = _prop.Description if _prop.Description is not None else ''
                                new_prop.datatype = get_unit(ifc_obj, pset, prop)
                                new_prop.index = j      
                                new_prop.type_prop = type_prop     
                                set_prop_type(new_prop, item_prop)
                                #c += 1

                        # se é uma propriedade enumerada
                        if type_prop == 'IfcPropertyEnumeratedValue':  
                            new_prop = new_item.props.add()                             
                            new_prop.name = prop  
                            new_prop.description = _prop.Description if _prop.Description is not None else ''
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
                        new_prop.description = _prop.Description if _prop.Description is not None else ''
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

# Função para obter as propriedades de um elemento e do seu tipo, e adicionar na coleção de propriedades do addon
def refresh_props(context):
    # get active object
    props = context.scene.og_props
    props.prop_metadata.clear() 
    props.documents.clear()
    props.has_document = False
    props.document = ''
    obj = context.active_object
    if obj:
        ifc_obj = tool.Ifc.get_entity(obj)
        if ifc_obj is None:
            return
        # se o tipo do elemento tem algum documento associado
        ifc_obj_type = ifcopenshell.util.element.get_type(ifc_obj)
        if getattr(ifc_obj_type, 'HasAssociations', None):
            associations = ifc_obj_type.HasAssociations
            props.has_document = True
            for association in associations:
                if association.is_a('IfcRelAssociatesDocument'):
                    document = association.RelatingDocument
                    newdocument = props.documents.add()
                    newdocument.name = document.Name
                    newdocument.identification = document.Identification
                    if document.Location:
                        newdocument.location = document.Location
                    else:
                        newdocument.location = ''

        ifc_type_obj = ifcopenshell.util.element.get_type(ifc_obj)

        if ifc_obj.is_a('IfcTypeProduct'):
            set_properties(props, ifc_type_obj, "type", 0)
        else:
            i = set_properties(props, ifc_obj, "instance", 0)
            set_properties(props, ifc_type_obj, "type", i)

# Função para expandir ou contrair a árvore de classes, produtos ou tipos
def set_hide_class(context, index, is_hidden):
    props = context.scene.og_props
    level = props.classes[index].level
    for classe in props.classes:
        if classe.index > index:
            if classe.level > level:
                classe.is_hidden = is_hidden                
            else:
                return

# Função para expandir ou contrair a árvore de classes, produtos ou tipos
def set_hide_product(context, index, is_hidden):
    props = context.scene.og_props
    level = props.products[index].level
    for product in props.products:
        if product.index > index:
            if product.level_index > level:
                product.is_hidden = is_hidden                
            else:
                return

# Função para expandir ou contrair a árvore de classes, produtos ou tipos           
def build_products(context, classe, c, level, parent, hide, children):
    c += 1 
    props = context.scene.og_props
    new_product = props.types.add()
    new_product.id        = classe["id"]                 
    new_product.name        = classe["name"]
    new_product.tag        = classe["tag"]
    new_product.description = classe['description']   
    new_product.element_type         = classe["element_type"] 
    new_product.index       =   c  
    new_product.level = level
    new_product.parent = parent
    new_product.is_expanded = False
    new_product.is_hidden = hide
    new_product.has_children = children
    return c

# Função para expandir ou contrair a árvore de classes, produtos ou tipos
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
    new_class.level = level
    new_class.parent = parent
    new_class.is_expanded = False
    new_class.is_hidden = hide
    
    if 'children' in classe:   
        level = level + 1     
        new_class.has_children = True
        for child in classe['children']:            
            c = build_classes(context, child , c, level, classe['name'], True)
            set_hide_class(context, c, True)
    else:
        new_class.has_children = False
    return c

# Classes

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
    def get_ifc_type(cls):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'ifc_types.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

class CDE_Api:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def get_projects(self):
        response = requests.get(f'{self.endpoint}/projects')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_contracts(self):
        #response = requests.get(f'{self.endpoint}/projects/{project_id}/contracts')
        contracts = [
            {
                "id": "ct1",
                "name": "Contracto-001",
                "objects": [
                    {
                        "id" : "TR-001",
                        "name" : "Trench-001",
                        "objects": [
                            {
                                "id" : "AC-001",
                                "name" : "AC-001"
                            },
                            {
                                "id" : "AC-002",
                                "name" : "AC-002"
                            }
                        ]
                    },
                    {
                        "id" : "TR-002",
                        "name" : "Trench-002",
                        "objects": [
                            {
                                "id" : "AC-003",
                                "name" : "AC-003"
                            },
                            {
                                "id" : "AC-004",
                                "name" : "AC-004"
                            }
                        ]
                    }

                ]
            },
            {
                "id": "ct2",
                "name": "Contracto-002",
                "objects": [
                    {
                        "id" : "TR-003",
                        "name" : "Trench-003",
                        "objects": [
                            {
                                "id" : "AC-005",
                                "name" : "AC-005"
                            },
                            {
                                "id" : "AC-006",
                                "name" : "AC-006"
                            }
                        ]
                    },
                    {
                        "id" : "TR-004",
                        "name" : "Trench-004",
                        "objects": [
                            {
                                "id" : "AC-007",
                                "name" : "AC-007"
                            },
                            {
                                "id" : "AC-008",
                                "name" : "AC-008"
                            }
                        ]
                    }

                ]
            }
        ]

        return contracts

    def get_assets(self):
        assets = [
            {
                "id": "as1",
                "name": "Asset-001",
                "objects": [
                    {
                        "id" : "AC-001",
                        "name" : "AC-001"
                    },
                    {
                        "id" : "AC-002",
                        "name" : "AC-002"
                    }
                ]
            },
            {
                "id": "as2",
                "name": "Asset-002",
                "objects": [
                    {
                        "id" : "AC-003",
                        "name" : "AC-003"
                    },
                    {
                        "id" : "AC-004",
                        "name" : "AC-004"
                    }
                ]
            }
        ]
        return assets

    def get_inventory(self):
        inventory = [
            {
                "id": "in1",
                "name": "Inventory-001",
                "objects": [
                    {
                        "id" : "AC-001",
                        "name" : "AC-001"
                    },
                    {
                        "id" : "AC-002",
                        "name" : "AC-002"
                    }
                ]
            },
            {
                "id": "in2",
                "name": "Inventory-002",
                "objects": [
                    {
                        "id" : "AC-003",
                        "name" : "AC-003"
                    },
                    {
                        "id" : "AC-004",
                        "name" : "AC-004"
                    }
                ]
            }
        ]
        return inventory