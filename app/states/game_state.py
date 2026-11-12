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
        self.world = World(self.window, level_number)

    def tick(self) -> None:
        self.world.tick()

        # Check for game over
        if self.world.game_over:
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
        if self.world.clicked_next_button(pos):
            self.world.start_next_level()
            return

        # ===== CHECK CLICK POS =====
        # Loop through all clickable (tile, card & flour) objects to find which was clicked
        for tile in list(self.world.garden.tiles):
            if not tile.rect.collide_point(point=pos):
                continue

            if not isinstance(tile, Tile):
                continue

            if not self.world.card_holder.selected_card:
                continue

            # Skip if tile already has a good
            if not tile.is_empty:
                self.world.card_holder.selected_card = None
                continue

            # Skip if not enough flour
            if self.world.flour < self.world.card_holder.selected_card.cost:
                self.world.card_holder.selected_card = None
                continue

            # Create new good on the tiles
            cx, cy = tile.rect.centre
            tile.good = self.world.card_holder.selected_card.create_good(
                self.window.canvas, cx, cy
            )

            # Take flour amount, start the card's cooldown and reset selected card
            self.world.flour -= self.world.card_holder.selected_card.cost
            self.world.card_holder.selected_card.start_cooldown()
            self.world.card_holder.selected_card = None

        for card in list(self.world.card_holder.cards):
            if not card.rect.collide_point(point=pos):
                continue

            if not isinstance(card, Card):
                continue

            # Cards recharging can't be selected
            if not card.is_ready:
                continue

            # If card is already selected, deselect
            if self.world.card_holder.selected_card == card:
                self.world.card_holder.selected_card = None
                continue

            # Select card
            self.world.card_holder.selected_card = card

    def handle_motion(self, event: tk.Event) -> None:
        # Hovering over flour collects it
        self.world.collect_flour_at((event.x, event.y))
