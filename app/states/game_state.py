from __future__ import annotations
from app.states.base_state import BaseState
import tkinter as tk
from app.states.pause_state import PauseState
from app.states.gameover_state import GameOverState
from entities.card import Card
from entities.tile import Tile
from app.world import World


class GameState(BaseState):
    def __init__(self, state_stack, window, level_number: int = 1) -> None:
        super().__init__(state_stack, window)
        self.__world = World(self.window, level_number)

    @property
    def world(self) -> World:
        return self.__world

    def tick(self) -> None:
        self.__world.tick()

        # Check for game over
        if self.__world.game_over:
            self.state_stack.push(GameOverState(self.state_stack, self.window))
            return

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Escape":
            self.state_stack.push(
                PauseState(self.state_stack, self.window)
            )

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)

        # Next level button
        if self.__world.clicked_next_button(pos):
            self.__world.start_next_level()
            return

        # ===== CHECK CLICK POS =====
        # Loop through all clickable (tile, card & flour) objects to find which was clicked
        for tile in list(self.__world.garden.tiles):
            if not tile.rect.collide_point(point=pos):
                continue

            if not isinstance(tile, Tile):
                continue

            if not self.__world.card_holder.selected_card:
                continue

            # Skip if tile already has a good
            if not tile.is_empty:
                self.__world.card_holder.selected_card = None
                continue

            # Skip if not enough flour
            if self.__world.flour < self.__world.card_holder.selected_card.cost:
                self.__world.card_holder.selected_card = None
                continue

            # Create new good on the tiles
            cx, cy = tile.rect.centre
            tile.good = self.__world.card_holder.selected_card.create_good(
                self.window.canvas, cx, cy
            )

            # Take flour amount, start the card's cooldown and reset selected card
            self.__world.flour -= self.__world.card_holder.selected_card.cost
            self.__world.card_holder.selected_card.start_cooldown()
            self.__world.card_holder.selected_card = None

        for card in list(self.__world.card_holder.cards):
            if not card.rect.collide_point(point=pos):
                continue

            if not isinstance(card, Card):
                continue

            # Cards recharging can't be selected
            if not card.is_ready:
                continue

            # If card is already selected, deselect
            if self.__world.card_holder.selected_card == card:
                self.__world.card_holder.selected_card = None
                continue

            # Select card
            self.__world.card_holder.selected_card = card

    def handle_motion(self, event: tk.Event) -> None:
        # Hovering over flour collects it
        self.__world.collect_flour_at((event.x, event.y))
