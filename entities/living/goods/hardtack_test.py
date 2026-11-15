from entities.living.goods.hardtack import Hardtack


def test_is_very_tough_and_does_nothing(canvas):
    hardtack = Hardtack(canvas, 100, 100)
    assert hardtack.health == 5000 and hardtack.act(canvas) is None
