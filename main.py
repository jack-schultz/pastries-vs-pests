from __future__ import annotations
import random
import time
import tkinter as tk
from pest import Ant, Pest
from card import Card
from good import FlourFlower, SugarShooter
from flour import Flour
from projectile import Projectile
from tile import Tile
from good import Good

# Pygame difference to Tkinter
# Pygame	                    |   Tkinter
# while running: loop           |   root.mainloop()
# pygame.event.get()            |   Callbacks like command= or bind()
# screen.blit() / pygame.draw   |   canvas.create_rectangle(), canvas.create_image()
# clock.tick(60)	            |   root.after(ms, function)
# Manual hit detection          |   Widgets handle clicks automatically
# Rect.x                        |   Calc from points x1, y1, x2, y2 = self.__canvas.coords(self.__rect) where (x1, y1) is top left and (x2, y2) is bottom right


class Game:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bakery vs. Pests")
        self.root.resizable(False, False)

        self.width, self.height = (900, 600)

        # Create the world canvas to store our rects coordinates
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus so it needs this
        self.canvas.pack()

        # === GAME SETTINGS ===
        self.cards_count: int = 6
        self.grid_size: int = 90
        self.rows, self.columns = 5, 9
        self.tile_margins: tuple[int, int] = (40, 120)
        self.card_location = (120, 20)
        self.card_size = (70, 85)
        self.card_gap = 10

        self.ant_spawn_interval: float = 5  # seconds between ant spawns
        self.last_ant_spawn: float = time.monotonic()

        # === INPUT VARIABLES ===
        self.mouse_pos: tuple[int, int] | None = None
        self.selected_card: Card | None = None

        # === GAME VARIABLES ===
        self.flour: int = 50  # This is the currency to make bakery goods

        # === GAME OBJECTS ===

        self.card_attributes = [
            # Name, Cost, Class
            ("The Flour Flower", 25, FlourFlower),
            ("The Sugar Shooter", 60, SugarShooter),
        ]
        self.pests: list[Pest] = []
        self.flours: list[Flour] = []
        self.projectiles: list[Projectile] = []
        self.cards = self._create_cards()  # Holds the cards which are displayed along the top
        self.tiles = self._create_tiles()  # Holds the rects that make up the grid on the floor

        # Text in top left to display flour count
        self.flour_text = self.canvas.create_text(
            10, 10,
            text=f"{self.flour}",  # amount of flour
            anchor="nw",  # top-left of the text sits at (10, 10)
            font=("Arial", 90, "bold"),
            fill="#3d405b",
        )

    def _create_cards(self):
        """Create the cards displayed along the top of the screen."""
        self.cards: list[Card | None] = [None] * self.cards_count  # Create list of empty bread cards
        positions = []
        lx, ly = self.card_location
        w, h = self.card_size
        for i in range(self.cards_count):  # columns
            positions.append(
                (
                    lx + w * i + self.card_gap * i,
                    ly,
                )
            )

        cards = []
        for (x, y), (name, cost, good_class) in zip(positions, self.card_attributes):
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
                )
            )

        return cards

    def _create_tiles(self):
        positions = []
        x_margin, y_margin = self.tile_margins
        colour_a = "#e0fa5f"
        colour_b = "#c8e04a"
        for i in range(self.columns):  # columns
            for j in range(self.rows):  # rows
                colour = colour_a if (i + j) % 2 == 0 else colour_b
                positions.append(
                    (
                        x_margin + self.grid_size * i,
                        y_margin + self.grid_size * j,
                        colour
                    )
                )

        tiles: list[Tile] = []
        for x, y, colour in positions:
            tiles.append(Tile(self.canvas, x, y, self.grid_size, colour))
        return tiles

    def _tile_blocking(self, pest: Pest) -> Tile | None:
        # Returns the tile whose good the pest's left edge has reached, if any
        _, py = pest.rect.centre
        for tile in self.tiles:
            if isinstance(tile, Tile) and isinstance(tile.good, Good) and pest.is_blocked_by(tile.good):
                return tile
        return None

    def _pest_at(self, projectile: Projectile) -> Pest | None:
        # Returns the first pest the projectile is overlapping, if any
        for pest in self.pests:
            if projectile.hits(pest):
                return pest
        return None

    def _spawn_ant(self) -> None:
        row = random.randrange(self.rows)
        _, y_margin = self.tile_margins
        # Spawn just off the right edge of the canvas, centred in the row
        ax = self.width
        ay = y_margin + self.grid_size * row + 20
        self.pests.append(Ant(self.canvas, ax, ay))

    def _create_game_loop(self) -> None:
        # ========== GAME LOOP =========
        def update():
            # Code which runs every frame goes here
            self.canvas.itemconfig(self.flour_text, text=f"{self.flour}")

            # ===== GOODS ACT =====
            # Every good acts on its own timer; flour and projectiles it makes are routed to the right list
            for tile in list(self.tiles):
                if not isinstance(tile, Tile) and tile.good:
                    continue

                made_obj = tile.good.act(self.canvas)
                if isinstance(made_obj, Flour):
                    self.flours.append(made_obj)
                elif isinstance(made_obj, Projectile):
                    self.projectiles.append(made_obj)

            # ===== SPAWN ANTS =====
            # Spawn an ant on the right edge of a random row
            if time.monotonic() - self.last_ant_spawn >= self.ant_spawn_interval:
                self.last_ant_spawn = time.monotonic()
                self._spawn_ant()

            # ===== PESTS WALK =====
            # Pests walk left unless blocked by a good, which they attack instead
            for pest in list(self.pests):
                blocking_tile = self._tile_blocking(pest)
                # Colliding with a tile which has a good
                if blocking_tile and blocking_tile.good:
                    # Check the good blocking the pest is valid
                    blocking_good = blocking_tile.good
                    if not blocking_good:
                        continue
                    # Pest attacks good till its dead
                    pest.attack(blocking_good)
                    if blocking_good.is_dead:
                        blocking_good.destroy()
                        blocking_tile.clear_good()
                else:
                    # If not colliding, moves
                    pest.move()

                # Remove pests that have left the screen
                if pest.has_left_screen():
                    pest.destroy()
                    self.pests.remove(pest)
                else:
                    # Draw pests above goods (flour is raised after, so it stays on top)
                    pest.rect.raise_to_top()

            # ===== MOVE PROJECTILES =====
            # projectiles fly right and damage the first pest they touch
            for projectile in list(self.projectiles):
                projectile.move()
                hit_pest = self._pest_at(projectile)
                if hit_pest:
                    hit_pest.take_damage(projectile.damage)
                    if hit_pest.is_dead:
                        hit_pest.destroy()
                        self.pests.remove(hit_pest)
                        projectile.destroy()
                        self.projectiles.remove(projectile)

                # If the projectile goes off the screen, kill it
                elif projectile.rect.x > self.width:
                    projectile.destroy()
                    self.projectiles.remove(projectile)

                projectile.rect.raise_to_top()

            # ===== DRAW FLOUR ON TOP  =====
            # Draw flour on top of everything else
            for obj in self.flours:
                if isinstance(obj, Flour):
                    obj.rect.raise_to_top()

            self.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event: tk.Event) -> None:
            self.mouse_pos = (event.x, event.y)

        def on_click(event: tk.Event) -> None:
            pos = (event.x, event.y)

            # ===== CHECK CLICK POS =====
            # Loop through all clickable (tile, card & flour) objects to find which was clicked
            for tile in list(self.tiles):
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
                    self.canvas, tile.rect.x + 10, tile.rect.y + 10, tile.rect.w - 20, tile.rect.h - 20
                )

                # Take flour amount and reset selected card
                self.flour -= self.selected_card.cost
                self.selected_card = None

            for card in list(self.cards):
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

            for flour in list(self.flours):
                if not flour.rect.collide_point(point=pos):
                    continue

                if not isinstance(flour, Flour):
                    continue

                # Collecting removes it from the canvas and returns its amount
                self.flour += flour.collect()
                self.flours.remove(flour)

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self) -> None:
        self._create_game_loop()
        self.root.mainloop()


game = Game()
game.run()
