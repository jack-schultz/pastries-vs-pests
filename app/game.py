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

        # === INPUT VARIABLES ===
        self.mouse_pos: tuple[int, int] | None = None
        self.selected_card: Card | None = None

        # === GAME VARIABLES ===
        self.flour: int = 50  # This is the currency to make bakery goods

        # === GAME OBJECTS ===
        self.world = World(self.window.canvas, self.flour, self.window.width)

    def _create_game_loop(self) -> None:
        # ========== GAME LOOP =========
        def update():
            # Code which runs every frame goes here
            self.world.update_flour_count(self.flour)

            # ===== GOODS ACT =====
            self.world.add_goods(self.world.garden.goods_act())

            # ===== SPAWN ANTS =====
            self.world.spawn_ant_if_due()

            # ===== PESTS WALK =====
            self.world.update_pests()

            # ===== MOVE PROJECTILES =====
            self.world.update_projectiles()

            # ===== DRAW FLOUR ON TOP  =====
            self.world.raise_flours()

            self.window.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event: tk.Event) -> None:
            self.mouse_pos = (event.x, event.y)

        def on_click(event: tk.Event) -> None:
            pos = (event.x, event.y)

            # ===== CHECK CLICK POS =====
            # Loop through all clickable (tile, card & flour) objects to find which was clicked
            for tile in list(self.world.garden.tiles):
                if not tile.rect.collide_point(point=pos):
                    continue

                if not isinstance(tile, Tile):
                    continue

                if not self.selected_card:
                    continue

                # Skip if tile already has a good
                if not tile.is_empty:
                    self.selected_card = None
                    continue

                # Skip if not enough flour
                if self.flour < self.selected_card.cost:
                    self.selected_card = None
                    continue

                # Create new good on the tiles
                tile.good = self.selected_card.create_good(
                    self.window.canvas, tile.rect.x + 10, tile.rect.y + 10, tile.rect.w - 20, tile.rect.h - 20
                )

                # Take flour amount and reset selected card
                self.flour -= self.selected_card.cost
                self.selected_card = None

            for card in list(self.world.card_holder.cards):
                if not card.rect.collide_point(point=pos):
                    continue

                if not isinstance(card, Card):
                    continue

                # If card is already selected, deselect
                if self.selected_card == card:
                    self.selected_card = None
                    continue

                # Select card
                self.selected_card = card

            self.flour += self.world.collect_flour_at(pos)

        self.window.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.window.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self) -> None:
        self._create_game_loop()
        self.window.run()
