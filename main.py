import tkinter as tk

# Pygame difference to Tkinter
# Pygame	                    |   Tkinter
# while running: loop           |   root.mainloop()
# pygame.event.get()            |   Callbacks like command= or bind()
# screen.blit() / pygame.draw   |   canvas.create_rectangle(), canvas.create_image()
# clock.tick(60)	            |   root.after(ms, function)
# Manual hit detection          |   Widgets handle clicks automatically
# Rect.x                        |   Calc from points x1, y1, x2, y2 = self.__canvas.coords(self.__rect) where (x1, y1) is top left and (x2, y2) is bottom right


class Rectangle:
    def __init__(self, canvas, width, height, colour):
        self.__canvas = canvas
        self.__rect = self.__canvas.create_rectangle(
            0, 0, width, height,
            fill=colour,
            outline="",
        )

    @property
    def width(self):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        width = x2 - x1  # Calculate difference between points
        return width

    @width.setter
    def width(self, new_width):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            x1, y1,  # top left
            x1 + new_width, y2  # bottom right
        )

    @property
    def height(self):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        height = y2 - y1  # Calculate difference between points
        return height

    @height.setter
    def height(self, new_height):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            x1, y1,  # top left
            x2, y1 + new_height  # bottom right
        )

    @property
    def centre(self):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        half_width = self.width // 2
        half_height = self.height // 2
        centre = (x1 + half_width, y1 + half_height)
        return centre  # (cx, cy)

    @centre.setter
    def centre(self, centre):
        cx, cy = centre
        half_width = self.width // 2
        half_height = self.height // 2
        self.__canvas.coords(
            self.__rect,
            cx - half_width,
            cy - half_height,
            cx + half_width,
            cy + half_height,
        )

    def move(self, difference):
        dx, dy = difference
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,
            x1 + dx, y1 + dy,
            x2 + dx, y2 + dy,
            )


def main():
    root = tk.Tk()
    root.title("Bakery vs. Pests")
    root.resizable(False, False)

    # Create the world canvas to store our rects coordinates
    canvas = tk.Canvas(root, width=900, height=600, bg="#fdf3e1", highlightthickness=0)
    # Places canvas widget inside parent window as tk is designed for menus
    canvas.pack()

    # === GAME OBJECTS ===
    square1 = Rectangle(canvas, 40, 40, "#e07a5f")
    square2 = Rectangle(canvas, 40, 40, "#e07a5f")

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
