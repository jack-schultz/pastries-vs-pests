from __future__ import annotations
import time
from abc import ABC
from entities.damage import Damage
from entities.living.living import Living
from armour.base_armour import BaseArmour
from entities.living.goods.base_good import BaseGood


class BasePest(Living, ABC):
    """Base class for all pests."""

    def __init__(
        self, canvas, x, y,
        size, colour,
        health: int = 160,
        speed: float = 0.25,
        damage: int = 100,
        attack_interval: float = 1.0,
        armour: BaseArmour | None = None,
        layer_count: int = 1,
    ) -> None:
        super().__init__(canvas, x, y, size, size, colour, health, armour,
                         layer_count)
        self.rect.centre_left = (x, y)
        self.rect.set_text("BasePest", colour="#ffffff")

        self.__update_armour_outline()

        self.__speed = speed  # Pixels moved left each frame.
        self.__damage = damage  # Damage dealt to a good per attack.
        # Time between attacks in seconds.
        self.__attack_interval = attack_interval
        self.__last_attack = 0.0

    def __update_armour_outline(self) -> None:
        # Armour's outline colour is only shown while the pest still has
        # armour.
        if self.armour is not None and not self.armour.is_broken:
            self.rect.set_outline(self.armour.outline_colour, width=3)
        else:
            self.rect.set_outline("", width=1)

    def take_damage(self, damage: Damage | float) -> None:
        super().take_damage(damage)
        self.__update_armour_outline()

    @property
    def attack_interval(self):
        return self.__attack_interval

    @attack_interval.setter
    def attack_interval(self, new_attack_interval):
        if isinstance(new_attack_interval, float):
            self.__attack_interval = new_attack_interval
        else:
            raise ValueError(
                f"Expected float, got {type(new_attack_interval)}")

    @property
    def speed(self) -> float:
        return self.__speed

    @speed.setter
    def speed(self, new_speed: float) -> None:
        self.__speed = new_speed

    @property
    def damage(self) -> int:
        return self.__damage

    def move(self) -> None:
        self.rect.move((-self.__speed, 0))

    def is_blocked_by(self, good: BaseGood) -> bool:
        # Blocked when the pest's left edge (at its vertical centre) has
        # reached the good.
        px = self.rect.left
        _, py = self.rect.centre
        return good.rect.collide_point((px, py))

    def has_left_screen(self) -> bool:
        return self.rect.left + self.rect.w < 0

    def attack(self, good: BaseGood) -> None:
        # Only hit once per attack interval.
        now = time.monotonic()
        if now - self.__last_attack < self.__attack_interval:
            return
        self.__last_attack = now
        self._strike(good)

    # Protected instead of private to allow overwrites.
    def _strike(self, good: BaseGood) -> None:
        # One hit on the good. Subclasses override this to attack in
        # their own way.
        good.take_damage(self.__damage)
