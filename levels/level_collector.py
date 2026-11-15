from entities.living.pests.pest_type import PestType

default_flour = 75  # flour the player starts a level with
dev_level_id = 0  # hidden testing level, not counted in level_count


class LevelCollector():
    """Holds the level data. A level is a list of waves, in order."""

    def __init__(self):
        self.__levels = {
            1: self.level_1,
            2: self.level_2,
            3: self.level_3,
            4: self.level_4,
            5: self.level_5,
            6: self.level_6,
            7: self.level_7,
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

    def get_level(self, number: int) -> list[dict[PestType, int]]:
        if number in self.__dev_levels:
            return self.__dev_levels[number]()
        if number not in self.__levels:
            raise KeyError(f"There is no level {number}")
        return self.__levels[number]()

    def starting_flour(self, number: int) -> int:
        return self.__starting_flour.get(number, default_flour)

    def dev_level(self) -> list[dict[PestType, int]]:
        return [
            {PestType.SPRINGTAIL: 2, PestType.MEALWORM: 1, PestType.RHINO_BEETLE: 1,
                PestType.STINKBUG: 1},  # one of every new pest first
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 2, PestType.SPRINGTAIL: 2},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 4, PestType.MEALWORM: 2},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 5,
                PestType.HEAVY_ARMOUR_ANT: 2, PestType.RHINO_BEETLE: 2},
            {PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 2, PestType.STINKBUG: 2},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 6,
                PestType.HEAVY_ARMOUR_ANT: 3, PestType.SPRINGTAIL: 3},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 4,
                PestType.MEALWORM: 2, PestType.RHINO_BEETLE: 2},
            {PestType.ARMOUR_ANT: 10, PestType.HEAVY_ARMOUR_ANT: 4, PestType.STINKBUG: 3},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 5,
                PestType.SPRINGTAIL: 4, PestType.RHINO_BEETLE: 3},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 10, PestType.HEAVY_ARMOUR_ANT: 6,
                PestType.MEALWORM: 3, PestType.STINKBUG: 3},
            {PestType.ANT: 10, PestType.ARMOUR_ANT: 12, PestType.HEAVY_ARMOUR_ANT: 10, PestType.SPRINGTAIL: 5,
                PestType.MEALWORM: 4, PestType.RHINO_BEETLE: 4, PestType.STINKBUG: 4},  # finale
        ]

    def level_1(self) -> list[dict[PestType, int]]:
        # Tutorial: plain ants only
        return [
            {PestType.ANT: 1},
            {PestType.ANT: 2},
            {PestType.ANT: 3},
            {PestType.ANT: 4},
            {PestType.ANT: 5},
            {PestType.ANT: 8},  # finale
        ]

    def level_2(self) -> list[dict[PestType, int]]:
        # Armour Ants arrive
        return [
            {PestType.ANT: 2},
            {PestType.ANT: 3},
            {PestType.ANT: 3, PestType.ARMOUR_ANT: 1},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 2},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 3},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 3},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 5},  # finale
        ]

    def level_3(self) -> list[dict[PestType, int]]:
        # First Heavy Armour Ants
        return [
            {PestType.ANT: 1},
            {PestType.ANT: 4},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 1},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 2},
            {PestType.ANT: 3, PestType.ARMOUR_ANT: 4},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 4},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 5, PestType.HEAVY_ARMOUR_ANT: 1},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 5},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 7,
                PestType.HEAVY_ARMOUR_ANT: 2},  # finale
        ]

    def level_4(self) -> list[dict[PestType, int]]:
        # Armour become common
        return [
            {PestType.ANT: 2},
            {PestType.ANT: 5},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 2},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 4},
            {PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 1},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 4, PestType.HEAVY_ARMOUR_ANT: 1},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 2},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 2},
            {PestType.ANT: 8, PestType.ARMOUR_ANT: 8,
                PestType.HEAVY_ARMOUR_ANT: 4},  # finale
        ]

    def level_5(self) -> list[dict[PestType, int]]:
        # long level with constant pressure
        return [
            {PestType.ANT: 2},
            {PestType.ANT: 5},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 1},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 3},
            {PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 1},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 5, PestType.HEAVY_ARMOUR_ANT: 1},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 2},
            {PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 3},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 3},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 4},
            {PestType.ANT: 8, PestType.ARMOUR_ANT: 10,
                PestType.HEAVY_ARMOUR_ANT: 6},  # finale
        ]

    def level_6(self) -> list[dict[PestType, int]]:
        # very hard level, with a big opening and a huge last wave
        return [
            {PestType.ANT: 2},
            {PestType.ANT: 5},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 2},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 4},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 5, PestType.HEAVY_ARMOUR_ANT: 2},
            {PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 2},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 3},
            {PestType.ANT: 4, PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 4},
            {PestType.ARMOUR_ANT: 10, PestType.HEAVY_ARMOUR_ANT: 4},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 8, PestType.HEAVY_ARMOUR_ANT: 5},
            {PestType.ANT: 5, PestType.ARMOUR_ANT: 10, PestType.HEAVY_ARMOUR_ANT: 6},
            {PestType.ANT: 10, PestType.ARMOUR_ANT: 12,
                PestType.HEAVY_ARMOUR_ANT: 10},  # finale
        ]

    def level_7(self) -> list[dict[PestType, int]]:
        # Bug infestation: each new pest is brought in one at a time, then they all come at once
        return [
            {PestType.ANT: 2},
            {PestType.ANT: 5},
            {PestType.ANT: 3, PestType.SPRINGTAIL: 1},  # first Springtail
            {PestType.ANT: 3, PestType.SPRINGTAIL: 3},
            {PestType.ANT: 3, PestType.ARMOUR_ANT: 2,
                PestType.MEALWORM: 1},  # first Mealworm
            {PestType.ARMOUR_ANT: 3, PestType.SPRINGTAIL: 2, PestType.MEALWORM: 2},
            {PestType.ANT: 4, PestType.RHINO_BEETLE: 2},  # first Rhino Beetles
            {PestType.ARMOUR_ANT: 3, PestType.SPRINGTAIL: 3, PestType.RHINO_BEETLE: 3},
            {PestType.ANT: 3, PestType.ARMOUR_ANT: 3,
                PestType.STINKBUG: 2},  # first Stinkbugs
            {PestType.HEAVY_ARMOUR_ANT: 2, PestType.MEALWORM: 2, PestType.STINKBUG: 3},
            {PestType.ARMOUR_ANT: 4, PestType.SPRINGTAIL: 4,
                PestType.RHINO_BEETLE: 3, PestType.STINKBUG: 3},
            {PestType.ANT: 6, PestType.ARMOUR_ANT: 6, PestType.HEAVY_ARMOUR_ANT: 4, PestType.SPRINGTAIL: 5,
                PestType.MEALWORM: 4, PestType.RHINO_BEETLE: 4, PestType.STINKBUG: 4},  # finale
        ]
