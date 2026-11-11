from __future__ import annotations
from entities.living.goods.base_good import BaseGood


class Hardtack(BaseGood):
    def __init__(self, canvas, x, y) -> None:
        colour = "#FFFF00"
        health = 3000
        super().__init__(canvas, x, y, 80, 80, colour, health)
        self.rect.set_text(type(self).__name__)
