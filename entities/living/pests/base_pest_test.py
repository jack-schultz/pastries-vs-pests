import pytest
from entities.living.pests.base_pest import BasePest


@pytest.fixture
def pest(canvas):
    return BasePest(canvas, 100, 100, 30, "#ffffff")


def test_walks_left_and_leaves_the_screen_once_fully_off(pest):
    left = pest.rect.left
    pest.move()
    assert pest.rect.left == left - pest.speed and not pest.has_left_screen()
    pest.rect.left = -31
    assert pest.has_left_screen()


def test_attack_interval_must_be_a_float(pest):
    with pytest.raises(ValueError):
        pest.attack_interval = 2
