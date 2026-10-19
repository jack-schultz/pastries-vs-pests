import tkinter as tk
from rectangle import Rectangle
from card import Card
from good import FlourFlower
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
        card_location = (120, 20)
        card_size = (70, 85)
        card_gap = 10
        tile_margins = (40, 120)

        # === INPUT VARIABLES ===
        self.mouse_pos = None
        self.selected_card = None

        # === GAME VARIABLES ===
        self.flour = 50  # This is the currency to make bakery goods

        # === GAME OBJECTS ===
        self.pests = []
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

    def _create_game_loop(self):
        # === GAME LOOP ===
        def update():
            # Code which runs every frame goes here
            self.canvas.itemconfig(self.flour_text, text=f"{self.flour}")

            self.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event):
            self.mouse_pos = (event.x, event.y)

        def on_click(event):
            pos = (event.x, event.y)

            for obj in self.objects:
                if obj.rect.collide_point(point=pos):
                    if type(obj).__name__.lower() == "tile":
                        if self.selected_card:
                            # Skip if tile already has a good
                            if obj.good:
                                self.selected_card = None
                                continue

                            # Skip if not enough flour
                            if self.flour < self.selected_card.cost:
                                self.selected_card = None
                                continue

                            # Create new good on the tiles
                            obj.good = self.selected_card.good_class(
                                rect=Rectangle(self.canvas, obj.rect.x + 10, obj.rect.y + 10, obj.rect.w - 20, obj.rect.h - 20, "#FFFF00"),
                                tile=obj,
                            )

                            # Take flour amount and reset selected card
                            self.flour -= self.selected_card.cost
                            self.selected_card = None

                    elif type(obj).__name__.lower() == "card":
                        # If card is already selected, deselect
                        if self.selected_card == obj:
                            self.selected_card = None
                            continue

                        # Select card
                        self.selected_card = obj

                    elif type(obj).__name__.lower() == "flour":
                        self.flour += obj.amount

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self):
        self._create_game_loop()
        self.root.mainloop()


game = Game()
game.run()
