import pytest
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.pests.ants.ant import Ant


@pytest.fixture
def candy(canvas):
    return PoppingCandy(canvas, 100, 100)


def test_arms_only_after_its_arming_time(candy, fast_forward):
    assert not candy.is_armed
    fast_forward()
    assert candy.is_armed


def test_detonating_kills_a_pest_in_its_row_and_uses_the_candy_up(candy, canvas):
    pest = Ant(canvas, 130, 100)
    assert candy.detonate([pest]) == [pest]
    assert pest.is_dead and candy.is_dead
