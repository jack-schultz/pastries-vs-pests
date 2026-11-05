

# Hmm, still need to think about how i want the enemies to be stored and how they are spawned
class LevelCollector():
    def __init__(self):
        pass

    def level_1(self):
        return {
            1: {
                1: {
                    1: {  # first zombie
                        1: 1,
                    },
                },
                2: {  # Early game
                    1: 10,
                    2: 3,
                },
            },
            2: {  # harder midgame
                1: 5,
                2: 10,
                3: 1,
            },
            3: {  # Final round
                1: 9,
                2: 15,
                3: 3,
            },
        },
