from armour.chainmail import Chainmail
from entities.living.pests.ants.armour_ant import ArmourAnt


def test_wears_chainmail(canvas):
    assert isinstance(ArmourAnt(canvas, 100, 100).armour, Chainmail)
