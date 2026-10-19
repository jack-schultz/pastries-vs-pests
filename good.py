from abc import ABC
from tile import Tile
from rectangle import Rectangle


class Good(ABC):
    def __init__(self, rect: Rectangle, tile: Tile, health: int):
        self.__rect = rect
        self.__tile = tile
        self.__health = health

    @property
    def rect(self):
        return self.__rect

    @property
    def tile(self):
        return self.__tile

    @property
    def health(self):
        return self.__health


class FlourFlower(Good):
    def __init__(self, rect, tile):
        super().__init__(rect, tile, 50)
        self.__production_amount = 20
        self.__production_rate = 50

    def produce(self):
        pass
