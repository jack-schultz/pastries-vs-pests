from __future__ import annotations
from entities.entity import Entity


class Flour(Entity):
    def __init__(self, canvas, x, y, amount: int) -> None:
        colour = "#ffffff"
        width, height = 30, 30
        # Spawn in center of coords given
        super().__init__(canvas, x - width // 2, y - height // 2, width, height, colour)
        self.__amount = amount
        self.__destination = None

    @property
    def amount(self) -> int:
        return self.__amount

    def move(self) -> None:
        if self.__destination:
            dx = (self.__destination[0] - self.rect.x) / 20
            dy = (self.__destination[1] - self.rect.y) / 20

            # Inside your update/run loop (called 20 times):
            self.rect.move((dx, dy))

    def finished_move(self) -> bool:
        if self.__destination:
            if self.rect.collide_point((self.__destination[0] + 10, self.__destination[1] + 10)):
                self.destroy()
                return True
        return False

    def click(self, destination) -> None:
        # Removes the flour from the canvas and hands back its amount
        if not self.__destination:
            self.__destination = destination
