from __future__ import annotations
from entities.entity import Entity


class Flour(Entity):
    def __init__(self, canvas, x, y, amount: int) -> None:
        colour = "#ffffff"
        width, height = 30, 30
        # Spawn in center of coords given
        super().__init__(canvas, x - width // 2, y - height // 2, width, height, colour)
        self.__amount = amount

    @property
    def amount(self) -> int:
        return self.__amount

    def collect(self) -> int:
        # Removes the flour from the canvas and hands back its amount
        self.destroy()
        return self.__amount