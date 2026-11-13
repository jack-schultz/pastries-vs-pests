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
        # Cost shown next to the mouse while a card is over a tile
        self.__cost_preview = self.window.canvas.create_text(
            0, 0, text="", anchor="nw",
            font=("Arial", 14, "bold"), fill="#ffffff", state="hidden",
        )

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
        self.window.canvas.itemconfig(self.__cost_preview, state="hidden")

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

        # Skip if tile has a good and this card cant replace it
        if not selected.can_place_on(tile.good):
            holder.selected_card = None
            return

        # Replacing has its own cost, otherwise it's the card's normal cost
        existing = tile.good
        cost = selected.cost_for(existing)

        # Skip if not enough flour
        if self.__world.flour < cost:
            holder.selected_card = None
            return

        # Create new good on the tile and replace if able
        cx, cy = tile.rect.centre
        new_good = selected.create_good(self.window.canvas, cx, cy, existing)
        if existing is not None:
            existing.destroy()
            tile.clear_good()
        tile.good = new_good

        # Take flour amount, start the card's cooldown and reset selected card
        self.__world.flour -= cost
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
        # Show what the selected card would cost on the tile under the mouse
        self.__update_cost_preview((event.x, event.y))

    def __tile_at(self, pos: tuple[int, int]) -> Tile | None:
        for tile in self.__world.garden.tiles:
            if tile.rect.collide_point(point=pos):
                return tile
        return None

    def __update_cost_preview(self, pos: tuple[int, int]) -> None:
        canvas = self.window.canvas
        selected = self.__world.card_holder.selected_card
        tile = self.__tile_at(pos)

        # Only cards placing goods show a cost, not the glove or bin, and only where the placement would work
        if (
            not selected
            or selected.tool is not None
            or tile is None
            or not selected.can_place_on(tile.good)
        ):
            canvas.itemconfig(self.__cost_preview, state="hidden")
            return

        cost = selected.cost_for(tile.good)
        # Red when the player can't pay for it
        colour = "#ffffff" if self.__world.flour >= cost else "#ffb3b3"
        canvas.itemconfig(self.__cost_preview, text=f"-{cost}", fill=colour, state="normal")
        canvas.coords(self.__cost_preview, pos[0] + 16, pos[1] - 16)
        canvas.tag_raise(self.__cost_preview)
