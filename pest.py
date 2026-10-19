from abc import ABC
from rectangle import Rectangle


class Pest(ABC):
    def __init__(self, rect: Rectangle, health: int, speed: float):
        self.__rect = rect
        self.__health = health
        self.__speed = speed  # pixels moved left each frame

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


class Ant(Pest):
    def __init__(self, rect: Rectangle):
        super().__init__(rect, health=30, speed=0.5)
