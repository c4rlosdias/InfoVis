import importlib.util
from collections import namedtuple
from pathlib import Path


_MODULE_PATH = Path(__file__).parents[1] / "data" / "li_materials.py"
_SPEC = importlib.util.spec_from_file_location("li_materials", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
resolve_material_information = _MODULE.resolve_material_information


class Entity:
    def __init__(self, entity_id, **attributes):
        self._entity_id = entity_id
        for name, value in attributes.items():
            setattr(self, name, value)

    def id(self):
        return self._entity_id


class FakeElementUtil:
    def __init__(self, materials=None, layers=None, psets=None):
        self.materials = materials or {}
        self.layers = layers or {}
        self.psets = psets or {}

    def get_materials(self, entity, should_inherit=False):
        assert should_inherit is False
        return self.materials.get(entity.id(), [])

    def get_material_layers(self, entity):
        return self.layers.get(entity.id(), [])

    def get_pset(self, material, pset_name):
        return self.psets.get((material.id(), pset_name))


def test_material_names_prefer_occurrence_and_include_type_without_duplicates():
    occurrence = Entity(1)
    type_entity = Entity(2)
    steel = Entity(10, Name="Steel", Category="Metal")
    coating = Entity(11, Name="FBE", Category="Coating")
    util = FakeElementUtil({1: [steel], 2: [steel, coating]})

    value = resolve_material_information(
        type_entity, occurrence, {"material_field": "name"}, util
    )

    assert value == "Steel; FBE"


def test_material_composition_includes_category():
    occurrence = Entity(1)
    steel = Entity(10, Name="Steel", Category="Metal")
    util = FakeElementUtil({1: [steel]})

    value = resolve_material_information(
        None, occurrence, {"material_field": "composition"}, util
    )

    assert value == "Steel (Metal)"


def test_material_property_reads_material_pset():
    occurrence = Entity(1)
    steel = Entity(10, Name="Steel")
    util = FakeElementUtil(
        {1: [steel]},
        psets={(10, "Pset_MaterialCommon"): {"Grade": "X65"}},
    )

    value = resolve_material_information(
        None,
        occurrence,
        {
            "material_field": "property",
            "pset": "Pset_MaterialCommon",
            "property": "Grade",
        },
        util,
    )

    assert value == "X65"


def test_material_layers_include_thickness():
    occurrence = Entity(1)
    coating = Entity(10, Name="Coating")
    layer = namedtuple("Layer", "priority material thickness")(0, coating, 3.5)
    util = FakeElementUtil(layers={1: [layer]})

    value = resolve_material_information(
        None, occurrence, {"material_field": "layer_thickness"}, util
    )

    assert value == "Coating: 3.5"
