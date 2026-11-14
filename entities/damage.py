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
        # Negative damage would heal the target, cant be having that.
        if amount < 0:
            raise ValueError(f"Damage amount can't be negative, got {amount}")

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
