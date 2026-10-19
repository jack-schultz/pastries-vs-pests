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


def main():
    root = tk.Tk()
    root.title("Bakery vs. Pests")
    root.resizable(False, False)

    # Create the world canvas to store our rects coordinates
    canvas = tk.Canvas(root, width=900, height=600, bg="#fdf3e1", highlightthickness=0)
    # Places canvas widget inside parent window as tk is designed for menus
    canvas.pack()

    # === GAME OBJECTS ===
    rows, columns = 5, 9
    breads = [None] * rows * columns  # Create 5 rows of 10 prefilled as None
    floor_rects = []
    grid_size = 90
    x_margin, y_margin = 40, 120
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

    square1 = Rectangle(canvas, 0, 0, 40, 40, "#e07a5f")
    square2 = Rectangle(canvas,  0, 0, 40, 40, "#e07a5f")

    # === GAME LOOP ===
    def update():
        square2.move((3, 0))  # 3 pixels right per frame

        root.after(16, update)  # run again in about 16 ms (~60 FPS)

    update()

    # === EVENTS ===
    def on_motion(event):
        square1.centre = (event.x, event.y)

    def on_click(event):
        print(f"Clicked at ({event.x}, {event.y})")

    canvas.bind("<Motion>", on_motion)  # Mouse movement
    canvas.bind("<Button-1>", on_click)  # Left mouse click

    # === RUN ===
    root.mainloop()


main()
