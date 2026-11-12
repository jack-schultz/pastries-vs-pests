from __future__ import annotations
import math
import random
import tkinter as tk
from entities.flour import Flour
from entities.living.goods.base_good import BaseGood


class FlourFlower(BaseGood):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=50, height=50,
            colour="#FFFF00",
            health=300
        )
        self.rect.set_text(type(self).__name__)
        self.__production_amount = 25
        self.__production_interval = 3  # seconds between spawns
        self.__spawn_distance = 40  # pixels from the flower's centre

    def act(self, canvas: tk.Canvas, pests=None) -> Flour | None:
        if not self._ready(self.__production_interval):
            return None

        # Spawn a small distance away from the flower in a random direction
        angle = random.uniform(0, 2 * math.pi)
        cx, cy = self.rect.centre
        fx = cx + self.__spawn_distance * math.cos(angle)
        fy = cy + self.__spawn_distance * math.sin(angle)
        return Flour(canvas, fx, fy, amount=self.__production_amount)
