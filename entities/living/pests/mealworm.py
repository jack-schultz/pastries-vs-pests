from __future__ import annotations
from armour.chainmail import Chainmail
from entities.living.goods.base_good import BaseGood
from entities.living.pests.base_pest import BasePest


class Mealworm(BasePest):
    # Each bite into the same good does more and more damage.
    def __init__(self, canvas, x, y) -> None:
        self.__first_bite = 40
        self.__bite_growth = 25
        self.__max_bite = 200
        super().__init__(
            canvas, x, y,
            armour=Chainmail(),
            speed=0.22,
            damage=self.__first_bite,
        )
        self.__target: BaseGood | None = None
        self.__bite = self.__first_bite

    @property
    def bite(self) -> int:
        return self.__bite

    def _strike(self, good: BaseGood) -> None:
        if good is self.__target:
            self.__bite = min(self.__bite + self.__bite_growth, self.__max_bite)
        else:
            self.__target = good
            self.__bite = self.__first_bite
        good.take_damage(self.__bite)
