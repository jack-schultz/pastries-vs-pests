from __future__ import annotations
from entities.damage_type import DamageType
from entities.direction import Direction


class Damage:
    def __init__(
        self,
        amount: float,
        damage_type: DamageType = DamageType.BLUDGEONING,
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
