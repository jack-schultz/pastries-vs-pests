

class Card:
    def __init__(self, rect, name: str, cost: int, good_class):
        rect.set_text(name, colour="#ffffff")
        self.__rect = rect
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class

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
    def good_class(self):
        return self.__good_class
