import json
import os

from . import decomposition_views


PROFILE_TYPE = "infovis_config_profile"
PROFILE_SCHEMA_VERSION = "1.0"
PROFILE_FILENAME = "infovis_config_profile.json"


def get_resources_dir():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "resources")
    )


def get_li_mapping_path():
    return os.path.join(get_resources_dir(), "li_mapping.json")


def ensure_json_suffix(filepath):
    if not filepath:
        return filepath
    return filepath if filepath.lower().endswith(".json") else f"{filepath}.json"


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filepath, payload):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


def load_decomposition_payload():
    return decomposition_views.normalize_payload(
        load_json(decomposition_views.get_config_path())
    )


def load_li_mapping_payload():
    return load_json(get_li_mapping_path())


def save_li_mapping_payload(payload):
    save_json(get_li_mapping_path(), payload)


def label_settings_from_props(props):
    return {
        "show_ifc_label": bool(getattr(props, "show_ifc_label", True)),
        "offset": {
            "x": float(getattr(props, "label_offset_x", 80.0)),
            "y": float(getattr(props, "label_offset_y", 80.0)),
        },
        "attributes": [
            {
                "attr_name": item.attr_name,
                "display_name": item.display_name,
            }
            for item in getattr(props, "ifc_label_attributes", [])
            if item.attr_name
        ],
    }


def apply_label_settings_to_props(props, settings):
    if not isinstance(settings, dict):
        return

    if "show_ifc_label" in settings:
        props.show_ifc_label = bool(settings["show_ifc_label"])

    offset = settings.get("offset", {})
    if isinstance(offset, dict):
        if "x" in offset:
            props.label_offset_x = float(offset["x"])
        if "y" in offset:
            props.label_offset_y = float(offset["y"])

    attributes = settings.get("attributes")
    if isinstance(attributes, list):
        props.ifc_label_attributes.clear()
        for item_data in attributes:
            if not isinstance(item_data, dict):
                continue
            attr_name = str(item_data.get("attr_name", "")).strip()
            if not attr_name:
                continue
            item = props.ifc_label_attributes.add()
            item.attr_name = attr_name
            item.display_name = str(item_data.get("display_name", "")).strip()
        props.active_ifc_label_attr_index = 0 if props.ifc_label_attributes else -1


def preferences_from_addon_preferences(preferences):
    if preferences is None:
        return {}
    return {
        "cde_url": getattr(preferences, "cde_url", ""),
        "debug_mode": bool(getattr(preferences, "debug_mode", False)),
    }


def apply_preferences_to_addon_preferences(preferences, preferences_data):
    if preferences is None or not isinstance(preferences_data, dict):
        return
    if "cde_url" in preferences_data:
        preferences.cde_url = str(preferences_data["cde_url"])
    if "debug_mode" in preferences_data:
        preferences.debug_mode = bool(preferences_data["debug_mode"])


def build_profile(
    props=None,
    preferences=None,
    addon_version="",
    decomposition_payload=None,
    li_mapping_payload=None,
):
    if decomposition_payload is None:
        decomposition_payload = load_decomposition_payload()
    if li_mapping_payload is None:
        li_mapping_payload = load_li_mapping_payload()

    return {
        "profile_type": PROFILE_TYPE,
        "schema_version": PROFILE_SCHEMA_VERSION,
        "addon": "InfoVis",
        "addon_version": addon_version,
        "label_settings": label_settings_from_props(props) if props is not None else {},
        "preferences": preferences_from_addon_preferences(preferences),
        "decomposition_views": decomposition_views.normalize_payload(decomposition_payload),
        "li_mapping": li_mapping_payload,
    }


def validate_li_mapping_payload(payload):
    errors = []
    if not isinstance(payload, dict):
        return ["LI mapping must be a JSON object."]

    columns = payload.get("columns")
    if columns is not None and not isinstance(columns, list):
        errors.append("LI mapping 'columns' must be a list.")

    if isinstance(columns, list):
        for index, column in enumerate(columns, start=1):
            if not isinstance(column, dict):
                errors.append(f"LI mapping column {index} must be an object.")

    return errors


def validate_profile(profile):
    errors = []
    if not isinstance(profile, dict):
        return ["Config profile must be a JSON object."]

    profile_type = profile.get("profile_type")
    if profile_type and profile_type != PROFILE_TYPE:
        errors.append(f"Unsupported config profile type: {profile_type}")

    decomposition_payload = profile.get("decomposition_views")
    if decomposition_payload is not None:
        errors.extend(decomposition_views.validate_payload(decomposition_payload))

    li_mapping_payload = profile.get("li_mapping")
    if li_mapping_payload is not None:
        errors.extend(validate_li_mapping_payload(li_mapping_payload))

    return errors
