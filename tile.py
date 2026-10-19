from entity import Entity
from rectangle import Rectangle
from good import Good


class Tile(Entity):
    def __init__(self, rect: Rectangle):
        super().__init__(rect)
        self.__good = None

    @property
    def good(self):
        return self.__good

    @good.setter
    def good(self, good):
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

    def clear_good(self):
        self.__good = None
