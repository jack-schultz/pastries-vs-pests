from __future__ import annotations
from enum import Enum, auto


# Affects what armour defends against
# For example: chainmail doesn't defend against fire
class DamageType(Enum):
    PHYSICAL = 1
    FIRE = 2
    EXPLOSIVE = 3
    GAS = 4
    ACID = 5


# Direction attack came from, for example SugarCubes hit from the left, so are blocked by a shield
# But a shield would not defend an explosion from behind
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    BELOW = 4
    AMBIENT = 5  # like explosions or poison gas


class Damage:
    def __init__(
            self,
            amount: float,
            damage_type: DamageType = DamageType.PHYSICAL,
            direction: Direction = Direction.LEFT
    ) -> None:
        self.__amount = amount
        self.__type = damage_type
        self.__direction = direction

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def type(self) -> DamageType:
        return self.__type

    @property
    def direction(self) -> Direction:
        return self.__direction
