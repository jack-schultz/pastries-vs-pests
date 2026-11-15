from __future__ import annotations
import time
import tkinter as tk
from abc import ABC
from typing import TYPE_CHECKING
from entities.living.living import Living
from entities.flour import Flour
from entities.projectiles.projectile import Projectile

if TYPE_CHECKING:
    from entities.living.pests.base_pest import BasePest


class BaseGood(Living, ABC):
    """
    Base class for goods placed on tiles. Each good acts on its own
    timer.
    """

    def __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            colour,
            health: int) -> None:
        super().__init__(canvas, x, y, width, height, colour, health)
        self.rect.centre = (x, y)
        self.__last_action = time.monotonic()
        self.__stunned_until = 0.0
        self.__shown_stunned = False

    @property
    def is_stunned(self) -> bool:
        return time.monotonic() < self.__stunned_until

    def stun(self, seconds: float) -> None:
        # Stops the good acting for a while. A new stun can extend it,
        # never shorten it.
        self.__stunned_until = max(
            self.__stunned_until, time.monotonic() + seconds)
        self.__shown_stunned = True
        self.rect.set_outline("#7e57c2", width=6)

    def can_act(self) -> bool:
        # A stunned good cannot act.
        if self.is_stunned:
            return False

        # Makes sure to remove stunned outline.
        if self.__shown_stunned:
            self.__shown_stunned = False
            self.rect.set_outline("", width=1)
        return True

    def _ready(self, interval: float) -> bool:
        # True once `interval` seconds have passed since the last
        # action, and restarts the timer.
        if time.monotonic() - self.__last_action < interval:
            return False
        self.__last_action = time.monotonic()
        return True

    def act(
            self,
            canvas: tk.Canvas,
            pests: list[BasePest] | None = None) -> Flour | Projectile | None:
        # Called every frame with the live pests. Returns whatever the
        # good made this frame, if anything.
        pass
