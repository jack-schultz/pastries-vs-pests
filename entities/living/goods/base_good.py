from __future__ import annotations
import time
import tkinter as tk
from abc import ABC, abstractmethod
from entities.entity import Living
from entities.flour import Flour
from entities.projectile import Projectile


class BaseGood(Living, ABC):
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