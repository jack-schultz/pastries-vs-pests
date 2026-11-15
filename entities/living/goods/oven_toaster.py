from __future__ import annotations
import tkinter as tk
from entities.living.goods.base_good import BaseGood
from entities.projectiles.flame import Flame


class OvenToaster(BaseGood):
    """Breathes a flame three tiles to the right. Holds fire until a
    pest is within that range.
    """

    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=60, height=60,
            colour="#e65100",
            health=300
        )
        self.rect.set_text("Oven\nToaster", colour="#ffffff")
        self.__range = 3 * 90  # Three tiles, the garden's grid size is 90.
        self.__fire_interval = 2.5  # Time between flames in seconds.

    def __pest_in_range(self, pests) -> bool:
        # A pest is in range when it is in this plant's row and ahead of
        # it, within range.
        top, bottom = self.rect.top, self.rect.bottom
        front = self.rect.right
        for pest in pests or []:
            _, py = pest.rect.centre
            if top <= py <= bottom and pest.rect.left < front + \
                    self.__range and pest.rect.right > front:
                return True
        return False

    def act(self, canvas: tk.Canvas, pests=None) -> Flame | None:
        if not self.__pest_in_range(pests):
            return None
        if not self._ready(self.__fire_interval):
            return None
        # Start the flame just in front of the plant, in its row.
        return Flame(
            canvas,
            left=self.rect.right,
            centre_y=self.rect.centre_y,
            range_px=self.__range,
        )
