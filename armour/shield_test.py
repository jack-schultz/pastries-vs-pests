from armour.shield import Shield
from entities.damage import Damage
from entities.direction import Direction


def test_blocks_hits_from_the_front_until_it_breaks():
    shield = Shield()
    assert shield.absorb(Damage(500)) == 0
    assert shield.is_broken
    assert shield.absorb(Damage(100)) == 100


def test_ignores_hits_from_behind():
    shield = Shield()
    assert shield.absorb(Damage(100, direction=Direction.RIGHT)) == 100
    assert shield.durability == 500
