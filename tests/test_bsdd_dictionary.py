import importlib.util
from pathlib import Path


_MODULE_PATH = Path(__file__).parents[1] / "data" / "bsdd_dictionary.py"
_SPEC = importlib.util.spec_from_file_location("bsdd_dictionary", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
get_property_json_description = _MODULE.get_property_json_description
get_property_json_definition = _MODULE.get_property_json_definition


def test_property_description_comes_from_json_for_exact_object_type():
    description = get_property_json_description(
        "AnchoringCollar",
        "OGSubPset_LineComponentOccurrence",
        "IsSpare",
    )

    assert description == "Is Spare"


def test_property_description_accepts_ifc_occurrence_typo():
    description = get_property_json_description(
        "AnchoringCollar",
        "OGSubPset_LineComponentOccurence",
        "IsSpare",
    )

    assert description == "Is Spare"


def test_property_definition_comes_from_json():
    definition = get_property_json_definition(
        "AnchoringCollar",
        "OGSubPset_LineComponentOccurrence",
        "IsSpare",
    )

    assert definition == "Indicates whether the item is spare (TRUE) or not (FALSE)."


def test_property_description_returns_none_for_unknown_property():
    description = get_property_json_description(
        "AnchoringCollar",
        "OGSubPset_LineComponentOccurrence",
        "PropertyThatDoesNotExist",
    )

    assert description is None
