from __future__ import annotations
import tkinter as tk
from typing import Sequence
from entities.projectiles.projectile import Projectile
from entities.projectiles.sugar_cube import SugarCube
from entities.living.goods.base_good import BaseGood


class SugarShooter(BaseGood):
    def __init__(self, canvas, x, y, delay_pattern: Sequence[float] = (1.4,)) -> None:
        super().__init__(
            canvas, x, y,
            width=40, height=40,
            colour="#FFFF00",
            health=300
        )
        self.rect.set_text(type(self).__name__)
        self.__delay_pattern = delay_pattern
        self.__pattern_index = 0  # which delay in the pattern the next shot is waiting on

    @property
    def delay_pattern(self) -> Sequence[float]:
        return self.__delay_pattern

    def __pest_in_lane(self, pests) -> bool:
        # A pest is in the lane when its vertical centre is within this shooter's row and it is ahead of the shooter
        top = self.rect.top
        bottom = top + self.rect.h
        shooter_x = self.rect.centre[0]
        for pest in pests or []:
            _, py = pest.rect.centre
            if top <= py <= bottom and pest.rect.left + pest.rect.w > shooter_x:
                return True
        return False

    def act(self, canvas: tk.Canvas, pests=None) -> Projectile | None:
        # Hold fire (and keep the timer ready) until a pest is in the lane
        if not self.__pest_in_lane(pests):
            return None
        if not self._ready(self.__delay_pattern[self.__pattern_index]):
            return None
        self.__pattern_index = (self.__pattern_index + 1) % len(self.__delay_pattern)
        return self._make_projectile(canvas)

    def _make_projectile(self, canvas: tk.Canvas) -> Projectile:
        # Fire from the front-right of the shooter, along its row
        x, y = self.rect.centre_right
        return SugarCube(canvas, x, y)
