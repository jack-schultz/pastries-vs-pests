from __future__ import annotations
from entities.living.goods.hardtack import Hardtack
from entities.living.goods.sugar_shooter import SugarShooter
from entities.living.goods.sugar_blaster import SugarBlaster
from entities.living.goods.flour_flower import FlourFlower
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.goods.profiterole import Profiterole
from entities.living.goods.oven_toaster import OvenToaster
from entities.card import Card, ToolType
from entities.entity import Entity


class CardHolder(Entity):
    def __init__(self, canvas, x: int = 175, y: int = 15, screen_width: int = 900):
        colour = "#8b6c5c"
        self.__x, self.__y = x, y
        self.__margin = 5
        self.__card_size = (70, 85)
        self.__card_gap = 10
        self.__card_attributes = [
            # Name, Cost, Class, Cooldown (seconds), Tool, Replaces (existing good class -> (class to spawn, replace cost))
            ("Flour Flower", 50, FlourFlower, 5.0, None, {}),
            ("Sugar Shooter", 100, SugarShooter, 5.0, None, {SugarShooter: {"replace": SugarBlaster, "cost": 200}}),
            ("Hardtack", 50, Hardtack, 30.0, None, {}),
            ("Popping Candy", 25, PoppingCandy, 20.0, None, {}),
            ("Profiterole", 150, Profiterole, 30.0, None, {}),
            ("Oven Toaster", 125, OvenToaster, 8.0, None, {}),
        ]
        # Tools get their own panel
        self.__tool_attributes = [
            ("Glove", 50, None, 5.0, ToolType.GLOVE, {}),
            ("Bin", 0, None, 3.0, ToolType.BIN, {}),
        ]
        self.__cards_count: int = len(self.__card_attributes)
        self.__selected_card: Card | None = None
        self.__hovered_card: Card | None = None

        super().__init__(
            canvas, self.__x, self.__y,
            self.__panel_width(len(self.__card_attributes)),
            self.__card_size[1] + self.__margin * 2,
            colour
        )

        # Tool panel
        tools_width = self.__panel_width(len(self.__tool_attributes))
        self.__tools_x = screen_width - 10 - tools_width
        self.__tools_panel = Entity(
            canvas, self.__tools_x, self.__y,
            tools_width, self.__card_size[1] + self.__margin * 2,
            colour
        )

        self.__cards = self._create_cards()  # Holds the cards which are displayed along the top

    def __panel_width(self, count: int) -> int:
        return self.__card_size[0] * count + self.__card_gap * (count - 1) + self.__margin * 2

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
        return (
            self.__build_row(self.__card_attributes, self.__x)
            + self.__build_row(self.__tool_attributes, self.__tools_x)
        )

    def __build_row(self, attributes, panel_x: int) -> list[Card]:
        w, h = self.__card_size
        cards = []
        for i, (name, cost, good_class, cooldown, tool, replaces) in enumerate(attributes):
            x = panel_x + w * i + self.__card_gap * i + self.__margin
            y = self.__y + self.__margin
            cards.append(
                Card(
                    canvas=self.canvas,
                    width=w,
                    height=h,
                    x=x,
                    y=y,
                    name=name,
                    cost=cost,
                    good_class=good_class,
                    cooldown=cooldown,
                    tool=tool,
                    replaces=replaces,
                )
            )
        return cards
