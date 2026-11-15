from __future__ import annotations
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction


class BaseArmour:
    """
    Armour has its own durability, separate from the wearer's health.
    Subclasses configure it through __init__, and can override absorb()
    for different functionality.
    """

    def __init__(
            self,
            durability: float,
            outline_colour: str = "#9a9a9a",
            covered_directions: set[Direction] | None = None,
            absorption: dict[DamageType, float] | None = None,
            wear: dict[DamageType, float] | None = None,
            layer_count: int = 1
    ) -> None:
        self.__durability = durability
        self.__outline_colour = outline_colour
        # Directions this armour protects. Anything else hits the wearer
        # directly.
        self.__covered_directions = set(
            Direction) if covered_directions is None else covered_directions
        # Fraction of a damage type the armour takes (1.0 = all, 0.0 =
        # none, passes through) If a damage type isn't in the list, it
        # does 1.0.
        self.__absorption = absorption or {}
        # Durability lost per point absorbed (>1 is a weakness, <1 is a
        # strength). If a damage type isn't in the list, it does 1.0.
        self.__wear = wear or {}
        # Extra layers affects projectile's piercing value.
        self.__layer_count = layer_count

    @property
    def durability(self) -> float:
        return self.__durability

    @property
    def outline_colour(self) -> str:
        return self.__outline_colour

    @property
    def layer_count(self) -> int:
        return self.__layer_count

    @property
    def is_broken(self) -> bool:
        return self.__durability <= 0

    def absorb(self, damage: Damage) -> float:
        # Returns the damage that gets through to the wearer's health.
        if self.is_broken or damage.direction not in self.__covered_directions:
            return damage.amount

        # ABSORB MECHANICS. If armour fully absorbs damage from a hit,
        # if the armour breaks, it will still absorb all damage for that
        # hit. Example 1: If an ant with chainmail (100 durability) is
        # hit with explosion (250 damage). the ant will take 200 damage.
        # The first 100 is halved by the chainmail, but it breaks and
        # the remaining damage is passed to the pest as the chainmail
        # does not block all damage. Example 2: But a shield in the same
        # situation: shield (100 durability) is hit with physical (250
        # damage). the ant should take zero damage, the shield is
        # destroyed and absorbs all the damage.

        wear = self.__wear.get(damage.type, 1.0)
        absorb_fraction = self.__absorption.get(damage.type, 1.0)
        handled_damage = damage.amount

        if absorb_fraction < 1.0 and wear > 0:
            # A partial block only holds up while it lasts, the rest
            # passes through untouched.
            handled_damage = min(handled_damage, self.__durability / wear)

        # A full block takes the whole hit, even if that wears out the
        # rest of its durability.
        self.__durability = max(0, self.__durability - (handled_damage * wear))

        return damage.amount - (handled_damage * absorb_fraction)
