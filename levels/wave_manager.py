from __future__ import annotations
import random
from entities.living.pests.base_pest import BasePest


class WaveManager:
    """
    Runs a level's waves. Each wave's pests spawn one at a time
    The next wave starts once the board is clear and the break between waves is over.
    """
    def __init__(self, waves: list[dict[int, int]], pest_types: dict[int, type[BasePest]]) -> None:
        self.start_delay = 5.0
        self.wave_delay = 8.0
        self.spawn_interval = 1.0

        # For each wave, create a flat list with one entry per pest to spawn.
        self.__waves = [
            # Inside a wave: turn each pest id and count into that many pest classes.
            # {1: 2, 2: 1} -> [Ant, Ant, ArmourAnt]
            [
                pest_types[pest_id]  # look up the pest class for this id
                for pest_id, count in wave.items()  # each pest id and how many to spawn
                for _ in range(count)  # repeat it count times
            ]
            for wave in waves  # do this for every wave in the level
        ]
        self.__queue: list[type[BasePest]] = []  # pests still to spawn in the current wave
        self.__wave_number = 0  # how many waves have started
        self.__break_ends_at: float | None = None  # set once the board clears
        self.__next_spawn_at = 0.0
        self.__finished = False

    @property
    def wave_number(self) -> int:
        return self.__wave_number

    @property
    def total_waves(self) -> int:
        return len(self.__waves)

    @property
    def finished(self) -> bool:
        return self.__finished

    def next_pest(self, now: float, pests_on_board: int) -> type[BasePest] | None:
        # Returns the pest class to spawn right now, or None if nothing spawns this tick
        if self.__finished:
            return None

        if self.__queue:
            if now < self.__next_spawn_at:
                return None
            self.__next_spawn_at = now + self.spawn_interval
            return self.__queue.pop(0)

        if pests_on_board > 0:
            return None

        # Board is clear. Last wave cleared means the level is complete
        if self.__wave_number >= self.total_waves:
            self.__finished = True
            return None

        if self.__break_ends_at is None:
            self.__break_ends_at = now + (self.wave_delay if self.__wave_number else self.start_delay)
        if now < self.__break_ends_at:
            return None

        # Start the next wave
        self.__break_ends_at = None
        self.__wave_number += 1
        self.__queue = list(self.__waves[self.__wave_number - 1])
        random.shuffle(self.__queue)
        self.__next_spawn_at = now + self.spawn_interval
        return self.__queue.pop(0)
