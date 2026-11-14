from __future__ import annotations
from armour.base_armour import BaseArmour
from entities.living.goods.base_good import BaseGood
from entities.living.pests.ants.ant import Ant
from entities.living.pests.base_pest import BasePest


class Springtail(Ant):
    # like an ant, but jumps over first good
    def __init__(
        self,
        canvas, x, y,
    ) -> None:
        super().__init__(
            canvas, x, y,
        )

        # Quicker and has less health, all other stats match ants
        self.speed = 0.4
        self.max_health = 120

        self.rect.set_text("Springtail", colour="#ffffff")
        self.__can_leap = True
        self.__has_leapt = False

    @property
    def has_leapt(self) -> bool:
        return self.__has_leapt

    def attack(self, good: BaseGood) -> None:
        # The first good it meets gets hopped over instead of eaten
        if self.__can_leap and not self.__has_leapt:
            self.__has_leapt = True
            # Land with its front just past the good's left edge, so it is no longer blocked
            self.rect.right = good.rect.left - 1
            self.speed = 0.25  # Slows down to normal ant speed after jump
            return
        super().attack(good)
