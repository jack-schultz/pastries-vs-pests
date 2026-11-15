import pytest
from levels.level_collector import LevelCollector


def test_unknown_level_raises_a_key_error():
    with pytest.raises(KeyError):
        LevelCollector().get_level(99)
