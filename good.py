from __future__ import annotations
import math
import random
import time
from abc import ABC
from rectangle import Rectangle
from objects import Flour


class Good(ABC):
    def __init__(self, rect: Rectangle, health: int):
        self.__rect = rect
        self.__health = health

    @property
    def rect(self):
        return self.__rect

    @property
    def health(self):
        return self.__health


class FlourFlower(Good):
    def __init__(self, rect):
        super().__init__(rect, 50)
        self.__production_amount = 25
        self.__production_interval = 15  # seconds between spawns
        self.__spawn_distance = 40  # pixels from the flower's centre
        self.__flour_size = 30
        self.__last_spawn = time.monotonic()

    def produce(self, canvas) -> Flour | None:
        if time.monotonic() - self.__last_spawn < self.__production_interval:
            return None
        self.__last_spawn = time.monotonic()

        # Spawn a small distance away from the flower in a random direction
        angle = random.uniform(0, 2 * math.pi)
        cx, cy = self.rect.centre
        fx = cx + self.__spawn_distance * math.cos(angle)
        fy = cy + self.__spawn_distance * math.sin(angle)
        half = self.__flour_size // 2
        flour_rect = Rectangle(canvas, fx - half, fy - half, self.__flour_size, self.__flour_size, "#ffffff")
        return Flour(rect=flour_rect, amount=self.__production_amount)
