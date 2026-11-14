from __future__ import annotations
from armour.shield import Shield
from entities.living.goods.base_good import BaseGood
from entities.living.pests.ants.ant import Ant
from entities.living.pests.base_pest import BasePest


class Stinkbug(Ant):
    # Stinks the good it hits, stunning the good (prevents them from acting)
    # Otherwise, like an ant with slower attacks
    def __init__(self, canvas, x, y) -> None:
        self.__stun_time = 3.0  # seconds
        super().__init__(
            canvas, x, y,
            armour=Shield(),
        )
        self.attack_interval = 1.5
        self.rect.set_text("Stinkbug", colour="#ffffff")

    @property
    def stun_time(self) -> float:
        return self.__stun_time

    def _strike(self, good: BaseGood) -> None:
        super()._strike(good)
        good.stun(self.__stun_time)
