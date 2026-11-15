from __future__ import annotations
import math
import random
import tkinter as tk
from app.rectangle import Rectangle
from entities.flour import Flour
from entities.living.goods.base_good import BaseGood


class FlourFlower(BaseGood):
    """A good that produces flour over time."""

    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=50, height=50,
            colour="#FFFF00",
            health=300
        )
        self.__draw(self.rect)
        self.__production_amount = 25
        self.__production_interval = 12  # Time between flour drops in seconds.
        self.__spawn_distance = 40  # Pixels from the flower's centre.

    def __draw(self, rect: Rectangle) -> None:
        self.rect.hide_hitbox()

        # Stem and leaves, white flour petals and a golden wheat centre.
        cx, cy = rect.centre
        rect.draw("line", cx, cy + 4, cx, cy + 26, fill="#2e7d32", width=4)
        rect.draw("oval", cx - 14, cy + 12, cx, cy +
                  20, fill="#43a047", outline="")
        rect.draw("oval", cx, cy + 16, cx + 14, cy +
                  24, fill="#43a047", outline="")

        # Draw the petals.
        for i in range(8):
            angle = i * math.pi / 4
            px, py = cx + 13 * math.cos(angle), cy - 6 + 13 * math.sin(angle)
            rect.draw("oval", px - 8, py - 8, px + 8, py +
                      8, fill="#fffdf5", outline="#d7ccc8")

        # Draw the yellow centre.
        rect.draw("oval", cx - 9, cy - 15, cx + 9, cy + 3,
                  fill="#f2b632", outline="#c68a12", width=2)

        # Little dot eyes so it looks friendly.
        rect.draw("oval", cx - 5, cy - 9, cx - 2,
                  cy - 6, fill="#3d2b1f", outline="")
        rect.draw("oval", cx + 2, cy - 9, cx + 5,
                  cy - 6, fill="#3d2b1f", outline="")

    def act(self, canvas: tk.Canvas, pests=None) -> Flour | None:
        if not self._ready(self.__production_interval):
            return None

        # Spawn a small distance away from the flower in a random
        # direction.
        angle = random.uniform(0, 2 * math.pi)
        cx, cy = self.rect.centre
        fx = cx + self.__spawn_distance * math.cos(angle)
        fy = cy + self.__spawn_distance * math.sin(angle)
        return Flour(canvas, fx, fy, amount=self.__production_amount)
