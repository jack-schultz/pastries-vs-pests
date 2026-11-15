from entities.living.goods.base_good import BaseGood
from entities.living.pests.ants.ant import Ant
from entities.living.pests.springtail import Springtail


def make_good(canvas, x=300):
    return BaseGood(canvas, x, 100, 80, 80, "yellow", 1000)


def walk_into(pest, good):
    # Move the pest so its front is just inside the good.
    pest.rect.move((good.rect.right - 5 - pest.rect.left, 0))
    assert pest.is_blocked_by(good)


def labels(canvas):
    return [canvas.itemcget(i, "text")
            for i in canvas.find_all() if canvas.type(i) == "text"]


# These tests cover construction.

def test_is_an_ant_with_no_armour(canvas):
    springtail = Springtail(canvas, 800, 100)
    assert isinstance(springtail, Ant)
    assert springtail.armour is None
    assert springtail.layer_count == 1


def test_has_less_health_than_an_ant(canvas):
    springtail = Springtail(canvas, 800, 100)
    assert springtail.max_health == 120
    assert springtail.health == 120


def test_is_faster_than_an_ant(canvas):
    springtail = Springtail(canvas, 800, 100)
    assert springtail.speed == 0.4
    assert springtail.speed > Ant(canvas, 800, 100).speed


def test_label_is_springtail(canvas):
    Springtail(canvas, 800, 100)
    assert "Springtail" in labels(canvas)


# These tests cover leaping.

def test_has_not_leapt_at_start(canvas):
    assert not Springtail(canvas, 800, 100).has_leapt


def test_leaps_over_first_good_without_damaging_it(canvas):
    good = make_good(canvas)
    springtail = Springtail(canvas, 800, 100)
    walk_into(springtail, good)

    springtail.attack(good)
    assert springtail.has_leapt
    assert good.health == 1000
    assert springtail.rect.right < good.rect.left
    assert not springtail.is_blocked_by(good)


def test_slows_to_ant_speed_after_leaping(canvas):
    good = make_good(canvas)
    springtail = Springtail(canvas, 800, 100)
    springtail.attack(good)
    assert springtail.speed == 0.25

    x_before = springtail.rect.left
    springtail.move()
    assert springtail.rect.left == x_before - 0.25


def test_only_leaps_once(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    first, second = make_good(canvas), make_good(canvas, x=150)
    springtail = Springtail(canvas, 800, 100)
    springtail.attack(first)  # The springtail leaps over the good.

    walk_into(springtail, second)
    x_before = springtail.rect.left
    springtail.attack(second)
    assert springtail.rect.left == x_before  # It cannot leap a second time.
    # It then bites like an ant.
    assert second.health == 1000 - springtail.damage
