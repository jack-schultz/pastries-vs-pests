from __future__ import annotations
from typing import TYPE_CHECKING
from entities.entity import Entity

# Only needed for the type hint
# importing at runtime would create an import loop error
if TYPE_CHECKING:
    from entities.living.pest import Pest


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
