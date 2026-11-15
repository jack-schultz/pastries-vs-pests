from armour.platemail import Platemail
from entities.living.pests.ants.heavy_armour_ant import HeavyArmourAnt


def test_wears_platemail(canvas):
    assert isinstance(HeavyArmourAnt(canvas, 100, 100).armour, Platemail)
