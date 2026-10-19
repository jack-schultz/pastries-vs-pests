from rectangle import Rectangle


class Flour:
    def __init__(self, rect: Rectangle, amount: int):
        self.__rect = rect
        self.__amount = amount

    @property
    def rect(self):
        return self.__rect

    @property
    def amount(self):
        return self.__amount
