import time
from abc import ABC
from rectangle import Rectangle


class Pest(ABC):
    def __init__(self, rect: Rectangle, health: int, speed: float, damage: int = 10, attack_interval: float = 1.0):
        rect.set_text("Ant", colour="#ffffff")
        self.__rect = rect
        self.__health = health
        self.__speed = speed  # pixels moved left each frame
        self.__damage = damage  # damage dealt to a good per attack
        self.__attack_interval = attack_interval  # seconds between attacks
        self.__last_attack = 0.0

    @property
    def rect(self):
        return self.__rect

    @property
    def health(self):
        return self.__health

    @property
    def speed(self):
        return self.__speed

    def move(self):
        self.__rect.move((-self.__speed, 0))

    def attack(self, good):
        # Only hit once per attack interval
        now = time.monotonic()
        if now - self.__last_attack < self.__attack_interval:
            return
        self.__last_attack = now
        good.take_damage(self.__damage)


class Ant(Pest):
    def __init__(self, rect: Rectangle):
        super().__init__(rect, health=30, speed=0.5)
