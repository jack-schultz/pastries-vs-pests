from __future__ import annotations
import math
import random
import time
import tkinter as tk
from abc import ABC, abstractmethod
from entities.entity import Living
from entities.flour import Flour
from entities.projectile import Projectile


class Good(Living, ABC):
    # Base class for goods placed on tiles. Each good acts on its own timer
    def __init__(self, canvas, x, y, width, height, colour, health: int) -> None:
        super().__init__(canvas, x, y, width, height, colour, health)
        self.__last_action = time.monotonic()

    def _ready(self, interval: float) -> bool:
        # True once `interval` seconds have passed since the last action, and restarts the timer
        if time.monotonic() - self.__last_action < interval:
            return False
        self.__last_action = time.monotonic()
        return True

    @abstractmethod
    def act(self, canvas: tk.Canvas) -> Flour | Projectile | None:
        # Called every frame. Returns whatever the good made this frame, if anything
        pass


class FlourFlower(Good):
    def __init__(self, canvas, x, y, width, height) -> None:
        colour = "#FFFF00"
        health = 300
        super().__init__(canvas, x, y, width, height, colour, health)
        self.rect.set_text(type(self).__name__)
        self.__production_amount = 25
        self.__production_interval = 24  # seconds between spawns
        self.__spawn_distance = 40  # pixels from the flower's centre

    def act(self, canvas: tk.Canvas) -> Flour | None:
        if not self._ready(self.__production_interval):
            return None

        # Spawn a small distance away from the flower in a random direction
        angle = random.uniform(0, 2 * math.pi)
        cx, cy = self.rect.centre
        fx = cx + self.__spawn_distance * math.cos(angle)
        fy = cy + self.__spawn_distance * math.sin(angle)
        return Flour(canvas, fx, fy, amount=self.__production_amount)


class SugarShooter(Good):
    def __init__(self, canvas, x, y, width, height) -> None:
        colour = "#FFFF00"
        health = 300
        super().__init__(canvas, x, y, width, height, colour, health)
        self.rect.set_text(type(self).__name__)
        self.__shoot_interval = 1.4  # seconds between shots
        self.__projectile_size = 14
        self.__projectile_speed = 6  # pixels per frame
        self.__projectile_colour = "#ff8fab"
        self.__projectile_damage = 60

    def act(self, canvas: tk.Canvas) -> Projectile | None:
        if not self._ready(self.__shoot_interval):
            return None

        # Fire from the front-right of the shooter, along its row
        x, y = self.rect.centre
        return Projectile(
            canvas, x, y,
            size=self.__projectile_size,
            colour=self.__projectile_colour,
            damage=self.__projectile_damage,
            speed=self.__projectile_speed
        )
