from entities.projectiles.sugar_cube import SugarCube


def test_has_the_sugar_cube_stats(canvas):
    cube = SugarCube(canvas, 100, 100)
    assert (cube.damage, cube.piercing) == (22, 2)


def test_never_expires_on_its_own(canvas):
    assert not SugarCube(canvas, 100, 100).is_expired()
