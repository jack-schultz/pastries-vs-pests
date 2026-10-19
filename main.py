import tkinter as tk
from rectangle import Rectangle
from card import Card
from good import Good
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

        # === INPUT VARIABLES ===
        self.mouse_pos = None
        self.selected_card = None

        # === GAME OBJECTS ===
        self.pests = []
        self.cards = [None] * self.cards_count  # Create list of empty bread cards
        self.breads = [None] * ROWS * COLUMNS  # Create 5 rows of 10 prefilled as None

        # Holds the rects that make up the grid on the floor
        tiles = []
        for rect in self._create_tile_rects(ROWS, COLUMNS, 90, (40, 120)):
            tiles.append(Tile(rect))

        # Holds the cards which are displayed along the top
        card_rects = self._create_card_rects((60, 20), (70, 85), 10)
        card_info = {
            0: (card_rects[0], "bread", 25, Good),
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

    def _create_tile_rects(self, rows: int, columns: int, grid_size: tuple[int, int], margins: tuple[int, int]):
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
            # square2.move((1, 0))

            self.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event):
            self.mouse_pos = (event.x, event.y)

        def on_click(event):
            print(f"Clicked at ({event.x}, {event.y})")
            pos = (event.x, event.y)

            for obj in self.objects:
                if obj.rect.collide_point(point=pos):
                    print(f"Clicked a {type(obj).__name__}")

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self):
        self._create_game_loop()
        self.root.mainloop()


game = Game()
game.run()
