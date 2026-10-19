import tkinter as tk
from rectangle import Rectangle
from card import Card
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

        # Fill card slots
        self.cards[0] = Card("bread", 25, Good)

        self.floor_rects = self._create_floor_rects(ROWS, COLUMNS, 90, (40, 120))
        self.card_rects = self._create_card_rects((60, 20), (70, 85), 10)

    def _create_floor_rects(self, rows: int, columns: int, grid_size: tuple[int, int], margins: tuple[int, int]):
        floor_rects = []
        x_margin, y_margin = margins
        colour_a = "#e0fa5f"
        colour_b = "#c8e04a"
        for i in range(columns):  # columns
            for j in range(rows):  # rows
                colour = colour_a if (i + j) % 2 == 0 else colour_b
                floor_rects.append(
                    Rectangle(
                        self.canvas,
                        x_margin + grid_size * i, y_margin + grid_size * j,
                        grid_size, grid_size,
                        colour
                    )
                )
        return floor_rects

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

            for i, rect in enumerate(self.card_rects):
                if rect.collide_point(point=pos):
                    print(f"Clicked a Card (index = {i})")
            for i, rect in enumerate(self.floor_rects):
                if rect.collide_point(point=pos):
                    print(f"Clicked a Floor (index = {i})")

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self):
        self._create_game_loop()
        self.root.mainloop()


game = Game()
game.run()
