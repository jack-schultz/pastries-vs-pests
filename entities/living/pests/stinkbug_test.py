from armour.shield import Shield
from entities.damage import Damage
from entities.damage_type import DamageType
from entities.direction import Direction
from entities.living.goods.base_good import BaseGood
from entities.living.pests.ants.ant import Ant
from entities.living.pests.stinkbug import Stinkbug
from entities.projectiles.sugar_cube import SugarCube


def make_good(canvas):
    return BaseGood(canvas, 300, 100, 80, 80, "yellow", 1000)


def labels(canvas):
    return [canvas.itemcget(i, "text") for i in canvas.find_all() if canvas.type(i) == "text"]


# Construction

def test_is_an_ant_with_a_shield(canvas):
    stinkbug = Stinkbug(canvas, 800, 100)
    assert isinstance(stinkbug, Ant)
    assert isinstance(stinkbug.armour, Shield)
    assert stinkbug.layer_count == 3  # its own layer plus the shield's two


def test_attacks_slower_than_an_ant(canvas):
    stinkbug = Stinkbug(canvas, 800, 100)
    assert stinkbug.attack_interval == 1.5
    assert stinkbug.attack_interval > Ant(canvas, 800, 100).attack_interval


def test_label_is_stinkbug(canvas):
    Stinkbug(canvas, 800, 100)
    assert "Stinkbug" in labels(canvas)


# Stinking

def test_hit_damages_and_stuns_good(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    stinkbug = Stinkbug(canvas, 800, 100)
    good = make_good(canvas)

    stinkbug.attack(good)
    assert good.health == 1000 - stinkbug.damage
    assert good.is_stunned
    assert not good.can_act()


def test_stun_wears_off(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    stinkbug = Stinkbug(canvas, 800, 100)
    good = make_good(canvas)

    stinkbug.attack(good)
    now[0] += stinkbug.stun_time - 0.1
    assert not good.can_act()
    now[0] += 0.2
    assert good.can_act()


def test_keeps_good_stunned_while_attacking(canvas, monkeypatch):
    # It hits again before the stun runs out, so the good never gets a turn
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    stinkbug = Stinkbug(canvas, 800, 100)
    good = make_good(canvas)
    for _ in range(5):
        stinkbug.attack(good)
        now[0] += stinkbug.attack_interval
        assert not good.can_act()


def test_does_not_hit_faster_than_attack_interval(canvas, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    stinkbug = Stinkbug(canvas, 800, 100)
    good = make_good(canvas)
    stinkbug.attack(good)
    now[0] += 1.0  # enough for an ant, not for a stinkbug
    stinkbug.attack(good)
    assert good.health == 1000 - stinkbug.damage


# Shield

def test_shield_blocks_sugar_cube_from_the_front(canvas):
    stinkbug = Stinkbug(canvas, 800, 100)
    cube = SugarCube(canvas, 100, 100)
    stinkbug.take_damage(cube.damage_to_deal())
    assert stinkbug.health == stinkbug.max_health


def test_shield_does_not_block_explosions(canvas):
    stinkbug = Stinkbug(canvas, 800, 100)
    stinkbug.take_damage(Damage(50, DamageType.EXPLOSIVE, Direction.AMBIENT))
    assert stinkbug.health == stinkbug.max_health - 50
