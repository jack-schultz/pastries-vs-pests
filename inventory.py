from __future__ import annotations
from good import FlourFlower, SugarShooter
from card import Card
from entity import Entity


class Inventory(Entity):
    def __init__(self, canvas, x, y):
        colour = "#FFFF00"
        self.card_location = (120, 20)
        self.card_size = (70, 85)
        self.card_gap = 10
        self.cards_count: int = 2

        super().__init__(
            canvas, x, y,
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
        lx, ly = self.card_location
        w, h = self.card_size
        for i in range(self.cards_count):  # columns
            positions.append(
                (
                    lx + w * i + self.card_gap * i,
                    ly,
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
