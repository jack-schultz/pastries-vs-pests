from entity import Entity


class Card(Entity):
    def __init__(self, rect, name: str, cost: int, good_class):
        rect.set_text(name, colour="#ffffff")
        super().__init__(rect)
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class

    @property
    def name(self):
        return self.__name

    @property
    def cost(self):
        return self.__cost

    def create_good(self, rect):
        # The card knows which good it sells, so the caller doesn't need to
        return self.__good_class(rect=rect)
