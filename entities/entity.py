from __future__ import annotations
from app.rectangle import Rectangle
from entities.damage import Damage
from armour.base_armour import BaseArmour


class Entity:
    # Base class for everything drawn on the canvas. Every entity owns one rect
    def __init__(self, canvas, x, y, width, height, colour) -> None:
        self.__rect = Rectangle(canvas, x, y, width, height, colour)

    @property
    def canvas(self):
        return self.rect.canvas

    @property
    def rect(self) -> Rectangle:
        return self.__rect

    def destroy(self) -> None:
        self.__rect.delete()


class Living(Entity):
    # Base class for entities with health that can be hurt and die
    def __init__(self, canvas, x, y, width, height, colour, health: int, armour: BaseArmour | None = None, layer_count: int = 1) -> None:
        super().__init__(canvas, x, y, width, height, colour)
        self.__health = health
        self.__armour = armour
        self.__layer_count = layer_count

    @property
    def health(self) -> int:
        return self.__health

    @property
    def armour(self) -> BaseArmour | None:
        return self.__armour

    @property
    def layer_count(self) -> int:
        return self.__layer_count

    @property
    def is_dead(self) -> bool:
        return self.__health <= 0

    def take_damage(self, damage: Damage | float) -> None:
        # If a float comes through, treat it as default damage
        if not isinstance(damage, Damage):
            damage = Damage(damage)

        remaining = damage.amount
        if self.__armour is not None:
            remaining = self.__armour.absorb(damage)
        self.__health -= remaining
