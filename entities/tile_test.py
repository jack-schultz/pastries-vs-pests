import pytest
from entities.living.goods.hardtack import Hardtack
from entities.tile import Tile


def test_holds_one_good_until_cleared(canvas):
    tile = Tile(canvas, 0, 0, 90, "#ffffff")
    tile.good = Hardtack(canvas, 0, 0)
    with pytest.raises(ValueError):
        tile.good = Hardtack(canvas, 0, 0)
    tile.clear_good()
    assert tile.is_empty


def test_rejects_things_that_are_not_goods(canvas):
    with pytest.raises(ValueError):
        Tile(canvas, 0, 0, 90, "#ffffff").good = "not a good"
