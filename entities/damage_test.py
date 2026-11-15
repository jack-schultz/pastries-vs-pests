import pytest
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction


def test_defaults_to_bludgeoning_from_the_left():
    damage = Damage(10)
    assert (damage.amount, damage.type, damage.direction) == (10, DamageType.BLUDGEONING, Direction.LEFT)


def test_keeps_given_type_and_direction():
    damage = Damage(5, DamageType.FIRE, Direction.AMBIENT)
    assert (damage.type, damage.direction) == (DamageType.FIRE, Direction.AMBIENT)


def test_negative_damage_is_rejected():
    with pytest.raises(ValueError):
        Damage(-1)
