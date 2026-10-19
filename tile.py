from rectangle import Rectangle


class Tile:
    def __init__(self, rect: Rectangle):
        self.__rect = rect

    @property
    def rect(self):
        return self.__rect
