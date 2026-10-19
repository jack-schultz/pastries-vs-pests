from __future__ import annotations
from entity import Entity
from good import Good


class Tile(Entity):
    def __init__(self, canvas, x, y, size, colour) -> None:
        super().__init__(canvas, x, y, size, size, colour)
        self.__good: Good | None = None

    @property
    def good(self) -> Good | None:
        return self.__good

    @good.setter
    def good(self, good: Good) -> bool:
        # Skip is tile already has a good
        if self.__good:
            return False

        if not isinstance(good, Good):
            return False

        self.__good = good
        return True

    @property
    def is_empty(self) -> bool:
        return self.__good is None

    def clear_good(self) -> None:
        self.__good = None
