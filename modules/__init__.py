from .common import operators as _common_ops
from .decomposition import operators as _decomp_ops
from .decomposition import panels as _decomp_panels
from .decomposition import properties as _decomp_props
from .dictionary import operators as _dict_ops
from .dictionary import panels as _dict_panels
from .dictionary import properties as _dict_props
from .catalog import operators as _cat_ops
from .catalog import panels as _cat_panels
from .catalog import properties as _cat_props
from .types import panels as _types_panels
from .connections import operators as _conn_ops
from .connections import panels as _conn_panels
from .props import operators as _props_ops
from .props import panels as _props_panels
from .props import properties as _props_props
from .settings import panels as _settings_panels
from .og_properties import OG_Properties


def get_classes():
    """Return all Blender classes in correct registration order."""
    return [
        # --- Common ---
        _common_ops.Operator_expand_tree,
        _common_ops.Operator_contract_tree,
        _common_ops.Select_object,
        _common_ops.Columns,
        _common_ops.ErrorMessage,
        # --- PropertyGroups (must register before OG_Properties) ---
        _dict_props.Ifc_properties,
        _dict_props.Class_info,
        _dict_props.Class_prop_info,
        _cat_props.Class_type,
        _cat_props.Layer,
        _props_props.Enumeration_values,
        _props_props.Documents,
        _props_props.Property_info,
        _props_props.Pset_info,
        _decomp_props.Container,
        # --- OG_Properties (central property bag) ---
        OG_Properties,
        # --- Dictionary ---
        _dict_ops.Operator_get_properties,
        _dict_ops.Operator_get_classes,
        _dict_ops.Operator_add_properties,
        _dict_ops.Operator_clear_properties,
        _dict_ops.Operator_assign_all,
        _dict_ops.Operator_unassign_all,
        _dict_ops.Operator_uri,
        _dict_ops.Operator_get_prop_info,
        _dict_ops.Operator_get_class_info,
        _dict_ops.Operator_get_class_prop,
        _dict_ops.Operator_export_ids,
        _dict_panels.Panel_Connect,
        _dict_panels.BIM_UL_ifc_properties,
        _dict_panels.BIM_UL_property_class,
        _dict_panels.BIM_UL_classes,
        _dict_panels.BIM_UL_class_prop,
        # --- Decomposition ---
        _decomp_ops.Operator_decomposition_load,
        _decomp_ops.Operator_decomposition_select_element,
        _decomp_ops.Operator_decomposition_select_components,
        _decomp_ops.Operator_decomposition_move,
        _decomp_ops.Operator_decomposition_chg_order,
        _decomp_panels.Panel_Decompositions,
        _decomp_panels.BIM_UL_decomposition,
        _decomp_panels.BIM_UL_tree,
        # --- Catalog ---
        _cat_ops.Operator_load_products,
        _cat_ops.Operator_catalog_show_layers,
        _cat_ops.Operator_catalog_select_layer,
        _cat_ops.Operator_catalog_select_elements,
        _cat_panels.Panel_Catalog,
        _cat_panels.BIM_UL_products,
        _cat_panels.BIM_UL_layers,
        # --- Connections ---
        _conn_ops.Operator_disconnect,
        _conn_ops.Operator_select_object,
        _conn_ops.Operator_add_connect,
        _conn_panels.Panel_Connect_Elements,
        # --- Properties ---
        _props_ops.Operator_props_edit,
        _props_ops.Operator_props_load,
        _props_ops.Operator_props_expand,
        _props_ops.Operator_docs_expand,
        _props_ops.Operator_props_graph,
        _props_ops.Operator_props_invert,
        _props_ops.Operator_document_edit,
        _props_ops.Operator_document_load,
        _props_ops.Operator_document_open,
        _props_ops.Operator_show_table,
        _props_panels.Panel_Properties,
        #- --- Types ---
        _types_panels.Panel_Types,
        # --- Settings ---        
        _settings_panels.Panel_Info,
    ]
