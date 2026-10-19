from rectangle import Rectangle


class Good:
    def __init__(self, rect: Rectangle, name: str, health: int):
        self__rect = rect
        self.__name = name
        self.__health = health

    @property
    def rect(self):
        return self.__rect

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health


class FlourFlower(Good):
    def __init__(self, production_amount: int, production_rate: int):
        self.__production_amount = production_amount
        self.__production_rate = production_rate

    def produce(self):
        pass
