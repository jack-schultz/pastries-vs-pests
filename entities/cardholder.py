from __future__ import annotations
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.goods.flour_flower import FlourFlower
from entities.card import Card
from entities.entity import Entity


class CardHolder(Entity):
    def __init__(self, canvas, x: int = 180, y: int = 20):
        colour = "#FFFF00"
        self.x, self.y = x, y
        self.card_size = (70, 85)
        self.card_gap = 10
        self.cards_count: int = 2
        self.selected_card: Card | None = None

        super().__init__(
            canvas, self.x, self.y,
            self.card_size[0] * self.cards_count + self.card_gap * (self.cards_count - 1),
            self.card_size[1],
            colour
        )

        self.card_attributes = [
            # Name, Cost, Class
            ("The Flour Flower", 50, FlourFlower),
            ("The Sugar Shooter", 100, SugarShooter),
        ]
        self.cards = self._create_cards()  # Holds the cards which are displayed along the top

    def _create_cards(self):
        """Create the cards displayed along the top of the screen."""
        self.cards: list[Card | None] = [None] * self.cards_count  # Create list of empty bread cards
        positions = []
        w, h = self.card_size
        for i in range(self.cards_count):  # columns
            positions.append(
                (
                    self.x + w * i + self.card_gap * i,
                    self.y,
                )
            )

        cards = []
        for (x, y), (name, cost, good_class) in zip(positions, self.card_attributes):
            cards.append(
                Card(
                    canvas=self.canvas,
                    width=self.card_size[0],
                    height=self.card_size[1],
                    x=x,
                    y=y,
                    name=name,
                    cost=cost,
                    good_class=good_class,
                )
            )

        return cards
