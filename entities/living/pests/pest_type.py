from __future__ import annotations
from enum import Enum
from entities.living.pests.base_pest import BasePest
from entities.living.pests.ants.ant import Ant
from entities.living.pests.ants.armour_ant import ArmourAnt
from entities.living.pests.ants.heavy_armour_ant import HeavyArmourAnt
from entities.living.pests.weevils.weevil import Weevil
from entities.living.pests.weevils.chainmail_weevil import ChainmailWeevil
from entities.living.pests.weevils.helmet_weevil import HelmetWeevil
from entities.living.pests.weevils.shield_weevil import ShieldWeevil


# Every kind of pest a level can spawn. Level data uses these as wave keys,
# for example {PestType.ANT: 3} spawns three ants
class PestType(Enum):
    ANT = Ant
    ARMOUR_ANT = ArmourAnt
    HEAVY_ARMOUR_ANT = HeavyArmourAnt
    WEEVIL = Weevil  # leaps over the first good
    CHAINMAIL_WEEVIL = ChainmailWeevil  # Borer: bites harder the longer it chews
    HELMET_WEEVIL = HelmetWeevil  # Rammer: charges in for one big headbutt
    SHIELD_WEEVIL = ShieldWeevil  # Basher: stuns the goods it hits
