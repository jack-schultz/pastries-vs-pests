from __future__ import annotations
import time
from abc import ABC
from entities.damage import Damage
from entities.entity import Living
from armour.base_armour import BaseArmour
from entities.living.goods.base_good import BaseGood


class BasePest(Living, ABC):
    def __init__(
        self,
        canvas,
        x, y,
        size,
        colour,
        health: int,
        speed: float,
        damage: int = 100,
        attack_interval: float = 1.0,
        armour: BaseArmour | None = None
    ) -> None:
        super().__init__(canvas, x, y, size, size, colour, health, armour)
        self.rect.centre_left = (x, y)
        self.rect.set_text("Ant", colour="#ffffff")

        self.__update_armour_outline()

        self.__speed = speed  # pixels moved left each frame
        self.__damage = damage  # damage dealt to a good per attack
        self.__attack_interval = attack_interval  # seconds between attacks
        self.__last_attack = 0.0

    def __update_armour_outline(self) -> None:
        # Armour's outline colour is only shown while the pest still has armour
        if self.armour is not None and not self.armour.is_broken:
            self.rect.set_outline(self.armour.outline_colour, width=3)
        else:
            self.rect.set_outline("", width=1)

    def take_damage(self, damage: Damage | float) -> None:
        super().take_damage(damage)
        self.__update_armour_outline()

    @property
    def speed(self) -> float:
        return self.__speed

    def move(self) -> None:
        self.rect.move((-self.__speed, 0))

    def is_blocked_by(self, good: BaseGood) -> bool:
        # Blocked when the pest's left edge (at its vertical centre) has reached the good
        px = self.rect.left
        _, py = self.rect.centre
        return good.rect.collide_point((px, py))

    def has_left_screen(self) -> bool:
        return self.rect.left + self.rect.w < 0

    def attack(self, good: BaseGood) -> None:
        # Only hit once per attack interval
        now = time.monotonic()
        if now - self.__last_attack < self.__attack_interval:
            return
        self.__last_attack = now
        good.take_damage(self.__damage)
