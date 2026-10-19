
class Bread:
    def __init__(self, name, health):
        self.__name = name
        self.__health = health

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health
