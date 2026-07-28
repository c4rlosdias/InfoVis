import os
import json
import logging

import bpy
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.selector as selector
from bonsai.bim import import_ifc

from .bsdd import bSDD
from .ifc_session import (
    get_bonsai_data_dir_path,
    get_model,
    get_object_by_identifier,
    get_path,
)


class Import_ifc():

    file : ifcopenshell.file

    @classmethod
    def import_type_from_ifc(self, element: ifcopenshell.entity_instance, context: bpy.types.Context) -> None:
        self.file = get_model()
        logger = logging.getLogger("ImportIFC")
        ifc_import_settings = import_ifc.IfcImportSettings.factory(context, get_path(), logger)

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
            if get_object_by_identifier(material.id()):
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
                    if element2.is_a("IfcSurfaceStyle") and not get_object_by_identifier(element2.id()):
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
            if element.is_a("IfcSurfaceStyle") and not get_object_by_identifier(element.id()):
                ifc_importer.create_style(element)


class Catalog:
    
    @classmethod
    def get_ifc_type(cls):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'resources', 'ifc_types.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data


class PropTempl:
    template = None
    filepath = None
    # Obtem o arquivo template de propriedades
    @classmethod
    def get_template(cls):   
        cls.filepath = (get_bonsai_data_dir_path("pset") / "EPset_OG.ifc").__str__()
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
        # Ensure the template file exists; create one if needed.
        if cls.template is None:
            cls.get_template()

        # Load value types by unit.
        units_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'resources', 'units.json')
        with open(units_path, 'r') as file:
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

        # Select the correct data type.
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

        # If the property has allowed values, create an enumerated property.
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

        # Create the property for each class according to the Pset.
        for classe in metadata['propertyClasses']:
            pset_name = classe['propertySet']
            object_type = classe['code']

            # Check which IFC class the Pset should apply to.
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

            # If the Pset already exists in the file, edit it.
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
                # Otherwise, create the Pset.
                pset_templ = ifcopenshell.api.pset_template.add_pset_template(
                    cls.template,
                    name=pset_name,
                    applicable_entity= aplicable_entity
                )

            # If the property exists in that Pset, edit it.
            prop_templ = cls.get_prop(prop_name, pset_name, cls.template)
            if prop_templ is not None:
                prop_templ.Description=description
                prop_templ.PrimaryMeasureType=data_type
                prop_templ.TemplateType=template_type
                prop_templ.Enumerators=enumerators
            

            else:
                # Otherwise, create the property.
                property_template = ifcopenshell.api.pset_template.add_prop_template(
                    cls.template,
                    description=definition,
                    pset_template=pset_templ,
                    name=prop_name,
                    primary_measure_type = data_type,
                    template_type = template_type,                    
                )
                property_template.Enumerators=enumerators            
        # Write the template.
        
        if cls.filepath is not None:
            cls.template.write(cls.filepath)
            return True
        else:
            return False
