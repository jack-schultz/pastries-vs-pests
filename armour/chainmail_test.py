from armour.chainmail import Chainmail
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction


def test_blocks_physical_hits_from_every_side():
    chainmail = Chainmail()
    assert chainmail.absorb(Damage(100, direction=Direction.RIGHT)) == 0
    assert chainmail.durability == 250


def test_blocks_no_fire():
    assert Chainmail().absorb(Damage(100, DamageType.FIRE)) == 100
