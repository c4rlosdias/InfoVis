import bpy
from ifctester import ids
import os
from tqdm import tqdm
import ifcopenshell.util.element as element
import ifcopenshell.util.selector as selector
import ifcopenshell.api.root.create_entity as create_entity
import ifcopenshell.api.material as material
import ifcopenshell.api.geometry as geometry
import ifcopenshell
import webbrowser
from .data import bSDD, PropTempl,Catalog, refresh, refresh_container
import bonsai.tool as tool

def set_hide(context, index, is_hidden):
        props = context.scene.my_props
        level = props.classes[index].level_index
        for classe in props.classes:
            if classe.index > index:
                if classe.level_index > level:
                    classe.is_hidden = is_hidden                
                else:
                    return


def build_classes(context, classe, c, level, parent, hide):
    c += 1 
    props = context.scene.my_props
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
            set_hide(context, c, True)
    else:
        new_class.has_children = False
    return c
# ==================================================================================================
# Cria o elemento IFc a partir dos dados do dicionário
# ==================================================================================================
class Operator_create(bpy.types.Operator):
    """create IFC element from bSDD data"""
    bl_idname  = "object.create"
    bl_label   = "uri property"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    @classmethod
    def classify(self, entity, data):
        objecttype = data['referenceCode']
        if objecttype[-4:] == 'Type':
            type = element.get_type(entity)
            if type is not None:
                type=type[0]
                type.ElementType = objecttype
                type.Description = data['description']
                type.PredefinedType = 'USERDEFINED'
                entity.PredefinedType = None
                entity.ObjectType = None
                return True
            else:
                return False

        else:
            entity.PredefinedType = 'USERDEFINED'
            entity.ObjectType = objecttype
            entity.Description = data['description']
            return True
    
    def execute(self, context):                
        objs = context.selected_objects
        if len(objs)>0:    
            result = bSDD.get_class(self.uri)                         
            if result: 
                if 'relatedIfcEntityNames' in bSDD.data_info_class:
                    ifc_type = bSDD.data_info_class['relatedIfcEntityNames'][0]
                    for obj in objs:
                        entity = tool.Ifc.get_entity(obj)
                        if entity.is_a(ifc_type) or entity.is_a(ifc_type[:-4]):
                            result = self.classify(entity, bSDD.data_info_class)
                            if result:
                                print(f'{entity.Name} classified')
                            else:
                                print(f'{entity.Name} not classified')

                        else:
                            self.report({'ERROR'}, 'this class is not compatible')
                            return {'CANCELLED'}
                    return {"FINISHED"}
                else:
                    self.report({'ERROR'}, 'this class is not compatible')
                    return {'CANCELLED'} 
            else:
                self.report({'ERROR'}, 'error connecting bSDD')
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, 'No selected objects')
            return {"CANCELLED"}
    
# ==================================================================================================
# acerra a uri na propriedade no bSDD
# ==================================================================================================
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
    
# ==================================================================================================
# connect to bSDD and get the properties of Oil & Gas Subsea data dictionary
# ==================================================================================================
class Operator_get_properties(bpy.types.Operator):
    """connect to bSDD and get the properties of Oil & Gas Subsea data dictionary"""
    bl_idname  = "bsdd.get_prop"
    bl_label   = "Get properties from bSDD"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.my_props
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





# ==================================================================================================
# connect to bSDD and get the classes of Oil & Gas Subsea data dictionary
# ==================================================================================================
class Operator_get_classes(bpy.types.Operator):
    """ connect to bSDD and get the classes of Oil & Gas Subsea data dictionary"""
    bl_idname  = "bsdd.get_class"
    bl_label   = "Get classes from bSDD"
    bl_options = {"REGISTER", "UNDO"}

    
    
    
    def execute(self, context):                
        props = context.scene.my_props               
        props.classes.clear()
        props.classes_loaded = False
        c = -1
        result = bSDD.load_classes(props.dictionary)
        if result:
            for classe in bSDD.data_class:  
                new_c = build_classes(context, classe, c, 1, '', False)
                c = new_c
            refresh(context)
            return {"FINISHED"} 
        else:
            self.report({'ERROR'}, bSDD.response)
            return {"CANCELLED"}

# ==================================================================================================
# expand container
# ==================================================================================================
class Operator_expand_classes(bpy.types.Operator):
    """"""
    bl_idname  = "object.expand_classes"
    bl_label   = "Expand classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.my_props  
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

# ==================================================================================================
# contract container
# ==================================================================================================
class Operator_contract_classes(bpy.types.Operator):
    """"""
    bl_idname  = "object.contract_classes"
    bl_label   = "Contract classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.my_props  
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

# ==================================================================================================
# clear the list of properties loaded
# ==================================================================================================
class Operator_clear_properties(bpy.types.Operator):
    """"""
    bl_idname  = "object.clear_prop"
    bl_label   = "Clear properties"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.my_props
        props.ifc_prop.clear()              
        return {"FINISHED"}    
    
# ==================================================================================================
# assign all objects
# ==================================================================================================
class Operator_assign_all(bpy.types.Operator):
    """"""
    bl_idname  = "object.assign_all"
    bl_label   = "Assign all objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.my_props
        for obj in props.ifc_prop:
            obj.is_selected = True              
        return {"FINISHED"}         

# ==================================================================================================
# unassign all objects
# ==================================================================================================
class Operator_unassign_all(bpy.types.Operator):
    """"""
    bl_idname  = "object.unassign_all"
    bl_label   = "Assign all objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                
        props = context.scene.my_props
        for obj in props.ifc_prop:
            obj.is_selected = False              
        return {"FINISHED"}    

# ==================================================================================================
# Add selected properties to Pset template
# ==================================================================================================
class Operator_add_properties(bpy.types.Operator):
    """"""
    bl_idname  = "object.add_prop"
    bl_label   = "Add properties to selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):                        
        props = context.scene.my_props
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


# ==================================================================================================
# get property metadata 
# ==================================================================================================
class Operator_get_prop_info(bpy.types.Operator):
    """"""
    bl_idname  = "property.get_prop_info"
    bl_label   = "get property metadata"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    def execute(self, context):                
        props = context.scene.my_props
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

# ==================================================================================================
# get class metadata 
# ==================================================================================================
class Operator_get_class_info(bpy.types.Operator):
    """Get active class information"""
    bl_idname  = "bsdd.get_class_info"
    bl_label   = "get class metadata"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    def execute(self, context):                
        props = context.scene.my_props
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

    
# ==================================================================================================
# export IDS file 
# ==================================================================================================
class Operator_export_ids(bpy.types.Operator):
    """"""
    bl_idname  = "ids.export"
    bl_label   = "Export ids file"
    bl_options = {"REGISTER", "UNDO"}
    filepath : bpy.props.StringProperty(subtype="FILE_PATH")
    filte_glob : bpy.props.StringProperty(default='*.ids', options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.my_props
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
# load decomposition
# ==================================================================================================
class Operator_load_decomposition(bpy.types.Operator):
    """Get active class information"""
    bl_idname  = "elements.decomposition"
    bl_label   = ""
    bl_options = {"REGISTER", "UNDO"}

    
    @classmethod
    def load_contained_elements_by_decomposition(cls, container: ifcopenshell.entity_instance, context) -> None:
        props = context.scene.my_props
        
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
                new.name = f"[{element.is_a()}] {element.Name or 'Unnamed'}"
                new.type = element.is_a()
                new.level = level 
                new.id = element.id()
                new.id=element.id()
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
        #add_elements(elements)

           

    def execute(self, context):                       
        props = context.scene.my_props
        props.elements_containers.clear()
        model = tool.Ifc.get()
        #elements = selector.filter_elements(model, "IfcElement, IsNestedBy != (), Nests = ()")   
        
        # spatial_elements =  [
        #     e for e in model.by_type('IfcSpatialElement')
        #     if not ifcopenshell.util.element.get_aggregate(e).is_a('IfcProject')
        # ]
        
        # product_elements = [
        #     e for e in model.by_type("IfcProduct")
        #     if e.Nests == () and e.Decomposes == ()
        # ]

        #elements = spatial_elements 
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

# ==================================================================================================
# expand decomposition container
# ==================================================================================================
class Operator_expand_decomposition(bpy.types.Operator):
    """"""
    bl_idname  = "element.expand_decomposition"
    bl_label   = "Expand classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.my_props  
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

# ==================================================================================================
# contract decomposition container
# ==================================================================================================
class Operator_contract_decomposition(bpy.types.Operator):
    """"""
    bl_idname  = "element.contract_decomposition"
    bl_label   = "Contract classes"
    bl_options = {"REGISTER", "UNDO"}
    index : bpy.props.IntProperty(name="index")

    def execute(self, context):                
        props = context.scene.my_props       
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

# ==================================================================================================
# element decomposition selection
# ==================================================================================================
class Operator_element_selection(bpy.types.Operator):
    """"""
    bl_idname  = "element.selection"
    bl_label   = "Select objects"
    bl_options = {"REGISTER", "UNDO"}    
    index : bpy.props.IntProperty(name="index")


    def execute(self, context):   
        props = context.scene.my_props       
        item =  props.elements_containers[self.index] 
        item.is_selected = not item.is_selected  
                     
        model = tool.Ifc.get()
        ifc_element = model.by_id(item.id)
        obj=tool.Ifc.get_object(ifc_element)
        if obj:
            obj.select_set(item.is_selected)            
            if item.is_selected:
                bpy.context.view_layer.objects.active =  obj
            else:
                obj_i = context.selected_objects            
                bpy.context.view_layer.objects.active =  obj_i[0] if len(obj_i) > 0 else None

        refresh_container(context) 
        return {"FINISHED"} 
    
# ==================================================================================================
# CATALOG
# ==================================================================================================

# ==================================================================================================
# Export entity in json
# ==================================================================================================

class Operator_catalog_export(bpy.types.Operator):
    """"""
    bl_idname  = "catag.exp_json"
    bl_label   = "export element in json"
    bl_options = {"REGISTER", "UNDO"}    

    def make_entity(self, model, json):
        model.transaction
        ent = model.create_entity(json['ifc_class'])
        if hasattr(ent, 'GlobalId'):
            ent.GlobalId = ifcopenshell.guid.new()

        for key, value in json.items():
            if key != 'ifc_class':   

                if isinstance(value, list) :
                    l = []
                    for item in value:
                        ent2 = self.make_entity(model, item)
                        l.append(ent2)
                        setattr(ent, key, l)

                elif isinstance(value, dict) :
                    ent2 = self.make_entity(model, value)
                    setattr(ent, key, ent2)
                else:
                    setattr(ent, key, value)
        model.end_transaction
        return ent



    def execute(self, context):              
        props = context.scene.my_props       
        obj = context.active_object        
        model = tool.Ifc.get()
        cat = Catalog()
        cat.get_types()

        if 'entity' in cat.types:

            lt = [f'{x.is_a()}{x.Name}' for x in model.by_type('IfcTypeProduct')]
            if not cat.types['entity']['ifc_class']+cat.types['entity']['Name'] in lt:

                ent = self.make_entity(model, cat.types['entity'])
                
                if 'material' in cat.types:
                    mat = self.make_entity(model, cat.types['material'])
                    print(mat)
                    material.assign_material(model, products=[ent], type=mat.is_a(), material=mat)
                if 'geometry' in cat.types:
                    geo = self.make_entity(model, cat.types['geometry'])
                    geometry.assign_representation(model, product=ent, representation=geo)

                print('Done!')
                self.report({'OPERATOR'}, 'Done!')

            else:
                print('The type already exists!')
                self.report({'ERROR'}, 'The type already exists!')
        else:
            print('No entities was created')
            self.report({'ERROR'}, 'No entities was created!')

        return {"FINISHED"} 
