

class Card:
    def __init__(self, rect, name: str, cost: int, bread_class):
        self.__rect = rect
        self.__name = name
        self.__cost = cost
        self.__bread_class = bread_class

    @property
    def rect(self):
        return self.__rect

    @property
    def name(self):
        return self.__name

    @property
    def cost(self):
        return self.__cost

    @property
    def bread_class(self):
        return self.__bread_class
