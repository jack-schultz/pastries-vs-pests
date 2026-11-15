from armour.helmet import Helmet
from entities.living.goods.base_good import BaseGood
from entities.living.pests.base_pest import BasePest
from entities.living.pests.rhino_beetle import RhinoBeetle
from entities.projectiles.sugar_cube import SugarCube


def make_good(canvas, x=300):
    return BaseGood(canvas, x, 100, 80, 80, "yellow", 5000)


def labels(canvas):
    return [canvas.itemcget(i, "text")
            for i in canvas.find_all() if canvas.type(i) == "text"]


# Construction

def test_is_a_pest_wearing_a_helmet(canvas):
    beetle = RhinoBeetle(canvas, 800, 100)
    assert isinstance(beetle, BasePest)
    assert isinstance(beetle.armour, Helmet)
    assert beetle.layer_count == 3  # two of its own plus the helmet


def test_charges_in_fast(canvas):
    beetle = RhinoBeetle(canvas, 800, 100)
    assert beetle.speed == 0.9
    assert not beetle.has_rammed


def test_label_is_rhino_beetle(canvas):
    RhinoBeetle(canvas, 800, 100)
    assert "Rhino Beetle" in labels(canvas)


def test_helmet_does_not_block_hits_from_the_front(canvas):
    # The helmet only covers above, so sugar cubes hit it full on
    beetle = RhinoBeetle(canvas, 800, 100)
    cube = SugarCube(canvas, 100, 100)
    beetle.take_damage(cube.damage_to_deal())
    assert beetle.health == beetle.max_health - cube.damage


# Ramming

def test_first_hit_is_a_big_headbutt_then_slows(canvas):
    beetle = RhinoBeetle(canvas, 800, 100)
    good = make_good(canvas)
    beetle.attack(good)
    assert beetle.has_rammed
    assert good.health == 5000 - 450
    assert beetle.speed == 0.2


def test_later_hits_are_weak(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    beetle = RhinoBeetle(canvas, 800, 100)
    good = make_good(canvas)
    beetle.attack(good)
    now[0] += beetle.attack_interval
    beetle.attack(good)
    assert good.health == 5000 - 450 - 40


def test_only_one_charge_per_life(canvas, monkeypatch):
    # A new good after the first doesn't get a second headbutt
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    beetle = RhinoBeetle(canvas, 800, 100)
    first, second = make_good(canvas), make_good(canvas, x=150)
    beetle.attack(first)
    now[0] += beetle.attack_interval
    beetle.attack(second)
    assert second.health == 5000 - 40
    assert beetle.speed == 0.2


def test_headbutt_respects_attack_interval(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    beetle = RhinoBeetle(canvas, 800, 100)
    good = make_good(canvas)
    beetle.attack(good)
    beetle.attack(good)  # same moment, so ignored
    assert good.health == 5000 - 450
