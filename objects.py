from __future__ import annotations
from typing import TYPE_CHECKING
from entity import Entity
from rectangle import Rectangle

# Only needed for the type hint
# importing at runtime would create an import loop error
if TYPE_CHECKING:
    from pest import Pest


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


class Projectile(Entity):
    def __init__(self, canvas, centre_x, centre_y, size, colour, damage: int, speed: float) -> None:
        super().__init__(canvas, centre_x + 20 - size // 2, centre_y - size // 2, size, size, colour)
        self.__damage = damage
        self.__speed = speed  # pixels moved right each frame

    @property
    def damage(self) -> int:
        return self.__damage

    def move(self) -> None:
        self.rect.move((self.__speed, 0))

    def hits(self, pest: Pest) -> bool:
        # A projectile hits a pest when its centre is inside the pest's rect
        return pest.rect.collide_point(self.rect.centre)
