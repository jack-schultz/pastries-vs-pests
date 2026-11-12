from __future__ import annotations
import tkinter as tk
from entities.projectile import Projectile
from entities.living.goods.base_good import BaseGood


class SugarShooter(BaseGood):
    def __init__(self, canvas, x, y) -> None:
        colour = "#FFFF00"
        health = 300
        super().__init__(canvas, x, y, 40, 40, colour, health)
        self.rect.set_text(type(self).__name__)
        self.__shoot_interval = 1.4  # seconds between shots
        self.__projectile_size = 14
        self.__projectile_speed = 6  # pixels per frame
        self.__projectile_colour = "#ff8fab"
        self.__projectile_damage = 60
        self.__projectile_piercing = 1

    def __pest_in_lane(self, pests) -> bool:
        # A pest is in the lane when its vertical centre is within this shooter's row and it is ahead of the shooter
        top = self.rect.y
        bottom = top + self.rect.h
        shooter_x = self.rect.centre[0]
        for pest in pests or []:
            _, py = pest.rect.centre
            if top <= py <= bottom and pest.rect.x + pest.rect.w > shooter_x:
                return True
        return False

    def act(self, canvas: tk.Canvas, pests=None) -> Projectile | None:
        # Hold fire (and keep the timer ready) until a pest is in the lane
        if not self.__pest_in_lane(pests):
            return None
        if not self._ready(self.__shoot_interval):
            return None

        # Fire from the front-right of the shooter, along its row
        x, y = self.rect.centre_right
        return Projectile(
            canvas, x, y,
            size=self.__projectile_size,
            colour=self.__projectile_colour,
            damage=self.__projectile_damage,
            speed=self.__projectile_speed,
            piercing=self.__projectile_piercing
        )
