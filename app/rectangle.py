from __future__ import annotations
import tkinter as tk


class Rectangle:
    def __init__(self, canvas: tk.Canvas, x: float, y: float, width: float, height: float, colour: str):
        self.__canvas = canvas
        self.__rect: int = self.__canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=colour,
            outline="",
        )
        self.__text: int | None = None  # Optional label drawn on top of the rect

    @property
    def canvas(self):
        return self.__canvas

    def set_colour(self, colour: str) -> None:
        self.__canvas.itemconfig(self.__rect, fill=colour)

    def set_text(self, text: str, colour: str = "#3d405b", size: int = 9) -> None:
        if self.__text is not None:
            # Label already there, so just update it
            self.__canvas.itemconfig(self.__text, text=text, fill=colour)
            return
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__text = self.__canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text=text,
            fill=colour,
            font=("Arial", size, "bold"),
            width=(x2 - x1) - 6,  # wrap long names inside the rect
            justify="center",
        )

    def __centre_text(self) -> None:
        # Keep the label centred on the rect whenever the rect moves or resizes
        if self.__text is None:
            return
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(self.__text, (x1 + x2) / 2, (y1 + y2) / 2)

    @property
    def x(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return x1

    @x.setter
    def x(self, new_x) -> None:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            new_x, y1,  # top left
            new_x + self.w, y2  # bottom right
        )

    @property
    def y(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return y1

    @property
    def width(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        width = x2 - x1  # Calculate difference between points
        return width

    @width.setter
    def width(self, new_width: float):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            x1, y1,  # top left
            x1 + new_width, y2  # bottom right
        )
        self.__centre_text()

    @property
    def w(self) -> float:
        return self.width

    @property
    def height(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        height = y2 - y1  # Calculate difference between points
        return height

    @height.setter
    def height(self, new_height: float):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        # x1, y1 is top left
        # x2, y2 is bottom right
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            x1, y1,  # top left
            x2, y1 + new_height  # bottom right
        )
        self.__centre_text()

    @property
    def h(self) -> float:
        return self.height

    @property
    def centre(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        half_width = self.width // 2
        half_height = self.height // 2
        centre = (x1 + half_width, y1 + half_height)
        return centre  # (cx, cy)

    @centre.setter
    def centre(self, centre: tuple[float, float]):
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
        self.__centre_text()

    @property
    def centre_left(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        half_height = self.height // 2
        centreleft = (x1, y1 + half_height)
        return centreleft  # (cx, cy)

    @centre_left.setter
    def centre_left(self, centre_left: tuple[float, float]):
        cx, cy = centre_left
        half_height = self.height // 2
        self.__canvas.coords(
            self.__rect,
            cx,
            cy - half_height,
            cx + self.width,
            cy + half_height,
            )
        self.__centre_text()

    def move(self, difference: tuple[float, float]) -> None:
        dx, dy = difference
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,
            x1 + dx, y1 + dy,
            x2 + dx, y2 + dy,
            )
        self.__centre_text()

    def collide_point(self, point: tuple[float, float]) -> bool:
        px, py = point
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        if x1 < px < x2 and y1 < py < y2:
            return True
        else:
            return False

    def raise_to_top(self) -> None:
        self.__canvas.tag_raise(self.__rect)
        if self.__text is not None:
            self.__canvas.tag_raise(self.__text)

    def delete(self) -> None:
        self.__canvas.delete(self.__rect)
        if self.__text is not None:
            self.__canvas.delete(self.__text)
