from armour.platemail import Platemail
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction


def test_has_two_layers():
    assert Platemail().layer_count == 2


def test_blocks_three_quarters_of_an_explosion():
    platemail = Platemail()
    assert platemail.absorb(Damage(100, DamageType.EXPLOSIVE, Direction.AMBIENT)) == 25
    assert platemail.durability == 350
