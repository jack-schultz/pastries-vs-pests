from entities.living.pests.ants.ant import Ant


def test_is_an_unarmoured_ant(canvas):
    ant = Ant(canvas, 100, 100)
    assert ant.armour is None and ant.health == 160
