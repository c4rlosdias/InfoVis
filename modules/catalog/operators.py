import bpy
import os
import json
import ifcopenshell.util.element as element
import ifcopenshell
from pathlib import Path

import bonsai.tool as tool

from ...data.catalog import Catalog
from ...data.ifc_utils import build_products
from ...data.tree import refresh_types
from ..common.operators import _open_in_browser


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
            'tag': '',
            'description' : '',
            'element_type': '',
            'id' : 0
        }

        for type in types:
            dic = {}   
            dic['id'] = type.id()         
            dic['name'] = type.Name or  ''
            dic['tag'] = type.Tag or  ''
            dic['description'] = type.Description or ''
            dic['element_type'] = type.ElementType or ''

            if type.ElementType not in result:
                result[type.ElementType] = []
            result[type.ElementType].append(dic)
        
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

class Operator_catalog_show_layers(bpy.types.Operator):
    """"""
    bl_idname  = "catag.show_layers"
    bl_label   = "show layers of the type"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

    def _build_html(self, type_name, type_props, nested_elements):
        import html as html_mod
        props_rows = "<tr><td>No properties found</td><td></td></tr>"
        for pset_name, pset_values in type_props.items():
            for prop, value in pset_values.items():
                props_rows += f"<tr><td>{html_mod.escape(str(prop))}</td><td>{html_mod.escape(str(value))}</td></tr>\n"

        all_columns = []
        columns_set = set()
        layers_data = []

        for nest in nested_elements:
            nest_name = getattr(nest, 'Name', '') or ''
            obj_type = getattr(nest, 'ObjectType', '') or ''
            label = f"{nest_name} [{obj_type}]" if obj_type else nest_name
            nest_psets = ifcopenshell.util.element.get_psets(nest)

            values = {}
            for pset_name, pset_values in nest_psets.items():
                for prop, value in pset_values.items():
                    if prop == 'id':
                        continue
                    key = (pset_name, prop)
                    values[key] = value
                    if key not in columns_set:
                        columns_set.add(key)
                        all_columns.append(key)

            layers_data.append({"label": label, "values": values})

        header_cells = "<th>Layer</th>"
        for pset, prop in all_columns:
            header_cells += f"<th>{html_mod.escape(prop)}<br><small>{html_mod.escape(pset)}</small></th>"

        layer_rows = ""
        for layer in layers_data:
            cells = f"<td><strong>{html_mod.escape(layer['label'])}</strong></td>"
            for key in all_columns:
                val = layer["values"].get(key, "")
                cells += f"<td>{html_mod.escape(str(val))}</td>"
            layer_rows += f"<tr>{cells}</tr>\n"

        report = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>{html_mod.escape(type_name)} - Layers</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
                h2 {{ color: #569cd6; }}
                h3 {{ color: #9cdcfe; margin-top: 24px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #3c3c3c; padding: 8px 12px; text-align: left; white-space: nowrap; }}
                th {{ background: #264f78; color: #ffffff; }}
                th small {{ color: #9cdcfe; font-weight: normal; }}
                tr:nth-child(even) {{ background: #2d2d2d; }}
                tr:hover {{ background: #37373d; }}
                .table-wrapper {{ overflow-x: auto; }}
            </style>
            </head>
            <body>
            <h2>{html_mod.escape(type_name)}</h2>

            <h3>Pipe Structure Properties</h3>
            <table>
                <tr><th>Property</th><th>Value</th></tr>
                {props_rows}
            </table>"""

        layers = f"""<h3>Layers</h3>
            <div class="table-wrapper">
            <table>
                <tr>{header_cells}</tr>
                {layer_rows}
            </table>
            </div>

            </body>
            </html>"""
        
        if len(layers_data) > 0:
            report += layers

        return report
    
    def execute(self, context):                             
        return {"FINISHED"}

    def invoke(self, context, event):
        model = tool.Ifc.get()        
        ifc_type = model.by_id(self.id)   

        if ifc_type is not None:                
            type_name = ifc_type.Name or str(self.id)
            type_props = ifcopenshell.util.element.get_psets(ifc_type, psets_only=True)
            nested_elements = ifcopenshell.util.element.get_components(ifc_type) or []
            print(nested_elements)

            html = self._build_html(type_name, type_props, nested_elements)
            html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "layers.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            _open_in_browser(Path(html_path).as_uri())

            self.report({'INFO'}, "Layers opened in browser")
            return {"FINISHED"}
        else:
            self.report({'ERROR'}, f"No type found for id {self.id}")
            return {"CANCELLED"}

class Operator_catalog_select_layer(bpy.types.Operator):
    """"""
    bl_idname  = "catag.select_layer"
    bl_label   = "select elements of the layer"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

            
    def execute(self, context): 
            props = context.scene.og_props                     
            model = tool.Ifc.get()        
            layer = model.by_id(self.id)           

            obj_blender = tool.Ifc.get_object(layer)
            if obj_blender:
                obj_blender.select_set(True)
                context.view_layer.objects.active = obj_blender

                self.report({'OPERATOR'}, 'Done!')
                return {"FINISHED"}    
            else:
                self.report({'ERROR'}, f"No layer found for id {self.id}")
                return {"CANCELLED"}        

class Operator_catalog_select_elements(bpy.types.Operator):
    """"""
    bl_idname  = "catag.select_elements"
    bl_label   = "select elements of the type"
    bl_options = {"REGISTER", "UNDO"}  

    id : bpy.props.IntProperty(name="id")

            
    def execute(self, context): 
            props = context.scene.og_props                     
            model = tool.Ifc.get()        
            type = model.by_id(self.id)           
            elements=[]
            if type is not None:
                if getattr(type, "Types", None):
                    rels = [e for e in type.Types]                    
                    for rel in rels:
                        elements.extend(rel.RelatedObjects)

                for element in elements:
                    obj_blender = tool.Ifc.get_object(element)
                    if obj_blender:
                        obj_blender.select_set(True)
                        context.view_layer.objects.active = obj_blender

                self.report({'OPERATOR'}, 'Done!')
                return {"FINISHED"}    
            else:
                self.report({'ERROR'}, f"No type found for id {self.id}")
                return {"CANCELLED"}
            
def update_predefined_types():
    model = tool.Ifc.get()
    for entity in model.by_type('IfcElement'):
        if entity.IsTypedBy:
            type = entity.IsTypedBy[0].RelatingType
            if type.ElementType:
                object_type = type.ElementType.replace("Type", "")
                entity.ObjectType = object_type
                entity.PredefinedType = None
