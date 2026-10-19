import random
import time
import tkinter as tk
from rectangle import Rectangle
from pest import Ant
from card import Card
from good import FlourFlower, SugarShooter
from objects import Flour, Projectile
from tile import Tile

# Pygame difference to Tkinter
# Pygame	                    |   Tkinter
# while running: loop           |   root.mainloop()
# pygame.event.get()            |   Callbacks like command= or bind()
# screen.blit() / pygame.draw   |   canvas.create_rectangle(), canvas.create_image()
# clock.tick(60)	            |   root.after(ms, function)
# Manual hit detection          |   Widgets handle clicks automatically
# Rect.x                        |   Calc from points x1, y1, x2, y2 = self.__canvas.coords(self.__rect) where (x1, y1) is top left and (x2, y2) is bottom right


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bakery vs. Pests")
        self.root.resizable(False, False)

        # Create the world canvas to store our rects coordinates
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus
        self.canvas.pack()

        ROWS, COLUMNS = 5, 9

        # === GAME SETTINGS ===
        self.cards_count = 6
        self.grid_size = 90
        self.rows = ROWS
        self.tile_margins = (40, 120)
        card_location = (120, 20)
        card_size = (70, 85)
        card_gap = 10
        tile_margins = self.tile_margins

        self.ant_spawn_interval = 5  # seconds between ant spawns
        self.last_ant_spawn = time.monotonic()

        # === INPUT VARIABLES ===
        self.mouse_pos = None
        self.selected_card = None

        # === GAME VARIABLES ===
        self.flour = 50  # This is the currency to make bakery goods

        # === GAME OBJECTS ===
        self.pests = []
        self.projectiles = []
        self.cards = [None] * self.cards_count  # Create list of empty bread cards
        self.breads = [None] * ROWS * COLUMNS  # Create 5 rows of 10 prefilled as None

        # Holds the rects that make up the grid on the floor
        tiles = []
        for rect in self._create_tile_rects(ROWS, COLUMNS, self.grid_size, tile_margins):
            tiles.append(Tile(rect))

        # Holds the cards which are displayed along the top
        card_rects = self._create_card_rects(card_location, card_size, card_gap)
        card_info = {
            0: (card_rects[0], "The Flour Flower", 25, FlourFlower),
            1: (card_rects[1], "The Sugar Shooter", 60, SugarShooter),
        }
        cards = []
        for i in range(len(card_rects)):
            if i > max(card_info.keys()):
                break
            cards.append(Card(*card_info[i]))

        # Holds the game objects like flour or bullets. objects always have an obj.rect
        self.objects = []
        self.objects = self.objects + tiles
        self.objects = self.objects + cards

        # Text in top left to display flour count
        self.flour_text = self.canvas.create_text(
            10, 10,
            text=f"{self.flour}",  # amount of flour
            anchor="nw",  # top-left of the text sits at (10, 10)
            font=("Arial", 90, "bold"),
            fill="#3d405b",
        )

    def _create_tile_rects(self, rows: int, columns: int, grid_size: int, margins: tuple[int, int]):
        rects = []
        x_margin, y_margin = margins
        colour_a = "#e0fa5f"
        colour_b = "#c8e04a"
        for i in range(columns):  # columns
            for j in range(rows):  # rows
                colour = colour_a if (i + j) % 2 == 0 else colour_b
                rects.append(
                    Rectangle(
                        self.canvas,
                        x_margin + grid_size * i, y_margin + grid_size * j,
                        grid_size, grid_size,
                        colour
                    )
                )
        return rects

    def _create_card_rects(self, location: tuple[int, int], size: tuple[int, int], gap: int):
        card_rects = []
        colour = "#e63946"
        lx, ly = location
        w, h = size
        for i in range(len(self.cards)):  # columns
            card_rects.append(
                Rectangle(
                    self.canvas,
                    lx + w * i + gap * i, ly,
                    w, h,
                    colour
                )
            )
        return card_rects

    def _tile_blocking(self, pest):
        # Returns the tile whose good the pest's left edge has reached, if any
        px = pest.rect.x
        _, py = pest.rect.centre
        for obj in self.objects:
            if isinstance(obj, Tile) and obj.good and pest.is_blocked_by(obj.good):
                return obj
        return None

    def _pest_at(self, projectile):
        # Returns the first pest the projectile is overlapping, if any
        for pest in self.pests:
            if projectile.hits(pest):
                return pest
        return None

    def _spawn_ant(self):
        row = random.randrange(self.rows)
        _, y_margin = self.tile_margins
        # Spawn just off the right edge of the canvas (width 900), centred in the row
        ax = 900
        ay = y_margin + self.grid_size * row + 20
        rect = Rectangle(self.canvas, ax, ay, self.grid_size - 40, self.grid_size - 40, "#7a4a2b")
        self.pests.append(Ant(rect))

    def _create_game_loop(self):
        # === GAME LOOP ===
        def update():
            # Code which runs every frame goes here
            self.canvas.itemconfig(self.flour_text, text=f"{self.flour}")

            # Every good acts on its own timer; flour and projectiles it makes are routed to the right list
            for obj in list(self.objects):
                if isinstance(obj, Tile) and obj.good:
                    made = obj.good.act(self.canvas)
                    if isinstance(made, Flour):
                        self.objects.append(made)
                    elif isinstance(made, Projectile):
                        self.projectiles.append(made)

            # Spawn an ant on the right edge of a random row
            if time.monotonic() - self.last_ant_spawn >= self.ant_spawn_interval:
                self.last_ant_spawn = time.monotonic()
                self._spawn_ant()

            # Pests walk left unless blocked by a good, which they attack instead
            for pest in list(self.pests):
                blocking_tile = self._tile_blocking(pest)
                if blocking_tile:
                    pest.attack(blocking_tile.good)
                    if blocking_tile.good.is_dead:
                        blocking_tile.good.destroy()
                        blocking_tile.clear_good()
                else:
                    pest.move()

                # Remove pests that have left the screen
                if pest.has_left_screen():
                    pest.destroy()
                    self.pests.remove(pest)
                else:
                    # Draw pests above goods (flour is raised after, so it stays on top)
                    pest.rect.raise_to_top()

            # projectiles fly right and damage the first pest they touch
            for projectile in list(self.projectiles):
                projectile.move()
                hit_pest = self._pest_at(projectile)
                if hit_pest:
                    hit_pest.take_damage(projectile.damage)
                    if hit_pest.is_dead:
                        hit_pest.destroy()
                        self.pests.remove(hit_pest)
                elif projectile.rect.x < 900:
                    projectile.rect.raise_to_top()
                    continue
                projectile.destroy()
                self.projectiles.remove(projectile)

            # Draw flour on top of everything else
            for obj in self.objects:
                if isinstance(obj, Flour):
                    obj.rect.raise_to_top()

            self.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event):
            self.mouse_pos = (event.x, event.y)

        def on_click(event):
            pos = (event.x, event.y)

            for obj in list(self.objects):
                if obj.rect.collide_point(point=pos):
                    if isinstance(obj, Tile):
                        if self.selected_card:
                            # Skip if tile already has a good
                            if not obj.is_empty:
                                self.selected_card = None
                                continue

                            # Skip if not enough flour
                            if self.flour < self.selected_card.cost:
                                self.selected_card = None
                                continue

                            # Create new good on the tiles
                            obj.good = self.selected_card.create_good(
                                Rectangle(self.canvas, obj.rect.x + 10, obj.rect.y + 10, obj.rect.w - 20, obj.rect.h - 20, "#FFFF00"),
                            )

                            # Take flour amount and reset selected card
                            self.flour -= self.selected_card.cost
                            self.selected_card = None

                    elif isinstance(obj, Card):
                        # If card is already selected, deselect
                        if self.selected_card == obj:
                            self.selected_card = None
                            continue

                        # Select card
                        self.selected_card = obj

                    elif isinstance(obj, Flour):
                        # Collecting removes it from the canvas and returns its amount
                        self.flour += obj.collect()
                        self.objects.remove(obj)

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self):
        self._create_game_loop()
        self.root.mainloop()


game = Game()
game.run()
