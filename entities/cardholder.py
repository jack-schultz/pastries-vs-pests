from __future__ import annotations
from entities.living.goods.hardtack import Hardtack
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.goods.flour_flower import FlourFlower
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.goods.profiterole import Profiterole
from entities.card import Card
from entities.entity import Entity


class CardHolder(Entity):
    def __init__(self, canvas, x: int = 175, y: int = 15):
        colour = "#8b6c5c"
        self.__x, self.__y = x, y
        self.__margin = 5
        self.__card_size = (70, 85)
        self.__card_gap = 10
        self.__card_attributes = [
            # Name, Cost, Class, Cooldown (seconds)
            ("Flour Flower", 50, FlourFlower, 5.0),
            ("Sugar Shooter", 100, SugarShooter, 5.0),
            ("Hardtack", 50, Hardtack, 30.0),
            ("Popping Candy", 25, PoppingCandy, 20.0),
            ("Profiterole", 150, Profiterole, 30.0),
        ]
        self.__cards_count: int = len(self.__card_attributes)
        self.__selected_card: Card | None = None
        self.__hovered_card: Card | None = None

        super().__init__(
            canvas, self.__x, self.__y,
            self.__card_size[0] * self.__cards_count + self.__card_gap * (self.__cards_count - 1) + self.__margin * 2,
            self.__card_size[1] + self.__margin * 2,
            colour
        )

        self.__cards = self._create_cards()  # Holds the cards which are displayed along the top

    @property
    def cards(self) -> list[Card | None]:
        return self.__cards

    @property
    def selected_card(self) -> Card | None:
        return self.__selected_card

    @selected_card.setter
    def selected_card(self, card: Card | None) -> None:
        self.__selected_card = card

    def update_cooldowns(self) -> None:
        for card in self.__cards:
            card.tick_cooldown()

    def update_cards(self, flour: int) -> None:
        # Drop the selection if the card can no longer be used
        if self.__selected_card and not self.__selected_card.is_usable(flour):
            self.__selected_card = None
        for card in self.__cards:
            card.update_display(
                flour,
                selected=card is self.__selected_card,
                hovered=card is self.__hovered_card,
            )

    def hover_at(self, pos: tuple[int, int]) -> None:
        # Remembers which card the mouse is over so it can be highlighted
        self.__hovered_card = None
        for card in self.__cards:
            if card.rect.collide_point(pos):
                self.__hovered_card = card

    def _create_cards(self):
        """Create the cards displayed along the top of the screen."""
        self.__cards: list[Card | None] = [None] * self.__cards_count  # Create list of empty bread cards
        positions = []
        w, h = self.__card_size
        for i in range(self.__cards_count):  # columns
            positions.append(
                (
                    self.__x + w * i + self.__card_gap * i + self.__margin,
                    self.__y + self.__margin,
                )
            )

        cards = []
        for (x, y), (name, cost, good_class, cooldown) in zip(positions, self.__card_attributes):
            cards.append(
                Card(
                    canvas=self.canvas,
                    width=self.__card_size[0],
                    height=self.__card_size[1],
                    x=x,
                    y=y,
                    name=name,
                    cost=cost,
                    good_class=good_class,
                    cooldown=cooldown,
                )
            )

        return cards
