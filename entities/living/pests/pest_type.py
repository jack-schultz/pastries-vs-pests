from __future__ import annotations
from enum import Enum
from entities.living.pests.ants.ant import Ant
from entities.living.pests.ants.armour_ant import ArmourAnt
from entities.living.pests.ants.heavy_armour_ant import HeavyArmourAnt
from entities.living.pests.mealworm import Mealworm
from entities.living.pests.rhino_beetle import RhinoBeetle
from entities.living.pests.springtail import Springtail
from entities.living.pests.stinkbug import Stinkbug


# Every kind of pest a level can spawn. Level data uses these as wave
# keys, for example {PestType.ANT: 3} spawns three ants.
class PestType(Enum):
    """The kinds of pests that can appear in a wave."""
    ANT = Ant
    ARMOUR_ANT = ArmourAnt
    HEAVY_ARMOUR_ANT = HeavyArmourAnt
    STINKBUG = Stinkbug  # Leaps over the first good.
    RHINO_BEETLE = RhinoBeetle  # Eats more the longer it chews.
    SPRINGTAIL = Springtail  # Charges in for one big headbutt.
    MEALWORM = Mealworm  # Stuns the goods it hits.
