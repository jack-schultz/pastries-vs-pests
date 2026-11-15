import pytest
from entities.card import Card
from entities.living.goods.hardtack import Hardtack


def test_affordability_cooldown_and_creation(canvas):
    card = Card(canvas, 0, 0, 70, 85, "Hardtack", 50, Hardtack)
    assert card.can_afford(50) and not card.can_afford(49)
    card.start_cooldown()
    assert not card.is_usable(50)
    assert isinstance(card.create_good(canvas, 0, 0), Hardtack)


@pytest.mark.parametrize("cost, cooldown", [(-1, 5.0), (10, 0)])
def test_invalid_cost_or_cooldown_is_rejected(canvas, cost, cooldown):
    with pytest.raises(ValueError):
        Card(canvas, 0, 0, 70, 85, "Bad", cost, Hardtack, cooldown)
