from __future__ import annotations
from entities.entity import Entity
from entities.living.goods.base_good import BaseGood


class Tile(Entity):
    """A single square on the garden grid."""

    def __init__(self, canvas, x, y, size, colour) -> None:
        super().__init__(canvas, x, y, size, size, colour)
        self.__good: BaseGood | None = None

    @property
    def good(self) -> BaseGood | None:
        return self.__good

    @good.setter
    def good(self, good: BaseGood) -> None:
        # Tile holds 1 good, an occupied tile must be cleared first.
        if self.__good is not None:
            raise ValueError("Tile already has a good")

        if not isinstance(good, BaseGood):
            raise ValueError(
                f"Only a BaseGood can go on a tile, got {type(good).__name__}")

        self.__good = good

    @property
    def is_empty(self) -> bool:
        return self.__good is None

    def clear_good(self) -> None:
        self.__good = None
