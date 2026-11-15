import pytest
from entities.cardholder import CardHolder


@pytest.fixture
def holder(canvas):
    return CardHolder(canvas)


def test_holds_the_goods_and_tools(holder):
    names = [card.name for card in holder.cards]
    assert "Flour Flower" in names and "Glove" in names


def test_remembers_the_selected_card(holder):
    assert holder.selected_card is None
    holder.selected_card = holder.cards[0]
    assert holder.selected_card is holder.cards[0]
