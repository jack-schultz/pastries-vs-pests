import pytest
from entities.living.goods.base_good import BaseGood
from entities.living.living import Living


# These tests cover construction.

def test_is_a_living(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert isinstance(good, Living)


def test_starts_at_full_health(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert good.health == 10
    assert good.max_health == 10
    assert not good.is_dead


def test_has_no_armour(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert good.armour is None


def test_is_centred_on_given_point(canvas):
    # Unlike other entities, x and y are the centre, not the top left.
    good = BaseGood(canvas, 100, 200, 40, 60, "red", 10)
    assert good.rect.centre == (100, 200)


def test_keeps_its_size(canvas):
    good = BaseGood(canvas, 100, 200, 40, 60, "red", 10)
    assert good.rect.w == 40
    assert good.rect.h == 60


def test_is_drawn_on_canvas(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert good.canvas is canvas
    assert len(canvas.find_all()) == 1


# These tests cover taking damage.

def test_take_damage_lowers_health(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    good.take_damage(3)
    assert good.health == 7
    assert good.max_health == 10


def test_dies_when_health_reaches_zero(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    good.take_damage(10)
    assert good.is_dead


def test_negative_damage_raises(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    with pytest.raises(ValueError):
        good.take_damage(-5)
    assert good.health == 10


def test_destroy_removes_from_canvas(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    good.destroy()
    assert canvas.find_all() == ()


# These tests cover the action timer.

def test_not_ready_straight_away(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert not good._ready(1.0)


def test_ready_with_zero_interval(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert good._ready(0)


def test_ready_after_interval_passes(canvas, monkeypatch):
    # Fake clock so tests can run instantly.
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)

    now[0] += 0.5
    assert not good._ready(1.0)
    now[0] += 0.5
    assert good._ready(1.0)


def test_ready_restarts_timer(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)

    now[0] += 1.0
    assert good._ready(1.0)
    # Same moment, so the timer has just restarted.
    assert not good._ready(1.0)
    now[0] += 1.0
    assert good._ready(1.0)


def test_not_ready_does_not_restart_timer(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)

    now[0] += 0.6
    assert not good._ready(1.0)
    now[0] += 0.6
    assert good._ready(1.0)


# These tests cover acting.

def test_act_does_nothing_by_default(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert good.act(canvas) is None
    assert good.act(canvas, []) is None


# These tests cover stunning.

def test_can_act_when_not_stunned(canvas):
    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    assert not good.is_stunned
    assert good.can_act()


def test_stun_stops_acting_until_it_wears_off(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    good.stun(3.0)
    assert good.is_stunned
    assert not good.can_act()
    now[0] += 2.9
    assert not good.can_act()
    now[0] += 0.2
    assert good.can_act()


def test_shorter_stun_does_not_cut_a_longer_one(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])

    good = BaseGood(canvas, 100, 100, 40, 40, "red", 10)
    good.stun(5.0)
    good.stun(1.0)
    now[0] += 2.0
    assert good.is_stunned
