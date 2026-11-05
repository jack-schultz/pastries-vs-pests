from __future__ import annotations
import tkinter as tk
from entities.card import Card
from entities.tile import Tile
from app.window import Window
from app.world import World


class Game:
    # Holds the game state and rules. Draws onto a window
    def __init__(self) -> None:
        self.window = Window()
        self.world = World(self.window)

    def _create_game_loop(self) -> None:
        # ========== GAME LOOP =========
        def update():
            # Code which runs every frame goes here
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

            self.window.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        def on_click(event: tk.Event) -> None:
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

        self.window.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self) -> None:
        self._create_game_loop()
        self.window.run()
