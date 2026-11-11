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
        pass

    def level_1(self) -> list[dict[int, int]]:
        return [
            {1: 1},  # first zombie
            {1: 10, 2: 3},  # early game
            {1: 5, 2: 10, 3: 1},  # harder midgame
            {1: 9, 2: 15, 3: 3},  # final round
        ]
