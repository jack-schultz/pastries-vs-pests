import pytest
from entities.living.goods.oven_toaster import OvenToaster
from entities.living.pests.ants.ant import Ant
from entities.projectiles.flame import Flame


@pytest.fixture
def toaster(canvas):
    return OvenToaster(canvas, 100, 100)


def test_holds_fire_when_no_pest_is_in_range(toaster, canvas, fast_forward):
    fast_forward()
    assert toaster.act(canvas, [Ant(canvas, 800, 100)]) is None


def test_breathes_a_flame_at_a_pest_in_range(toaster, canvas, fast_forward):
    fast_forward()
    assert isinstance(toaster.act(canvas, [Ant(canvas, 250, 100)]), Flame)
