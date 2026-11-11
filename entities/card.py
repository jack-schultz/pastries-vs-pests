from __future__ import annotations
from typing import Callable
from entities.entity import Entity
from entities.living.goods.base_good import BaseGood
from app.rectangle import Rectangle


class Card(Entity):
    def __init__(self, canvas, x, y, width, height, name: str, cost: int, good_class: Callable[[Rectangle], BaseGood], cooldown: float = 5.0) -> None:
        super().__init__(canvas, x, y, width, height, "#e63946")
        self.rect.set_text(name, colour="#ffffff")
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class
        self.__cooldown_frames = round(cooldown * 60)
        self.__frames_left = 0  # 0 means ready to select

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cost(self) -> int:
        return self.__cost

    @property
    def is_ready(self) -> bool:
        return self.__frames_left == 0

    def start_cooldown(self) -> None:
        # Called when the card's good is placed, like Plants vs Zombies
        self.__frames_left = self.__cooldown_frames
        self.__refresh_display()

    def tick_cooldown(self) -> None:
        if self.__frames_left > 0:
            self.__frames_left -= 1
            self.__refresh_display()

    def __refresh_display(self) -> None:
        # Dark card with seconds left while recharging, bright and plain when ready
        if self.is_ready:
            self.rect.set_colour("#e63946")
            self.rect.set_text(self.__name, colour="#ffffff")
        else:
            seconds = self.__frames_left / 60
            self.rect.set_colour("#7a1d24")
            self.rect.set_text(f"{self.__name}\n{seconds:.1f}s", colour="#ffffff")

    def create_good(self, canvas, x, y) -> BaseGood:
        # The card knows which good it sells, so the caller doesn't need to
        return self.__good_class(canvas, x, y)
