from armour.base_armour import BaseArmour
from armour.chainmail import Chainmail
from entities.damage import Damage
from entities.living.pests.ants.ant import Ant
from entities.living.pests.ants.armour_ant import ArmourAnt


def test_armour_defaults_to_one_layer():
    assert BaseArmour(durability=100).layer_count == 1
    assert Chainmail().layer_count == 1


def test_armour_layer_count_can_be_set():
    assert BaseArmour(durability=100, layer_count=3).layer_count == 3


def test_unarmoured_pest_has_one_layer(canvas):
    assert Ant(canvas, 800, 100).layer_count == 1


def test_armour_adds_its_layers_to_the_pest(canvas):
    assert ArmourAnt(canvas, 800, 100).layer_count == 2
    thick = Ant(canvas, 800, 100, armour=BaseArmour(
        durability=100, layer_count=3))
    assert thick.layer_count == 4


def test_broken_armour_adds_no_layers(canvas):
    ant = Ant(canvas, 800, 100, armour=BaseArmour(durability=10))
    ant.take_damage(Damage(50))
    assert ant.armour.is_broken
    assert ant.layer_count == 1
