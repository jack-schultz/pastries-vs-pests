import pytest
from entities.garden import Garden
from entities.living.pests.ants.ant import Ant


@pytest.fixture
def garden(canvas):
    return Garden(canvas, 40, 120)


def test_is_a_grid_of_five_by_nine_tiles(garden):
    assert len(garden.tiles) == 45


def test_spawns_pests_on_the_right_edge(garden):
    pest = garden.spawn_pest(Ant, 900)
    assert pest.rect.left == 900 and garden.tile_blocking(pest) is None
