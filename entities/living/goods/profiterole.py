from __future__ import annotations
import time
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction
from entities.living.goods.base_good import BaseGood


class Profiterole(BaseGood):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=60, height=60,
            colour="#c2185b",
            health=150
        )
        self.__fuse = 1.2  # seconds between planting and exploding
        self.__planted_at = time.monotonic()
        self.__blast_damage = 1800
        self.__blast_radius = 135  # pixels; 1.5 tiles so it covers the 3x3 around its tile
        self.rect.set_text("Profiterole", colour="#ffffff")

    @property
    def is_primed(self) -> bool:
        return time.monotonic() - self.__planted_at >= self.__fuse

    def detonate(self, pests) -> list:
        # Hurts every pest within the blast radius, then destroys itself. Returns the pests hit
        cx, cy = self.rect.centre
        hit = []
        for pest in pests:
            px, py = pest.rect.centre
            if abs(px - cx) <= self.__blast_radius and abs(py - cy) <= self.__blast_radius:
                pest.take_damage(Damage(self.__blast_damage, DamageType.EXPLOSIVE, Direction.AMBIENT))
                hit.append(pest)
        self.take_damage(self.health)  # the bombe is used up
        return hit
