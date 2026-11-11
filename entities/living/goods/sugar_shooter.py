from __future__ import annotations
import tkinter as tk
from entities.projectile import Projectile
from entities.living.goods.base_good import BaseGood


class SugarShooter(BaseGood):
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
        self.__projectile_piercing = 1

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
            speed=self.__projectile_speed,
            piercing=self.__projectile_piercing
        )
