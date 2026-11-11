import tkinter as tk
import pytest
from entities.card import Card
from entities.flour import Flour
from entities.garden import Garden
from entities.living.good import FlourFlower, SugarShooter
from entities.cardholder import CardHolder
from app.world import World
from entities.living.pest import Ant
from entities.projectile import Projectile
from app.rectangle import Rectangle
from entities.tile import Tile
from entities.entity import Living


@pytest.fixture
def canvas():
    root = tk.Tk()
    root.withdraw()
    canvas = tk.Canvas(root, width=900, height=600)
    canvas.pack()
    yield canvas
    root.destroy()


@pytest.fixture
def world(window):
    return World(window)


def make_flower(canvas, x=100, y=100):
    return FlourFlower(canvas, x, y, 70, 70)


# ===== Rectangle =====
def test_rectangle_geometry_and_move(canvas):
    rect = Rectangle(canvas, 10, 20, 30, 40, "#000000")
    assert (rect.x, rect.y, rect.w, rect.h) == (10, 20, 30, 40)
    assert rect.centre == (25, 40)
    rect.move((5, 5))
    assert (rect.x, rect.y) == (15, 25)


def test_rectangle_collide_point(canvas):
    rect = Rectangle(canvas, 10, 20, 30, 40, "#000000")
    assert rect.collide_point((20, 30))
    assert not rect.collide_point((0, 0))


# ===== Living =====
def test_living_takes_damage_and_dies(canvas):
    living = Living(canvas, 0, 0, 10, 10, "#000000", health=20)
    living.take_damage(5)
    assert living.health == 15
    assert not living.is_dead
    living.take_damage(20)
    assert living.is_dead


# ===== Tile =====
def test_tile_accepts_only_one_good(canvas):
    tile = Tile(canvas, 0, 0, 90, "#ffffff")
    assert tile.is_empty
    first = make_flower(canvas)
    tile.good = first
    tile.good = SugarShooter(canvas, 0, 0, 70, 70)
    assert tile.good is first


def test_tile_rejects_non_good(canvas):
    tile = Tile(canvas, 0, 0, 90, "#ffffff")
    tile.good = "not a good"
    assert tile.is_empty


def test_tile_clear_good(canvas):
    tile = Tile(canvas, 0, 0, 90, "#ffffff")
    tile.good = make_flower(canvas)
    tile.clear_good()
    assert tile.is_empty


# ===== Flour =====
def test_flour_collect_returns_amount(canvas):
    flour = Flour(canvas, 100, 100, amount=25)
    assert flour.amount == 25
    assert flour.collect() == 25


# ===== Card =====
def test_card_properties_and_create_good(canvas):
    card = Card(canvas, 0, 0, 70, 85, name="The Flour Flower", cost=50, good_class=FlourFlower)
    assert card.name == "The Flour Flower"
    assert card.cost == 50
    assert isinstance(card.create_good(canvas, 0, 0, 70, 70), FlourFlower)


# ===== Goods =====
def test_flour_flower_waits_then_makes_flour(canvas):
    flower = make_flower(canvas)
    assert flower.act(canvas) is None
    flower._Good__last_action = -1000.0
    flour = flower.act(canvas)
    assert isinstance(flour, Flour)
    assert flour.amount == 25
    # Timer restarts after producing
    assert flower.act(canvas) is None


def test_sugar_shooter_waits_then_fires(canvas):
    shooter = SugarShooter(canvas, 100, 100, 70, 70)
    assert shooter.act(canvas) is None
    shooter._Good__last_action = -1000.0
    shot = shooter.act(canvas)
    assert isinstance(shot, Projectile)
    assert shot.damage == 20


# ===== Pests =====
def test_ant_stats_and_movement(canvas):
    ant = Ant(canvas, 800, 100)
    assert ant.health == 200
    ant.move()
    assert ant.rect.x == 800 - ant.speed


def test_ant_screen_bounds(canvas):
    assert Ant(canvas, -100, 0).has_left_screen()
    assert not Ant(canvas, 800, 0).has_left_screen()


def test_ant_blocked_by_good(canvas):
    blocker = make_flower(canvas)
    assert Ant(canvas, 150, 110).is_blocked_by(blocker)
    assert not Ant(canvas, 300, 110).is_blocked_by(blocker)


def test_ant_attack_respects_interval(canvas):
    victim = make_flower(canvas)
    ant = Ant(canvas, 150, 110)
    ant._Pest__last_attack = -1000.0
    ant.attack(victim)
    ant.attack(victim)
    assert victim.health == 300 - 100


# ===== Projectile =====
def test_projectile_moves_right(canvas):
    shot = Projectile(canvas, 200, 200, size=14, colour="#ff8fab", damage=10, speed=6)
    start = shot.rect.x
    shot.move()
    assert shot.rect.x == start + 6


def test_projectile_hits(canvas):
    shot = Projectile(canvas, 200, 200, size=14, colour="#ff8fab", damage=10, speed=6)
    assert shot.hits(Ant(canvas, 210, 180))
    assert not shot.hits(Ant(canvas, 600, 0))


# ===== Garden / Inventory =====
def test_garden_tiles_start_empty(canvas):
    garden = Garden(canvas, 40, 120)
    assert len(garden.tiles) == garden.rows * garden.columns
    assert all(t.is_empty for t in garden.tiles)


def test_garden_spawn_ant_off_right_edge_in_a_row(canvas):
    garden = Garden(canvas, 40, 120)
    ant = garden.spawn_ant(900)
    assert ant.rect.x == 900
    assert 120 <= ant.rect.y < 120 + garden.rows * garden.grid_size


def test_garden_tile_blocking(canvas):
    garden = Garden(canvas, 40, 120)
    garden.tiles[0].good = make_flower(canvas, 50, 130)
    assert garden.tile_blocking(Ant(canvas, 110, 140)) is garden.tiles[0]
    assert garden.tile_blocking(Ant(canvas, 500, 500)) is None


def test_garden_goods_act_collects_products(canvas):
    garden = Garden(canvas, 40, 120)
    flower = make_flower(canvas, 50, 130)
    flower._Good__last_action = -1000.0
    garden.tiles[0].good = flower
    results = garden.goods_act()
    assert sum(isinstance(r, Flour) for r in results) == 1


def test_inventory_cards_match_attributes(canvas):
    inventory = CardHolder(canvas, 120, 20)
    assert [c.name for c in inventory.cards] == [a[0] for a in inventory.card_attributes]
    assert len(inventory.cards) == inventory.cards_count


# ===== World =====
def test_world_starts_empty(world):
    assert not (world.pests or world.flours or world.projectiles)


def test_world_update_flour_count(world):
    world.update_flour_count(123)
    assert world.canvas.itemcget(world.flour_text, "text") == "123"


def test_world_add_goods_routes_by_type(world, canvas):
    flour = Flour(canvas, 0, 0, 10)
    shot = Projectile(canvas, 0, 0, 14, "#fff", 10, 6)
    world.add_goods([flour, shot, None])
    assert world.flours == [flour]
    assert world.projectiles == [shot]


def test_world_spawn_ant_only_when_due(world):
    world.spawn_pest_if_due()
    assert world.pests == []
    world.last_ant_spawn -= world.ant_spawn_interval
    world.spawn_pest_if_due()
    assert len(world.pests) == 1


def test_world_pest_walks_when_unblocked(world, canvas):
    ant = Ant(canvas, 800, 140)
    world.pests.append(ant)
    world.update_pests()
    assert ant.rect.x == 800 - ant.speed


def test_world_pest_attacks_and_kills_good(world, canvas):
    tile = world.garden.tiles[0]
    flower = make_flower(canvas, tile.rect.x + 10, tile.rect.y + 10)
    tile.good = flower
    ant = Ant(canvas, flower.rect.x + 20, flower.rect.centre[1] - 25)
    ant._Pest__last_attack = -1000.0
    world.pests.append(ant)
    start_x = ant.rect.x

    world.update_pests()
    assert ant.rect.x == start_x  # blocked, did not move
    assert flower.health == 200

    flower.take_damage(flower.health)
    ant._Pest__last_attack = -1000.0
    world.update_pests()
    assert tile.is_empty


def test_world_removes_pest_that_left_screen(world, canvas):
    world.pests.append(Ant(canvas, -100, 140))
    world.update_pests()
    assert world.pests == []


def test_world_projectile_damages_pest(world, canvas):
    ant = Ant(canvas, 300, 100)
    shot = Projectile(canvas, 320, 120, 14, "#fff", damage=20, speed=0)
    world.pests.append(ant)
    world.projectiles.append(shot)
    world.update_projectiles()
    assert ant.health == 180
    assert world.projectiles == [shot]  # survives until the pest dies


def test_world_projectile_kills_pest_and_is_removed(world, canvas):
    ant = Ant(canvas, 300, 100)
    ant.take_damage(190)
    shot = Projectile(canvas, 320, 120, 14, "#fff", damage=20, speed=0)
    world.pests.append(ant)
    world.projectiles.append(shot)
    world.update_projectiles()
    assert world.pests == []
    assert world.projectiles == []


def test_world_projectile_removed_off_screen(world, canvas):
    shot = Projectile(canvas, 899, 300, 14, "#fff", damage=20, speed=6)
    world.projectiles.append(shot)
    world.update_projectiles()
    assert world.projectiles == []


def test_world_collect_flour_at(world, canvas):
    near = Flour(canvas, 100, 100, 25)
    far = Flour(canvas, 500, 500, 25)
    world.flours.extend([near, far])
    assert world.collect_flour_at((100, 100)) == 25
    assert world.flours == [far]
    assert world.collect_flour_at((0, 0)) == 0
