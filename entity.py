from __future__ import annotations
from rectangle import Rectangle


class Entity:
    # Base class for everything drawn on the canvas. Every entity owns one rect
    def __init__(self, rect: Rectangle) -> None:
        self.__rect = rect

    @property
    def rect(self) -> Rectangle:
        return self.__rect

    def destroy(self) -> None:
        self.__rect.delete()


class Living(Entity):
    # Base class for entities with health that can be hurt and die
    def __init__(self, rect: Rectangle, health: int) -> None:
        super().__init__(rect)
        self.__health = health

    @property
    def health(self) -> int:
        return self.__health

    @property
    def is_dead(self) -> bool:
        return self.__health <= 0

    def take_damage(self, amount: int) -> None:
        self.__health -= amount
