from __future__ import annotations
from app.rectangle import Rectangle


class Entity:
    """Base class for everything drawn on the canvas. Every entity owns one rect"""
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
