
class Rectangle:
    def __init__(self, canvas, x, y, width, height, colour):
        self.__canvas = canvas
        self.__rect = self.__canvas.create_rectangle(
            x, y, x + width, y + height,
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

    def collide_point(self, point: tuple[int, int]):
        px, py = point
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        if x1 < px < x2 and y1 < py < y2:
            return True
        else:
            return False

    def raise_to_top(self):
        self.__canvas.tag_raise(self.__rect)

    def delete(self):
        self.__canvas.delete(self.__rect)
