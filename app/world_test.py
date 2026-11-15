import time
from types import SimpleNamespace
import pytest
from app.world import World
from entities.flour import Flour
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.goods.profiterole import Profiterole
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.pests.ants.ant import Ant
from entities.living.pests.pest_type import PestType
from entities.projectiles.sugar_cube import SugarCube
from levels.wave_manager import WaveManager


@pytest.fixture
def window(canvas):
    return SimpleNamespace(canvas=canvas, width=900, height=640)


@pytest.fixture
def world(window):
    return World(window)


def fast_forward(monkeypatch):
    # Jumps the clock so fuses, arming times and wave timers have all run out.
    later = time.monotonic() + 1000
    monkeypatch.setattr(time, "monotonic", lambda: later)


def test_unknown_level_falls_back_to_level_one(window):
    assert World(window, 99).level_number == 1


def test_last_level_has_no_next_level(window):
    last = World(window, 7)
    last.start_next_level()
    assert last.level_number == 7


def test_dropping_without_a_held_good_does_nothing(world):
    assert not world.drop_held(world.garden.tiles[0])


def test_wave_spawns_a_pest(world, monkeypatch):
    world._World__waves = WaveManager([{PestType.ANT: 1}])
    world.spawn_pest_if_due()
    fast_forward(monkeypatch)
    world.spawn_pest_if_due()
    assert len(world._World__pests) == 1


def test_finished_level_starts_the_next_one(world, canvas):
    world._World__waves = WaveManager([])
    world.tick()
    assert world.clicked_next_button((450, 335))

    tiles, pests = world.garden.tiles, world._World__pests
    for tile in tiles[:2]:
        tile.good = SugarShooter(canvas, *tile.rect.centre)
    world.pick_up(tiles[1])
    world.add_goods([Flour(canvas, 0, 0, 25), SugarCube(canvas, 0, 0)])
    pests.append(Ant(canvas, 500, 200))

    world.start_next_level()
    assert world.level_number == 2
    assert tiles[0].is_empty and not pests and not world.is_holding
    assert not world.clicked_next_button((450, 335))


def test_tick_resolves_combat(world, canvas, monkeypatch):
    tiles, pests = world.garden.tiles, world._World__pests
    for index, good in (
            (0, Profiterole), (10, SugarShooter), (20, PoppingCandy)):
        tiles[index].good = good(canvas, *tiles[index].rect.centre)
    tiles[10].good.take_damage(250)  # Leaves the shooter one bite from death.
    pests.extend(Ant(canvas, *tiles[i].rect.centre) for i in (0, 10, 20))
    pests.append(Ant(canvas, -100, 200))  # Already past the left edge.

    x, y = tiles[30].rect.centre
    weak_ant, cube = Ant(canvas, x + 30, y), SugarCube(canvas, x, y)
    weak_ant.take_damage(150)
    cube.piercing = 1
    pests.append(weak_ant)
    world.add_goods([cube, Flour(canvas, 0, 0, 25)])

    fast_forward(monkeypatch)
    world.tick()
    world.collect_flour_at((900, 640))
    assert world.game_over
    assert len(pests) == 1
    assert tiles[0].is_empty and tiles[10].is_empty and tiles[20].is_empty
