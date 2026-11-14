from __future__ import annotations
import time
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction
from entities.living.goods.base_good import BaseGood


class PoppingCandy(BaseGood):
    # Buried and harmless while arming, then explodes when a pest reaches it
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=50, height=35,
            colour="#8d6e63",
            health=200
        )
        self.__arm_time = 13  # seconds before it can detonate
        self.__planted_at = time.monotonic()
        self.__blast_damage = 1800
        self.__blast_radius = 110  # pixels from the candy's centre
        self.__row_tolerance = 45  # pests must be in the same row
        self.__shown_armed = False
        self.__refresh_display()

    @property
    def is_armed(self) -> bool:
        return time.monotonic() - self.__planted_at >= self.__arm_time

    def __refresh_display(self) -> None:
        if self.is_armed:
            self.rect.set_colour("#ff1744")
            self.rect.set_text("Popping\nCandy", colour="#ffffff")
        else:
            self.rect.set_colour("#8d6e63")
            self.rect.set_text("Arming...", colour="#ffffff")

    def act(self, canvas, pests=None) -> None:
        # Switch to the armed look once, the moment the arming time is up
        if not self.__shown_armed and self.is_armed:
            self.__shown_armed = True
            self.__refresh_display()
        return None

    def detonate(self, pests) -> list:
        # Hurts every pest in this row within the blast radius, then destroys itself. Returns the pests hit
        cx, cy = self.rect.centre
        hit = []
        for pest in pests:
            px, py = pest.rect.centre
            if abs(py - cy) <= self.__row_tolerance and abs(px - cx) <= self.__blast_radius:
                pest.take_damage(Damage(self.__blast_damage, DamageType.EXPLOSIVE, Direction.AMBIENT))
                hit.append(pest)
        self.take_damage(self.health)  # the candy is used up
        return hit
