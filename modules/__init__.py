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
from .analysis import operators as _analysis_ops
from .analysis import panels as _analysis_panels
from .analysis import properties as _analysis_props
from .types import panels as _types_panels
from .connections import operators as _conn_ops
from .connections import panels as _conn_panels
from .props import operators as _props_ops
from .props import panels as _props_panels
from .props import properties as _props_props
from .settings import panels as _settings_panels
from .settings import operators as _settings_ops
from .og_properties import (
    OG_Properties,
    IFC_Label_Attribute,
    Decomposition_View,
    Decomposition_View_Relation,
)


def get_classes():
    """Return all Blender classes in correct registration order."""
    return [
        # --- Common ---
        _common_ops.Operator_expand_tree,
        _common_ops.Operator_contract_tree,
        _common_ops.Select_object,
        _common_ops.Columns,
        _common_ops.ErrorMessage,
        _common_ops.Operator_common_set_tree_expansion,
        # --- PropertyGroups (must register before OG_Properties) ---
        _dict_props.Ifc_properties,
        _dict_props.Class_info,
        _dict_props.Class_prop_info,
        _cat_props.Class_type,
        _cat_props.Layer,        
        _cat_props.LIMappingSourceItem,
        _cat_props.LISupportTableRow,
        _cat_props.LISupportTable,
        _cat_props.LIMappingColumn,
        _props_props.Enumeration_values,
        _props_props.Documents,
        _props_props.Property_info,
        _props_props.Pset_info,
        _decomp_props.Container,
        _analysis_props.AnalysisLegendItem,
        IFC_Label_Attribute,
        Decomposition_View_Relation,
        Decomposition_View,
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
        _decomp_ops.Operator_decomposition_export,        
        _decomp_ops.Operator_decomposition_select_element,
        _decomp_ops.Operator_decomposition_select_components,
        _decomp_panels.Panel_Decompositions,
        _decomp_panels.BIM_UL_decomposition,
        _decomp_panels.BIM_UL_tree,
        # --- Catalog ---
        _cat_ops.Operator_load_products,
        _cat_ops.Operator_catalog_show_layers,
        _cat_ops.Operator_catalog_select_layer,
        _cat_ops.Operator_catalog_select_elements,
        _cat_ops.Operator_load_li_mapping,
        _cat_ops.Operator_save_li_mapping,
        _cat_ops.Operator_add_li_mapping_column,
        _cat_ops.Operator_remove_li_mapping_column,
        _cat_ops.Operator_move_li_mapping_column,
        _cat_ops.Operator_li_mapping_pick_property,
        _cat_ops.Operator_add_li_mapping_source_item,
        _cat_ops.Operator_remove_li_mapping_source_item,
        _cat_ops.Operator_add_li_support_table_row,
        _cat_ops.Operator_remove_li_support_table_row,
        _cat_ops.Operator_export_li,
        _cat_ops.Operator_export_qtds,
        _cat_panels.Panel_Catalog,
        _cat_panels.Panel_LI_Mapping,
        _cat_panels.BIM_UL_products,
        _cat_panels.BIM_UL_li_mapping_columns,
        _cat_panels.BIM_UL_li_mapping_source_items,
        _cat_panels.BIM_UL_li_support_tables,
        _cat_panels.BIM_UL_li_support_table_rows,
        _cat_panels.BIM_UL_layers,
        # --- Analysis ---
        _analysis_ops.Operator_analysis_apply_colors,
        _analysis_ops.Operator_analysis_reset_colors,
        _analysis_panels.Panel_Analysis,
        # --- Connections ---
        _conn_ops.Operator_disconnect,
        _conn_panels.Panel_Connect_Elements,
        # --- Properties ---
        _props_ops.Operator_props_load,
        _props_ops.Operator_props_expand,
        _props_ops.Operator_property_definition,
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
        _settings_ops.Operator_add_ifc_label_attr,
        _settings_ops.Operator_add_ifc_label_property,
        _settings_ops.Operator_remove_ifc_label_attr,
        _settings_ops.Operator_load_decomposition_views,
        _settings_ops.Operator_save_decomposition_views,
        _settings_ops.Operator_reset_decomposition_views,
        _settings_ops.Operator_add_decomposition_view,
        _settings_ops.Operator_duplicate_decomposition_view,
        _settings_ops.Operator_remove_decomposition_view,
        _settings_ops.Operator_add_decomposition_relation,
        _settings_ops.Operator_remove_decomposition_relation,
        _settings_ops.Operator_export_config_profile,
        _settings_ops.Operator_import_config_profile,
        _settings_panels.BIM_UL_ifc_label_attrs,
        _settings_panels.BIM_UL_decomposition_views,
        _settings_panels.BIM_UL_decomposition_view_relations,
        _settings_panels.Panel_Settings,
    ]
