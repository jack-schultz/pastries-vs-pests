from __future__ import annotations
from armour.base_armour import BaseArmour
from entities.living.pests.base_pest import BasePest


class Ant(BasePest):
    """Basic pest, uses BasePest stats. This is the most basic unit."""

    def __init__(self, canvas, x, y, armour: BaseArmour | None = None) -> None:
        super().__init__(
            canvas, x, y,
            size=30,
            colour="#915831",
            armour=armour,
        )
        self.rect.set_text("Ant", colour="#ffffff")
