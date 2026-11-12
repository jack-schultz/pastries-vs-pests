from __future__ import annotations
from entities.living.goods.hardtack import Hardtack
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.goods.flour_flower import FlourFlower
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.goods.profiterole import Profiterole
from entities.card import Card
from entities.entity import Entity


class CardHolder(Entity):
    def __init__(self, canvas, x: int = 180, y: int = 20):
        colour = "#FFFF00"
        self.x, self.y = x, y
        self.card_size = (70, 85)
        self.card_gap = 10
        self.card_attributes = [
            # Name, Cost, Class, Cooldown (seconds)
            ("Flour Flower", 50, FlourFlower, 5.0),
            ("Sugar Shooter", 100, SugarShooter, 5.0),
            ("Hardtack", 50, Hardtack, 30.0),
            ("Popping Candy", 25, PoppingCandy, 20.0),
            ("Cherry Bombe", 150, Profiterole, 30.0),
        ]
        self.cards_count: int = len(self.card_attributes)
        self.selected_card: Card | None = None

        super().__init__(
            canvas, self.x, self.y,
            self.card_size[0] * self.cards_count + self.card_gap * (self.cards_count - 1),
            self.card_size[1],
            colour
        )

        self.cards = self._create_cards()  # Holds the cards which are displayed along the top

    def update_cooldowns(self) -> None:
        for card in self.cards:
            card.tick_cooldown()

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
        for (x, y), (name, cost, good_class, cooldown) in zip(positions, self.card_attributes):
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
                    cooldown=cooldown,
                )
            )

        return cards
