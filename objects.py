from entity import Entity
from rectangle import Rectangle


class Flour(Entity):
    def __init__(self, rect: Rectangle, amount: int):
        super().__init__(rect)
        self.__amount = amount

    @property
    def amount(self):
        return self.__amount

    def collect(self) -> int:
        # Removes the flour from the canvas and hands back its amount
        self.destroy()
        return self.__amount


class Projectile(Entity):
    def __init__(self, rect: Rectangle, damage: int, speed: float):
        super().__init__(rect)
        self.__damage = damage
        self.__speed = speed  # pixels moved right each frame

    @property
    def damage(self):
        return self.__damage

    def move(self):
        self.rect.move((self.__speed, 0))

    def hits(self, pest) -> bool:
        # A projectile hits a pest when its centre is inside the pest's rect
        return pest.rect.collide_point(self.rect.centre)
