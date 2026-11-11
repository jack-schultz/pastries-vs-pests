from __future__ import annotations
from app.states.basestate import BaseState
import tkinter as tk
from app.states.pausestate import PauseState
from entities.card import Card
from entities.tile import Tile
from app.world import World


class GameState(BaseState):
    def __init__(self, state_stack, window) -> None:
        super().__init__(state_stack, window)
        self.world = World(self.window)

    def tick(self) -> None:
        self.world.update_flour_count()

        # ===== GOODS ACT =====
        self.world.add_goods(self.world.garden.goods_act())

        # ===== SPAWN ANTS =====
        self.world.spawn_pest_if_due()

        # ===== PESTS WALK =====
        self.world.update_pests()

        # ===== MOVE PROJECTILES =====
        self.world.update_projectiles()

        # ===== DRAW FLOUR ON TOP  =====
        self.world.raise_flours()

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Escape":
            self.state_stack.push(
                PauseState(self.state_stack, self.window)
            )

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)

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
            tile.good = self.world.card_holder.selected_card.create_good(
                self.window.canvas, tile.rect.x + 10, tile.rect.y + 10, tile.rect.w - 20, tile.rect.h - 20
            )

            # Take flour amount and reset selected card
            self.world.flour -= self.world.card_holder.selected_card.cost
            self.world.card_holder.selected_card = None

        for card in list(self.world.card_holder.cards):
            if not card.rect.collide_point(point=pos):
                continue

            if not isinstance(card, Card):
                continue

            # If card is already selected, deselect
            if self.world.card_holder.selected_card == card:
                self.world.card_holder.selected_card = None
                continue

            # Select card
            self.world.card_holder.selected_card = card

        self.world.flour += self.world.collect_flour_at(pos)
