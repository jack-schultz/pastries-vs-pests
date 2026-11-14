from entities.living.pests.ant import Ant
from entities.living.pests.armour_ant import ArmourAnt
from entities.living.pests.heavy_armour_ant import HeavyArmourAnt

# Maps the pest ids used in the level data to the pest classes they spawn
pest_ids = {
    1: Ant,
    2: ArmourAnt,
    3: HeavyArmourAnt,
}

default_flour = 75  # flour the player starts a level with
dev_level_id = 0  # hidden testing level, not counted in level_count


class LevelCollector():
    # Holds the level data. A level is a list of waves, in order.
    def __init__(self):
        self.__levels = {
            1: self.level_1,
            2: self.level_2,
            3: self.level_3,
            4: self.level_4,
            5: self.level_5,
            6: self.level_6,
        }
        # Extra levels for dev
        self.__dev_levels = {
            dev_level_id: self.dev_level,
        }
        # Levels that start with something other than default_flour
        self.__starting_flour = {
            dev_level_id: 9000,
        }

    def level_count(self) -> int:
        return len(self.__levels)

    def get_level(self, number: int) -> list[dict[int, int]]:
        if number in self.__dev_levels:
            return self.__dev_levels[number]()
        if number not in self.__levels:
            raise KeyError(f"There is no level {number}")
        return self.__levels[number]()

    def starting_flour(self, number: int) -> int:
        return self.__starting_flour.get(number, default_flour)

    def dev_level(self) -> list[dict[int, int]]:
        return [
            {1: 5, 2: 2},
            {1: 5, 2: 4},
            {1: 4, 2: 5, 3: 2},
            {2: 8, 3: 2},
            {1: 6, 2: 6, 3: 3},
            {1: 4, 2: 8, 3: 4},
            {2: 10, 3: 4},
            {1: 6, 2: 8, 3: 5},
            {1: 5, 2: 10, 3: 6},
            {1: 10, 2: 12, 3: 10},  # finale
        ]

    def level_1(self) -> list[dict[int, int]]:
        # Tutorial: plain ants only
        return [
            {1: 1},
            {1: 2},
            {1: 3},
            {1: 4},
            {1: 5},
            {1: 8},  # finale
        ]

    def level_2(self) -> list[dict[int, int]]:
        # Armour Ants arrive
        return [
            {1: 2},
            {1: 3},
            {1: 3, 2: 1},
            {1: 4, 2: 2},
            {1: 4, 2: 3},
            {1: 5, 2: 3},
            {1: 6, 2: 5},  # finale
        ]

    def level_3(self) -> list[dict[int, int]]:
        # First Heavy Armour Ants
        return [
            {1: 3},
            {1: 4, 2: 1},
            {1: 4, 2: 2},
            {1: 3, 2: 4},
            {1: 4, 2: 4},
            {1: 4, 2: 5, 3: 1},
            {1: 5, 2: 5},
            {1: 6, 2: 7, 3: 2},  # finale
        ]

    def level_4(self) -> list[dict[int, int]]:
        # Heavies become common
        return [
            {1: 4},
            {1: 5, 2: 2},
            {1: 4, 2: 4},
            {2: 6, 3: 1},
            {1: 6, 2: 4, 3: 1},
            {1: 4, 2: 6, 3: 2},
            {1: 6, 2: 6, 3: 2},
            {1: 8, 2: 8, 3: 4},  # finale
        ]

    def level_5(self) -> list[dict[int, int]]:
        # Siege: long level with heavy pressure
        return [
            {1: 4, 2: 1},
            {1: 4, 2: 3},
            {2: 6, 3: 1},
            {1: 5, 2: 5, 3: 1},
            {1: 4, 2: 6, 3: 2},
            {2: 8, 3: 3},
            {1: 6, 2: 6, 3: 3},
            {1: 4, 2: 8, 3: 4},
            {1: 8, 2: 10, 3: 6},  # finale
        ]

    def level_6(self) -> list[dict[int, int]]:
        # Finale: the hardest level, with a big opening and a huge last wave
        return [
            {1: 5, 2: 2},
            {1: 5, 2: 4},
            {1: 4, 2: 5, 3: 2},
            {2: 8, 3: 2},
            {1: 6, 2: 6, 3: 3},
            {1: 4, 2: 8, 3: 4},
            {2: 10, 3: 4},
            {1: 6, 2: 8, 3: 5},
            {1: 5, 2: 10, 3: 6},
            {1: 10, 2: 12, 3: 10},  # finale
        ]
