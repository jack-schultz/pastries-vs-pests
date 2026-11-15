import pytest
from entities.living.living import Living


@pytest.fixture
def living(canvas):
    return Living(canvas, 0, 0, 10, 10, "#ffffff", 100)


def test_damage_lowers_health_and_can_kill(living):
    living.take_damage(30)
    assert living.health == 70 and not living.is_dead
    living.take_damage(70)
    assert living.is_dead


def test_changing_max_health_keeps_the_fraction(living):
    living.take_damage(50)
    living.max_health = 200
    assert living.health == 100
