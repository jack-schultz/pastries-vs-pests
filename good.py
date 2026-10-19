from __future__ import annotations
import math
import random
import time
import tkinter as tk
from abc import ABC, abstractmethod
from entity import Living
from rectangle import Rectangle
from objects import Flour, Projectile


class Good(Living, ABC):
    # Base class for goods placed on tiles. Each good acts on its own timer
    def __init__(self, rect: Rectangle, health: int) -> None:
        super().__init__(rect, health)
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
    def __init__(self, rect: Rectangle) -> None:
        rect.set_text(type(self).__name__)
        super().__init__(rect, 50)
        self.__production_amount = 25
        self.__production_interval = 15  # seconds between spawns
        self.__spawn_distance = 40  # pixels from the flower's centre
        self.__flour_size = 30

    def act(self, canvas: tk.Canvas) -> Flour | None:
        if not self._ready(self.__production_interval):
            return None

        # Spawn a small distance away from the flower in a random direction
        angle = random.uniform(0, 2 * math.pi)
        cx, cy = self.rect.centre
        fx = cx + self.__spawn_distance * math.cos(angle)
        fy = cy + self.__spawn_distance * math.sin(angle)
        half = self.__flour_size // 2
        flour_rect = Rectangle(canvas, fx - half, fy - half, self.__flour_size, self.__flour_size, "#ffffff")
        return Flour(rect=flour_rect, amount=self.__production_amount)


class SugarShooter(Good):
    def __init__(self, rect: Rectangle) -> None:
        rect.set_text(type(self).__name__)
        super().__init__(rect, 50)
        self.__shoot_interval = 1.5  # seconds between shots
        self.__projectile_size = 14
        self.__projectile_speed = 6  # pixels per frame
        self.__damage = 10

    def act(self, canvas: tk.Canvas) -> Projectile | None:
        if not self._ready(self.__shoot_interval):
            return None

        # Fire from the front-right of the shooter, along its row
        cx, cy = self.rect.centre
        half = self.__projectile_size // 2
        projectile_rect = Rectangle(canvas, cx + 20 - half, cy - half, self.__projectile_size, self.__projectile_size, "#ff8fab")
        return Projectile(rect=projectile_rect, damage=self.__damage, speed=self.__projectile_speed)
