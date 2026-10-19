from __future__ import annotations
import math
import random
import time
from abc import ABC
from rectangle import Rectangle
from objects import Flour, Projectile


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

    @property
    def is_dead(self):
        return self.__health <= 0

    def take_damage(self, amount: int):
        self.__health -= amount


class FlourFlower(Good):
    def __init__(self, rect):
        rect.set_text(type(self).__name__)
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


class SugarShooter(Good):
    def __init__(self, rect):
        rect.set_text(type(self).__name__)
        super().__init__(rect, 50)
        self.__shoot_interval = 1.5  # seconds between shots
        self.__projectile_size = 14
        self.__projectile_speed = 6  # pixels per frame
        self.__damage = 10
        self.__last_shot = time.monotonic()

    def shoot(self, canvas) -> Projectile | None:
        if time.monotonic() - self.__last_shot < self.__shoot_interval:
            return None
        self.__last_shot = time.monotonic()

        # Fire from the front-right of the shooter, along its row
        cx, cy = self.rect.centre
        half = self.__projectile_size // 2
        projectile_rect = Rectangle(canvas, cx + 20 - half, cy - half, self.__projectile_size, self.__projectile_size, "#ff8fab")
        return Projectile(rect=projectile_rect, damage=self.__damage, speed=self.__projectile_speed)
