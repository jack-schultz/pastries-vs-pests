import pytest
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.pests.ants.ant import Ant
from entities.projectiles.sugar_cube import SugarCube


@pytest.fixture
def shooter(canvas):
    return SugarShooter(canvas, 100, 100)


def test_holds_fire_without_a_pest_in_its_lane(shooter, canvas, fast_forward):
    fast_forward()
    assert shooter.act(canvas, [Ant(canvas, 300, 400)]) is None


def test_fires_a_sugar_cube_at_a_pest_in_its_lane(shooter, canvas, fast_forward):
    fast_forward()
    assert isinstance(shooter.act(canvas, [Ant(canvas, 300, 100)]), SugarCube)
