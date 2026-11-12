from __future__ import annotations
import time
import tkinter as tk
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from entities.entity import Living
from entities.flour import Flour
from entities.projectile import Projectile

if TYPE_CHECKING:
    from entities.living.pests.base_pest import BasePest


class BaseGood(Living, ABC):
    # Base class for goods placed on tiles. Each good acts on its own timer
    def __init__(self, canvas, x, y, width, height, colour, health: int) -> None:
        super().__init__(canvas, x, y, width, height, colour, health)
        self.rect.centre = (x, y)
        self.__last_action = time.monotonic()

    def _ready(self, interval: float) -> bool:
        # True once `interval` seconds have passed since the last action, and restarts the timer
        if time.monotonic() - self.__last_action < interval:
            return False
        self.__last_action = time.monotonic()
        return True

    def act(self, canvas: tk.Canvas, pests: list[BasePest] | None = None) -> Flour | Projectile | None:
        # Called every frame with the live pests. Returns whatever the good made this frame, if anything
        pass
