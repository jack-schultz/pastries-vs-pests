from entities.flour import Flour
from entities.living.goods.flour_flower import FlourFlower


def test_makes_no_flour_straight_away(canvas):
    assert FlourFlower(canvas, 100, 100).act(canvas) is None


def test_makes_flour_once_its_timer_runs_out(canvas, fast_forward):
    flower = FlourFlower(canvas, 100, 100)
    fast_forward()
    flour = flower.act(canvas)
    assert isinstance(flour, Flour) and flour.amount == 25
