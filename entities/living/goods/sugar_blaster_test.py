import pytest
from entities.living.goods.sugar_blaster import SugarBlaster
from entities.living.goods.sugar_shooter import SugarShooter


@pytest.fixture
def blaster(canvas):
    return SugarBlaster(canvas, 100, 100)


def test_is_a_shooter_that_fires_faster(blaster, canvas):
    assert isinstance(
        blaster, SugarShooter) and blaster.delay_pattern == (1.4, 0.25)
