import pytest
from entities.living.pests.base_pest import BasePest
from entities.living.pests.ants.ant import Ant
from entities.living.pests.pest_type import PestType


def test_ant_type_spawns_ants():
    assert PestType.ANT.value is Ant


@pytest.mark.parametrize("pest_type", list(PestType))
def test_every_type_is_a_pest_class(pest_type):
    assert issubclass(pest_type.value, BasePest)
