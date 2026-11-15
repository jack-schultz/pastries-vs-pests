from entities.living.pests.ants.ant import Ant
from entities.projectiles.projectile import Projectile


def test_moves_right_by_its_speed(canvas):
    projectile = Projectile(canvas, 100, 100, 10, "#ffffff", 5, 4, 2)
    left = projectile.rect.left
    projectile.move()
    assert projectile.rect.left == left + 4


def test_hits_a_pest_once(canvas):
    projectile = Projectile(canvas, 100, 100, 10, "#ffffff", 5, 4, 2)
    x, y = projectile.rect.centre_right
    pest = Ant(canvas, x - 5, y)
    assert projectile.hits(pest)
    projectile.add_hit_pest(pest)
    assert not projectile.hits(pest)
