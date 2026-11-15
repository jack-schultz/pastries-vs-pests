from entities.living.pests.pest_type import PestType
from levels.wave_manager import WaveManager


def test_no_pest_spawns_before_the_start_delay():
    waves = WaveManager([{PestType.ANT: 1}])
    assert waves.next_pest(0, 0) is None
    assert waves.total_waves == 1 and not waves.finished
