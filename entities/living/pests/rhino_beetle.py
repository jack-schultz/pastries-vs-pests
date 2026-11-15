from __future__ import annotations
from armour.helmet import Helmet
from entities.living.goods.base_good import BaseGood
from entities.living.pests.base_pest import BasePest


class RhinoBeetle(BasePest):
    """Charges in fast and headbutts the first good it reaches with a
    big first hit.
    """

    def __init__(self, canvas, x, y) -> None:
        self.__ram_damage = 450
        self.__tired_speed = 0.2
        super().__init__(
            canvas, x, y,
            size=45,  # It is the biggest pest.
            colour="#3b2a20",
            armour=Helmet(),
            speed=0.9,
            damage=40,
            layer_count=2
        )
        self.rect.set_text("Rhino Beetle", colour="#ffffff")
        self.__has_rammed = False

    @property
    def has_rammed(self) -> bool:
        return self.__has_rammed

    def _strike(self, good: BaseGood) -> None:
        if not self.__has_rammed:
            # It only charges once in its life.
            self.__has_rammed = True
            self.speed = self.__tired_speed
            good.take_damage(self.__ram_damage)
            return
        super()._strike(good)
