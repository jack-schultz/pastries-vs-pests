import time
from app.window import Window
from app.world import World
from entities.flour import Flour
from entities.living.goods.hardtack import Hardtack
from entities.living.goods.profiterole import Profiterole
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.pests.ants.ant import Ant
from entities.living.pests.ants.armour_ant import ArmourAnt


def run_tests() -> bool:
    """Run the pytest suite and return True when every test passed."""
    import pytest
    return pytest.main() == 0


def tick_until(world: World, condition, max_ticks: int = 1000) -> int:
    """Tick the world until the condition is met and return the ticks.

    Returns -1 if the condition is still not met after max_ticks.
    """
    for ticks in range(1, max_ticks + 1):
        world.tick()
        if condition():
            return ticks
    return -1


def report(description: str, passed: bool) -> None:
    """Print one integration check and whether it passed."""
    result = "PASS" if passed else "FAIL"
    print(f"  [{result}] {description}")


def run_integration_tests() -> None:
    """Run the game's objects together on a hidden window."""
    window = Window()
    window.root.withdraw()
    canvas = window.canvas

    print("======== Level loading =========")
    # LevelCollector raises KeyError for a missing level and World
    # handles it by falling back to level 1.
    world = World(window, 99)
    report("Unknown level 99 falls back to level 1",
           world.level_number == 1)
    report(f"Level 1 starts with {world.flour} flour", world.flour > 0)

    print("\n======== Placing and moving goods =========")
    first_tile, second_tile, empty_tile = world.garden.tiles[0:3]
    first_tile.good = Hardtack(canvas, *first_tile.rect.centre)
    second_tile.good = Hardtack(canvas, *second_tile.rect.centre)
    report("Glove picks up a Hardtack", world.pick_up(first_tile))
    # Tile raises ValueError when occupied and World catches it.
    report("Dropping onto an occupied tile is refused",
           not world.drop_held(second_tile))
    report("Dropping onto an empty tile succeeds",
           world.drop_held(empty_tile))
    report("The Hardtack moved to the empty tile",
           first_tile.is_empty and not empty_tile.is_empty)

    print("\n======== Sugar Shooter against an armoured pest =========")
    world = World(window, 1)
    # Tiles are stored column by column, so index 5 is column 1, row 0.
    shooter_tile = world.garden.tiles[5]
    # A zero delay makes the shooter fire every frame for this test.
    shooter_tile.good = SugarShooter(
        canvas, *shooter_tile.rect.centre, delay_pattern=(0.0,))
    _, row_y = shooter_tile.rect.centre
    armour_ant = ArmourAnt(canvas, 700, row_y)
    world.add_pest(armour_ant)
    chainmail = armour_ant.armour
    report(f"Armour Ant starts with {chainmail.durability} durability",
           not chainmail.is_broken)
    ticks = tick_until(world, lambda: chainmail.is_broken)
    report(f"Sugar cubes break the chainmail after {ticks} ticks",
           ticks > 0 and armour_ant.health == armour_ant.max_health)
    ticks = tick_until(world, lambda: armour_ant not in world.pests)
    report(f"The unarmoured ant dies {ticks} ticks later",
           ticks > 0 and armour_ant.is_dead)

    print("\n======== Profiterole explosion =========")
    world = World(window, 1)
    bombe_tile = world.garden.tiles[12]
    bombe_x, bombe_y = bombe_tile.rect.centre
    bombe_tile.good = Profiterole(canvas, bombe_x, bombe_y)
    nearby_ant = Ant(canvas, bombe_x + 60, bombe_y)
    distant_ant = Ant(canvas, bombe_x + 400, bombe_y)
    world.add_pest(nearby_ant)
    world.add_pest(distant_ant)
    world.tick()
    report("The Profiterole waits for its fuse",
           not bombe_tile.is_empty)
    # The fuse is measured in real seconds, so wait for it to burn.
    time.sleep(1.3)
    world.tick()
    report("The explosion kills the nearby ant",
           nearby_ant not in world.pests)
    report("The distant ant is out of range",
           distant_ant in world.pests and not distant_ant.is_dead)
    report("The Profiterole is used up", bombe_tile.is_empty)

    print("\n======== Collecting flour =========")
    world = World(window, 1)
    starting_flour = world.flour
    world.add_goods([Flour(canvas, 400, 400, 25)])
    world.collect_flour_at((400, 400))
    ticks = tick_until(world, lambda: world.flour > starting_flour)
    report(f"Flour reaches the counter after {ticks} ticks "
           f"({starting_flour} -> {world.flour})",
           world.flour == starting_flour + 25)

    print("\n======== Game over and next level =========")
    world = World(window, 1)
    world.add_pest(Ant(canvas, 0, 300))
    world.tick()
    report("A pest at the left edge ends the game", world.game_over)
    world.start_next_level()
    report("The next level is level 2", world.level_number == 2)
    report("The board is cleared for the next level", not world.pests)

    window.root.destroy()


if run_tests():
    run_integration_tests()
    Window().run()
