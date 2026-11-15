from __future__ import annotations
from enum import Enum


# Affects what armour defends against. For example: chainmail doesn't
# defend against fire.
class DamageType(Enum):
    """The different types of damage an attack can deal."""
    BLUDGEONING = 1
    FIRE = 2
    EXPLOSIVE = 3
    GAS = 4
    ACID = 5
    PIERCING = 6
