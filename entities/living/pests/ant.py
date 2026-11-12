from __future__ import annotations
from armour.base_armour import BaseArmour
from armour.chainmail import Chainmail
from entities.living.pests.base_pest import BasePest


class Ant(BasePest):
    def __init__(self, canvas, x, y, armour: BaseArmour | None = None) -> None:
        super().__init__(
            canvas, x, y,
            size=30,
            colour="#915831",
            health=160,
            speed=0.25,
            armour=armour
        )


class ArmourAnt(Ant):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            armour=Chainmail(80)
        )


class HeavyArmourAnt(Ant):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            armour=Platemail(80)
        )
