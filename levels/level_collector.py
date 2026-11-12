from entities.living.pests.ant import Ant, ArmourAnt, HeavyArmourAnt

# Maps the pest ids used in the level data to the pest classes they spawn
pest_ids = {
    1: Ant,
    2: ArmourAnt,
    3: HeavyArmourAnt,
}


class LevelCollector():
    # Holds the level data. A level is a list of waves, in order.
    # Each wave maps a pest id (see PEST_TYPES) to how many of that pest spawn in the wave.
    def __init__(self):
        self.__levels = {
            1: self.level_1,
            2: self.level_2
        }

    def level_count(self) -> int:
        return len(self.__levels)

    def get_level(self, number: int) -> list[dict[int, int]] | None:
        if number not in self.__levels:
            return None
        return self.__levels[number]()

    def level_1(self) -> list[dict[int, int]]:
        return [
            {1: 1},  # first zombie
            {1: 10, 2: 3},  # early game
            {1: 5, 2: 10, 3: 1},  # harder midgame
            {1: 9, 2: 15, 3: 3},  # final round
        ]

    def level_2(self) -> list[dict[int, int]]:
        # Placeholder numbers: swap in the real level 2 data
        return [
            {1: 5},
            {1: 12, 2: 5},
            {1: 6, 2: 12, 3: 2},
            {1: 12, 2: 18, 3: 5},
        ]
