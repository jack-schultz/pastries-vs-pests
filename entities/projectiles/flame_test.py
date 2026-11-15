from entities.living.pests.ants.ant import Ant
from entities.projectiles.flame import Flame


def test_grows_then_burns_out(canvas):
    flame = Flame(canvas, 100, 100, 90)
    flame.move()
    assert flame.rect.w == 9 and not flame.is_expired()
    for _ in range(40):
        flame.move()
    assert flame.is_expired()


def test_burns_any_pest_along_its_body(canvas):
    flame = Flame(canvas, 100, 100, 90)
    for _ in range(10):
        flame.move()
    assert flame.touches(Ant(canvas, 150, 100))
