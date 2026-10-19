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


class Projectile:
    def __init__(self, rect: Rectangle, damage: int, speed: float):
        self.__rect = rect
        self.__damage = damage
        self.__speed = speed  # pixels moved right each frame

    @property
    def rect(self):
        return self.__rect

    @property
    def damage(self):
        return self.__damage

    def move(self):
        self.__rect.move((self.__speed, 0))
