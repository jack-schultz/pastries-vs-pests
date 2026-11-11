from entities.living.pests.base_pest import BasePest


class Ant(BasePest):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(canvas, x, y, size=30, colour="#915831", health=160, speed=0.25)


class ArmourAnt(BasePest):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(canvas, x, y, size=40, colour="#7a4a2b", health=240, speed=0.20)


class HeavyArmourAnt(BasePest):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(canvas, x, y, size=50, colour="#663718", health=450, speed=0.10)
