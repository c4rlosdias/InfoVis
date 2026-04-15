import numpy as np
import pandas as pd
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.unit
import bonsai.tool as tool


def set_prop_type(prop, value_prop):
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
    if ifc_obj is None:
        return i
    id = ifc_obj.id()
    psets = ifcopenshell.util.element.get_psets(ifc_obj, should_inherit=False)    
    print(psets)
    for pset, _props in psets.items():             
        _pset = get_pset(ifc_obj, pset)        
        table = {}    

        new_item = props.prop_metadata.add()            
        new_item.name = pset  
        new_item.is_a = is_a 
        new_item.id_obj = id          
        new_item.index = i     

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
                        _prop = get_property(ifc_obj, pset, prop)

                        if _prop is not None: 
                            type_prop = _prop.is_a()
                        else:
                            type_prop = ''

                        if type_prop == 'IfcPropertyListValue':
                            for item_prop in value:    
                                new_prop = new_item.props.add() 
                                new_prop.name = prop
                                new_prop.description = _prop.Description if _prop.Description is not None else ''
                                new_prop.datatype = get_unit(ifc_obj, pset, prop)
                                new_prop.index = j      
                                new_prop.type_prop = type_prop     
                                set_prop_type(new_prop, item_prop)

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
                    else:
                        _prop = get_property(ifc_obj, pset, prop)

                        new_prop = new_item.props.add()  
                        new_prop.name = prop
                        new_prop.description = _prop.Description if _prop.Description is not None else ''
                        new_prop.datatype = get_unit(ifc_obj, pset, prop)
                        new_prop.index = j                                                
                        set_prop_type(new_prop, value)        
            j += 1

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
                        newdocument.location = str(document.Location)
                    else:
                        newdocument.location = ''

        ifc_type_obj = ifcopenshell.util.element.get_type(ifc_obj)

        if ifc_obj.is_a('IfcTypeProduct'):
            set_properties(props, ifc_type_obj, "type", 0)
        else:
            i = set_properties(props, ifc_obj, "instance", 0)
            set_properties(props, ifc_type_obj, "type", i)


def set_hide_class(context, index, is_hidden):
    props = context.scene.og_props
    level = props.classes[index].level
    for classe in props.classes:
        if classe.index > index:
            if classe.level > level:
                classe.is_hidden = is_hidden                
            else:
                return


def set_hide_product(context, index, is_hidden):
    props = context.scene.og_props
    level = props.products[index].level
    for product in props.products:
        if product.index > index:
            if product.level_index > level:
                product.is_hidden = is_hidden                
            else:
                return

           
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


def add_connections(obj_a, obj_b, obj_c, connect_type="IfcRelConnectsWithRealizingElements"):   
    model = tool.Ifc.get()
    element_a = tool.Ifc.get_entity(obj_a)
    element_b = tool.Ifc.get_entity(obj_b)
    element_c = tool.Ifc.get_entity(obj_c)
    if element_a and element_b:
        if connect_type == "IfcRelConnectsPorts":
            rel = model.create_entity(
                "IfcRelConnectsPorts",
                GlobalId=ifcopenshell.guid.new(),
                RelatingPort=element_a,
                RelatedPort=element_b,
                RealizingElement=element_c if element_c else None
            )
        elif connect_type == "IfcRelConnectsElements":
            rel = model.create_entity(
                "IfcRelConnectsElements",
                GlobalId=ifcopenshell.guid.new(),
                RelatingElement=element_a,
                RelatedElement=element_b
            )
        elif connect_type == "IfcRelConnectsWithRealizingElements":
            rel = model.create_entity(
                "IfcRelConnectsWithRealizingElements",
                GlobalId=ifcopenshell.guid.new(),
                RelatingElement=element_a,
                RelatedElement=element_b,
                RealizingElements=[element_c]
            )

        return rel
    else:
        return None
