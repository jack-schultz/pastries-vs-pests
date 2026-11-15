from __future__ import annotations
from typing import TYPE_CHECKING
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction
from entities.entity import Entity

# Only needed for the type hint
# importing at runtime would create an import loop error
if TYPE_CHECKING:
    from entities.living.pests.base_pest import BasePest


class Projectile(Entity):
    """Base class for things that fly across the board."""

    def __init__(
            self, canvas, centre_x, centre_y, size, colour,
            damage: int, speed: float, piercing: int,
            damage_type: DamageType = DamageType.BLUDGEONING
    ) -> None:
        super().__init__(canvas, centre_x + 20 - size //
                         2, centre_y - size // 2, size, size, colour)
        self.__damage = damage
        self.__speed = speed  # pixels moved right each frame
        self.__piercing = piercing
        self.__damage_type = damage_type

        self.__hit_pests: list[BasePest] = []

    @property
    def damage(self) -> int:
        return self.__damage

    @property
    def damage_type(self) -> DamageType:
        return self.__damage_type

    def damage_to_deal(self) -> Damage:
        # Projectiles fly right, so they deal damage to the left side of pests
        return Damage(self.__damage, self.__damage_type, Direction.LEFT)

    @property
    def piercing(self) -> int:
        return self.__piercing

    @piercing.setter
    def piercing(self, new_piercing) -> None:
        self.__piercing = new_piercing

    def move(self) -> None:
        self.rect.move((self.__speed, 0))

    def add_hit_pest(self, pest: BasePest):
        if pest in self.__hit_pests:
            return
        self.__hit_pests.append(pest)

    def hits(self, pest: BasePest) -> bool:
        if pest in self.__hit_pests:
            return False

        return self.touches(pest)

    # Split from .hits to allow override for different behaviours
    # Ex: flame defines touching as anywhere along the projectile's length
    def touches(self, pest: BasePest) -> bool:
        # A projectile hits a pest when its centre right is inside the pest's
        # rect
        return pest.rect.collide_point(self.rect.centre_right)

    def is_expired(self) -> bool:
        # Projectiles have limited lifespan use this, like flames or gas clouds
        return False
