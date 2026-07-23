import bpy
import os
import base64
from io import BytesIO
from pathlib import Path

import ifcopenshell.util.element as element
import bonsai.tool as tool
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from scipy.interpolate import interp1d

from ...data.ifc_utils import get_prop_type, refresh_props
from ..common.operators import _open_in_browser, get_options, dynamic_items, Columns


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
    interpoled : bpy.props.BoolProperty(name='Interpolated Curve')
    columns    : bpy.props.CollectionProperty(name='columns', type=Columns)
    intpl_type : bpy.props.EnumProperty(
        items=[
            ('cubic','cubic','cubic'),
            ('linear', 'linear', 'linear')
        ],
        name='type',
        description='Get interpolation type'
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
        
        # If an attached document exists.
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

        # Build a dictionary with properties and values.
        props = context.scene.og_props
        # If the document is associated with a property.
        if self.pset_index > -1:
            for pset in props.prop_metadata:            
                if pset.index == self.pset_index:    
                    # If it is not an external document.
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
            # Build the dataframe.
            if self.prop_index == -1:
                if os.path.exists(self.csv): 
                    self.df = pd.read_csv(self.csv) 
                else:
                    self.report({'ERROR'}, 'FILE NOT FOUND!')
                    return {"CANCELLED"}
            else:
                self.df = pd.DataFrame(self.table)

        # If the document is associated with the element.
        else:
            if os.path.exists(self.document): 
                self.df = pd.read_csv(self.document)
            else:
                self.report({'ERROR'}, 'FILE NOT FOUND!')
                return {"CANCELLED"}


        # Populate column options for the X axis.
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
        # Create the Matplotlib chart.
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
      
        # Configure the chart.
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

        # Save the image in memory.
        buffer = BytesIO()        
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Create HTML with the embedded image.
        html = f"""
        <html>
        <head><title>BIM Report</title></head>
        <body>
        <h2>{self.title}</h2>
        <img src="data:image/png;base64,{img_base64}" />
        </body>
        </html>
        """

        # Save the HTML and open it in the browser.
        html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "graphic.html")
        with open(html_path, "w") as f:
            f.write(html)
        _open_in_browser(Path(html_path).as_uri())
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
            doc.Location = self.location

        return {"FINISHED"}
    

class Operator_document_load(bpy.types.Operator):
    """"""
    bl_idname  = "props.load_doc"
    bl_label   = "load reference document"
    bl_options = {"REGISTER", "UNDO"} 
    filepath   : bpy.props.StringProperty(subtype='FILE_PATH')
    index      : bpy.props.IntProperty(name='index')
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
        location = self.location.strip()
        if not location:
            self.report({'ERROR'}, 'Location is empty!')
            return {"CANCELLED"}
        try:
            # If it is a URL, open it in the browser.
            if location.startswith(('http://', 'https://', 'ftp://')):
                _open_in_browser(location)
                return {"FINISHED"}
            # If it is a local file.
            abs_path = os.path.abspath(os.path.normpath(location))
            if os.path.exists(abs_path):
                _open_in_browser(Path(abs_path).as_uri())
                return {"FINISHED"}
            else:
                self.report({'ERROR'}, f'FILE NOT FOUND: {abs_path}')
                return {"CANCELLED"}
        except OSError as e:
            self.report({'ERROR'}, f'Failed to open: {e}')
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
