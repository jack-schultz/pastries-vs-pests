from __future__ import annotations
import random
from entities.living.pests.base_pest import BasePest


class WaveManager:
    """
    Runs a level's waves.
    First wave after start_delay, then one every wave_delay seconds.
    Pests from a wave trickle in one at a time, every spawn_interval seconds.
    The level is complete once every wave has arrived and the board is clear.
    """
    def __init__(self, waves: list[dict[int, int]], pest_types: dict[int, type[BasePest]]) -> None:
        self.__start_delay = 5.0  # seconds before the first wave
        self.__wave_delay = 8.0  # seconds from one wave's arrival to the next
        self.__spawn_interval = 1.0  # seconds between pests spawning

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
        self.__queue: list[type[BasePest]] = []  # pests that have arrived but not spawned yet
        self.__wave_number = 0  # how many waves have arrived
        self.__next_wave_at: float | None = None  # set on the first call to next_pest
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

        if self.__next_wave_at is None:
            self.__next_wave_at = now + self.__start_delay

        # A wave arrives on its timer, no matter what is still on the board
        if self.__wave_number < self.total_waves and now >= self.__next_wave_at:
            self.__wave_number += 1
            wave = list(self.__waves[self.__wave_number - 1])
            random.shuffle(wave)
            self.__queue.extend(wave)
            self.__next_wave_at = now + self.__wave_delay

        # Spawn the next queued pest once the spawn interval has passed
        if self.__queue and now >= self.__next_spawn_at:
            self.__next_spawn_at = now + self.__spawn_interval
            return self.__queue.pop(0)

        # Level is complete once every wave has arrived, spawned and been cleared
        if self.__wave_number >= self.total_waves and not self.__queue and pests_on_board == 0:
            self.__finished = True
        return None
