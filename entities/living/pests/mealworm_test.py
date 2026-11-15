from armour.chainmail import Chainmail
from entities.living.goods.base_good import BaseGood
from entities.living.pests.base_pest import BasePest
from entities.living.pests.mealworm import Mealworm


def make_good(canvas, health=5000, x=300):
    return BaseGood(canvas, x, 100, 80, 80, "yellow", health)


def bite(mealworm, good, now):
    # Step past the attack interval, then attack.
    now[0] += mealworm.attack_interval
    mealworm.attack(good)


# These tests cover construction.

def test_is_a_pest_wearing_chainmail(canvas):
    mealworm = Mealworm(canvas, 800, 100)
    assert isinstance(mealworm, BasePest)
    assert isinstance(mealworm.armour, Chainmail)
    assert mealworm.layer_count == 2  # its own layer plus the chainmail


def test_is_slow(canvas):
    assert Mealworm(canvas, 800, 100).speed == 0.22


def test_first_bite_is_small(canvas):
    mealworm = Mealworm(canvas, 800, 100)
    assert mealworm.bite == 40
    good = make_good(canvas)
    mealworm.attack(good)
    assert good.health == 5000 - 40


# These tests cover the bite ramping up.

def test_bites_get_harder_on_same_good(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    mealworm = Mealworm(canvas, 800, 100)
    good = make_good(canvas)

    for _ in range(3):
        bite(mealworm, good, now)
    assert good.health == 5000 - (40 + 65 + 90)


def test_bite_is_capped(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    mealworm = Mealworm(canvas, 800, 100)
    good = make_good(canvas, health=100000)
    for _ in range(20):
        bite(mealworm, good, now)
    assert mealworm.bite == 200


def test_new_good_resets_bite(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    mealworm = Mealworm(canvas, 800, 100)
    first, second = make_good(canvas), make_good(canvas, x=150)
    for _ in range(4):
        bite(mealworm, first, now)
    bite(mealworm, second, now)
    assert mealworm.bite == 40
    assert second.health == 5000 - 40


def test_does_not_bite_faster_than_attack_interval(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    mealworm = Mealworm(canvas, 800, 100)
    good = make_good(canvas)
    mealworm.attack(good)
    # the second attack is at the same moment, so it is ignored.
    mealworm.attack(good)
    assert good.health == 5000 - 40
    assert mealworm.bite == 40
