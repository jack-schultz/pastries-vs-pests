from armour.helmet import Helmet
from entities.damage import Damage
from entities.direction import Direction


def test_blocks_hits_from_above():
    helmet = Helmet()
    assert helmet.absorb(Damage(100, direction=Direction.ABOVE)) == 0
    assert helmet.durability == 150


def test_ignores_hits_from_the_front():
    helmet = Helmet()
    assert helmet.absorb(Damage(100, direction=Direction.LEFT)) == 100
    assert helmet.durability == 250
