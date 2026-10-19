from rectangle import Rectangle
from good import Good


class Tile:
    def __init__(self, rect: Rectangle):
        self.__rect = rect
        self.__good = None

    @property
    def rect(self):
        return self.__rect

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

    def clear_good(self):
        self.__good = None
