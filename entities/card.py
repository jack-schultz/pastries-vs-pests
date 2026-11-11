from __future__ import annotations
from typing import Callable
from entities.entity import Entity
from entities.living.goods.base_good import BaseGood
from app.rectangle import Rectangle


class Card(Entity):
    def __init__(self, canvas, x, y, width, height, name: str, cost: int, good_class: Callable[[Rectangle], BaseGood]) -> None:
        colour = "#e63946"

        super().__init__(canvas, x, y, width, height, colour)
        self.rect.set_text(name, colour="#ffffff")
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cost(self) -> int:
        return self.__cost

    def create_good(self, canvas, x, y, width, height) -> BaseGood:
        # The card knows which good it sells, so the caller doesn't need to
        return self.__good_class(canvas, x, y, width, height)
