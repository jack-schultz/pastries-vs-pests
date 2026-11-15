import pytest
from entities.living.goods.profiterole import Profiterole
from entities.living.pests.ants.ant import Ant


@pytest.fixture
def profiterole(canvas):
    return Profiterole(canvas, 100, 100)


def test_is_primed_only_after_its_fuse(profiterole, fast_forward):
    assert not profiterole.is_primed
    fast_forward()
    assert profiterole.is_primed


def test_detonating_hits_nearby_pests_only(profiterole, canvas):
    near, far = Ant(canvas, 150, 150), Ant(canvas, 700, 100)
    assert profiterole.detonate([near, far]) == [near]
    assert near.is_dead and not far.is_dead
