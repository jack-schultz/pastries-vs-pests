

class Card:
    def __init__(self, name: str, cost: int, bread_class):
        self.__name = name
        self.__cost = cost
        self.__bread_class = bread_class

    @property
    def name(self):
        return self.__name

    @property
    def cost(self):
        return self.__cost

    @property
    def bread_class(self):
        return self.__bread_class
