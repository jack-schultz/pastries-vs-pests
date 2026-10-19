import tkinter as tk
from rectangle import Rectangle

# Pygame difference to Tkinter
# Pygame	                    |   Tkinter
# while running: loop           |   root.mainloop()
# pygame.event.get()            |   Callbacks like command= or bind()
# screen.blit() / pygame.draw   |   canvas.create_rectangle(), canvas.create_image()
# clock.tick(60)	            |   root.after(ms, function)
# Manual hit detection          |   Widgets handle clicks automatically
# Rect.x                        |   Calc from points x1, y1, x2, y2 = self.__canvas.coords(self.__rect) where (x1, y1) is top left and (x2, y2) is bottom right


def create_floor_rects(canvas, rows, columns, grid_size, margins):
    floor_rects = []
    x_margin, y_margin = margins
    colour_a = "#e0fa5f"
    colour_b = "#c8e04a"
    for i in range(columns):  # columns
        for j in range(rows):  # rows
            colour = colour_a if (i + j) % 2 == 0 else colour_b
            floor_rects.append(
                Rectangle(
                    canvas,
                    x_margin + grid_size * i, y_margin + grid_size * j,
                    grid_size, grid_size,
                    colour
                )
            )
    return floor_rects


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
        self.mouse_pos = None
        self.mouse_click_pos = None

        # === GAME OBJECTS ===
        self.floor_rects = create_floor_rects(self.canvas, ROWS, COLUMNS, 90, (40, 120))
        self.pests = []
        self.bread_cards = [None] * ROWS * COLUMNS  # Create 5 rows of 10 prefilled as None
        self.breads = [None] * ROWS * COLUMNS  # Create 5 rows of 10 prefilled as None

        # === GAME LOOP ===
        def update():
            #square2.move((1, 0))  # 3 pixels right per frame

            self.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event):
            self.mouse_pos = (event.x, event.y)

        def on_click(event):
            print(f"Clicked at ({event.x}, {event.y})")
            self.mouse_click_pos = (event.x, event.y)

        self.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self):
        self.root.mainloop()


game = Game()
game.run()
