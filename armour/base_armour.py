from __future__ import annotations
from entities.damage import Damage, DamageType, Direction


class BaseArmour:
    # Armour has its own durability, separate from the wearer's health.
    # Subclasses configure it through __init__, and can override absorb()
    # for anything the tables can't express.
    def __init__(
            self,
            durability: float,
            outline_colour: str = "#9a9a9a",
            covered_directions: set[Direction] | None = None,
            absorption: dict[DamageType, float] | None = None,
            wear: dict[DamageType, float] | None = None
    ) -> None:
        self.__durability = durability
        self.__outline_colour = outline_colour
        # Directions this armour protects. Anything else hits the wearer directly
        self.__covered_directions = set(Direction) if covered_directions is None else covered_directions
        # Fraction of a damage type the armour takes (1.0 = all, 0.0 = none, passes through)
        self.__absorption = absorption or {}
        # Durability lost per point absorbed (>1 is a weakness, <1 is a strength)
        self.__wear = wear or {}

    @property
    def durability(self) -> float:
        return self.__durability

    @property
    def outline_colour(self) -> str:
        return self.__outline_colour

    @property
    def is_broken(self) -> bool:
        return self.__durability <= 0

    def absorb(self, damage: Damage) -> float:
        # Returns the damage that gets through to the wearer's health
        if self.is_broken or damage.direction not in self.__covered_directions:
            return damage.amount

        wear = self.__wear.get(damage.type, 1.0)
        wanted = damage.amount * self.__absorption.get(damage.type, 1.0)
        # Can only absorb as much as the remaining durability allows
        absorbed = min(wanted, self.__durability / wear) if wear > 0 else wanted
        self.__durability -= absorbed * wear
        return damage.amount - absorbed
