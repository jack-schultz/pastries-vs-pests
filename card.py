from __future__ import annotations
from typing import Callable
from entity import Entity
from good import Good
from rectangle import Rectangle


class Card(Entity):
    def __init__(self, rect: Rectangle, name: str, cost: int, good_class: Callable[[Rectangle], Good]) -> None:
        rect.set_text(name, colour="#ffffff")
        super().__init__(rect)
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cost(self) -> int:
        return self.__cost

    def create_good(self, rect: Rectangle) -> Good:
        # The card knows which good it sells, so the caller doesn't need to
        return self.__good_class(rect)
