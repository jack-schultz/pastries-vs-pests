from __future__ import annotations
import time
from abc import ABC
from entity import Living
from good import Good
from rectangle import Rectangle


class Pest(Living, ABC):
    def __init__(self, rect: Rectangle, health: int, speed: float, damage: int = 10, attack_interval: float = 1.0) -> None:
        rect.set_text("Ant", colour="#ffffff")
        super().__init__(rect, health)
        self.__speed = speed  # pixels moved left each frame
        self.__damage = damage  # damage dealt to a good per attack
        self.__attack_interval = attack_interval  # seconds between attacks
        self.__last_attack = 0.0

    @property
    def speed(self) -> float:
        return self.__speed

    def move(self) -> None:
        self.rect.move((-self.__speed, 0))

    def is_blocked_by(self, good: Good) -> bool:
        # Blocked when the pest's left edge (at its vertical centre) has reached the good
        px = self.rect.x
        _, py = self.rect.centre
        return good.rect.collide_point((px, py))

    def has_left_screen(self) -> bool:
        return self.rect.x + self.rect.w < 0

    def attack(self, good: Good) -> None:
        # Only hit once per attack interval
        now = time.monotonic()
        if now - self.__last_attack < self.__attack_interval:
            return
        self.__last_attack = now
        good.take_damage(self.__damage)


class Ant(Pest):
    def __init__(self, rect: Rectangle) -> None:
        super().__init__(rect, health=30, speed=0.5)
