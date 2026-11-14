from __future__ import annotations
from entities.living.goods.base_good import BaseGood


class Hardtack(BaseGood):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            width=80, height=80,
            colour="#FFFF00",
            health=5000
        )
        self.rect.set_text("Hardtack")
