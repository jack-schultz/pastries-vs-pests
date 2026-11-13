from __future__ import annotations
from app.states.base_state import BaseState
import tkinter as tk
from app.states.pause_state import PauseState
from app.states.gameover_state import GameOverState
from entities.card import Card, ToolType
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
        # Tiles first, then cards. The two never overlap
        for tile in list(self.__world.garden.tiles):
            if not tile.rect.collide_point(point=pos):
                continue

            if not isinstance(tile, Tile):
                continue

            self.__click_tile(tile)
            return

        for card in list(self.__world.card_holder.cards):
            if not card.rect.collide_point(point=pos):
                continue

            if not isinstance(card, Card):
                continue

            self.__click_card(card)
            return

    def __click_tile(self, tile: Tile) -> None:
        holder = self.__world.card_holder
        selected = holder.selected_card
        if not selected:
            return

        if selected.tool == ToolType.GLOVE:
            self.__glove_tile(tile, selected)
            return

        if selected.tool == ToolType.BIN:
            # Bin removes whatever good is on the tile, for free
            if not tile.is_empty:
                self.__world.remove_good(tile)
                selected.start_cooldown()
            holder.selected_card = None
            return

        # Skip if tile already has a good
        if not tile.is_empty:
            holder.selected_card = None
            return

        # Skip if not enough flour
        if self.__world.flour < selected.cost:
            holder.selected_card = None
            return

        # Create new good on the tiles
        cx, cy = tile.rect.centre
        tile.good = selected.create_good(self.window.canvas, cx, cy)

        # Take flour amount, start the card's cooldown and reset selected card
        self.__world.flour -= selected.cost
        selected.start_cooldown()
        holder.selected_card = None

    def __glove_tile(self, tile: Tile, glove: Card) -> None:
        world = self.__world
        holder = world.card_holder

        # pick up the good on this tile
        if not world.is_holding:
            world.pick_up(tile)
            return

        # Put it back where it came from
        if tile is world.held_origin:
            world.return_held()
            holder.selected_card = None
            return

        # Drop it on an empty tile
        if world.drop_held(tile):
            # The glove costs flour and starts its cooldown
            world.flour -= glove.cost
            glove.start_cooldown()
            holder.selected_card = None

    def __click_card(self, card: Card) -> None:
        world = self.__world
        holder = world.card_holder

        # Return held good if clicked card and continue
        if world.is_holding:
            world.return_held()
            holder.selected_card = None

        # Cards recharging or too expensive can't be selected
        if not card.is_usable(world.flour):
            return

        # If card is already selected, deselect
        if holder.selected_card == card:
            holder.selected_card = None
            return

        # Select card
        holder.selected_card = card

    def handle_motion(self, event: tk.Event) -> None:
        # The held good follows the mouse
        self.__world.move_held((event.x, event.y))
        # Hovering over flour collects it
        self.__world.collect_flour_at((event.x, event.y))
        # Hovering over a card highlights it
        self.__world.card_holder.hover_at((event.x, event.y))
