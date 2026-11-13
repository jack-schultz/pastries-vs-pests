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
        # Every item drawn for this rect (label and added sprite shapes) shares this tag,
        # so they can be moved, raise and delete together
        self.__tag = f"group{self.__rect}"
        self.__canvas.addtag_withtag(self.__tag, self.__rect)

    @property
    def canvas(self):
        return self.__canvas

    def set_colour(self, colour: str) -> None:
        self.__canvas.itemconfig(self.__rect, fill=colour)

    def set_outline(self, colour: str, width: int = 1) -> None:
        self.__canvas.itemconfig(self.__rect, outline=colour, width=width)

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
            tags=(self.__tag,),
        )

    def hide_hitbox(self) -> None:
        # Hides the rect itself but keeps it as a hitbox, for entities drawn with shapes instead
        self.__canvas.itemconfig(self.__rect, fill="", outline="")

    def draw(self, kind: str, *coords: float, **options) -> int:
        """
        Draws an extra shape that shares the same tag with this rect.
        Accepted shapes: ("oval", "rectangle", "polygon", "line", "arc", "text")
        """
        # makes sure the string passed in is a valid canvas object
        create = getattr(self.__canvas, f"create_{kind}")
        return create(*coords, tags=(self.__tag,), **options)

    def __centre_text(self) -> None:
        # Keep the label centred on the rect whenever the rect moves or resizes
        if self.__text is None:
            return
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(self.__text, (x1 + x2) / 2, (y1 + y2) / 2)

    @property
    def left(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return x1

    @left.setter
    def left(self, new_x) -> None:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,  # rect on canvas to edit
            new_x, y1,  # top left
            new_x + self.w, y2  # bottom right
        )

    @property
    def l(self) -> float:
        return self.left

    @l.setter
    def l(self, new_x) -> None:
        self.left = new_x

    @property
    def right(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return x2

    @right.setter
    def right(self, new_x) -> None:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,
            new_x - self.w, y1,  # top left
            new_x, y2  # bottom right
        )

    @property
    def r(self) -> float:
        return self.right

    @r.setter
    def r(self, new_x) -> None:
        self.right = new_x

    @property
    def top(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return y1

    @top.setter
    def top(self, new_y) -> None:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,
            x1, new_y,  # top left
            x2, new_y + self.h  # bottom right
        )

    @property
    def t(self) -> float:
        return self.top

    @t.setter
    def t(self, new_y: float) -> None:
        self.top = new_y

    @property
    def bottom(self) -> float:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        return y2

    @bottom.setter
    def bottom(self, new_y) -> None:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        self.__canvas.coords(
            self.__rect,
            x1, new_y - self.h,  # top left
            x2, new_y  # bottom right
        )

    @property
    def b(self) -> float:
        return self.bottom

    @b.setter
    def b(self, new_y: float) -> None:
        self.bottom = new_y

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

    @w.setter
    def w(self, new_width: float) -> None:
        self.width = new_width

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

    @h.setter
    def h(self, new_height: float) -> None:
        self.height = new_height

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
    def c(self) -> tuple[float, float]:
        return self.centre

    @c.setter
    def c(self, centre: tuple[float, float]) -> None:
        self.centre = centre

    @property
    def centre_right(self):
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        half_height = self.height // 2
        centre_right = (x2, y1 + half_height)
        return centre_right

    @centre_right.setter
    def centre_right(self, centre_right: tuple[float, float]):
        cx, cy = centre_right
        half_height = self.height // 2
        self.__canvas.coords(
            self.__rect,
            cx - self.width,
            cy - half_height,
            cx,
            cy + half_height,
        )
        self.__centre_text()

    @property
    def cr(self):
        return self.centre_right

    @property
    def centre_left(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        half_height = self.height // 2
        centre_left = (x1, y1 + half_height)
        return centre_left

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

    @property
    def cl(self):
        return self.centre_left

    def move(self, difference: tuple[float, float]) -> None:
        # Moves everything with the tag
        dx, dy = difference
        self.__canvas.move(self.__tag, dx, dy)

    def collide_point(self, point: tuple[float, float]) -> bool:
        px, py = point
        x1, y1, x2, y2 = self.__canvas.coords(self.__rect)
        if x1 < px < x2 and y1 < py < y2:
            return True
        else:
            return False

    def raise_to_top(self) -> None:
        self.__canvas.tag_raise(self.__tag)

    def delete(self) -> None:
        self.__canvas.delete(self.__tag)
