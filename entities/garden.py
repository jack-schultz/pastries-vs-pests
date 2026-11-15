from __future__ import annotations
import random
from entities.living.goods.base_good import BaseGood
from entities.tile import Tile
from entities.entity import Entity
from entities.living.pests.base_pest import BasePest


class Garden(Entity):
    """The grid of tiles that goods are placed on."""
    def __init__(self, canvas, x, y):
        colour = "#FFFF00"
        self.__position = (x, y)
        self.__rows, self.__columns = 5, 9
        self.__grid_size: int = 90
        super().__init__(
            canvas, x, y,
            self.__columns * self.__grid_size,
            self.__rows * self.__grid_size,
            colour
        )
        self.__tiles = self._create_tiles(self.canvas)  # Holds the rects that make up the grid on the floor

    @property
    def position(self):
        return self.__position

    @property
    def tiles(self) -> list[Tile]:
        return self.__tiles

    def _create_tiles(self, canvas):
        positions = []
        x_margin, y_margin = self.position
        colour_a = "#e0fa5f"
        colour_b = "#c8e04a"
        for i in range(self.__columns):  # columns
            for j in range(self.__rows):  # rows
                colour = colour_a if (i + j) % 2 == 0 else colour_b
                positions.append(
                    (
                        x_margin + self.__grid_size * i,
                        y_margin + self.__grid_size * j,
                        colour
                    )
                )

        tiles: list[Tile] = []
        for x, y, colour in positions:
            tiles.append(Tile(canvas, x, y, self.__grid_size, colour))
        return tiles

    def tile_blocking(self, pest: BasePest) -> Tile | None:
        # Returns the tile whose good the pest's left edge has reached, if any
        _, py = pest.rect.centre
        for tile in self.__tiles:
            if not tile.good:
                continue
            if isinstance(tile, Tile) and isinstance(tile.good, BaseGood) and pest.is_blocked_by(tile.good):
                return tile
        return None

    def spawn_pest(self, pest_class, game_width) -> BasePest:
        row = random.randrange(self.__rows)
        # Spawn just off the right edge of the canvas, centred in the row
        centre_y = self.position[1] + self.__grid_size * row + self.__grid_size // 2
        return pest_class(self.canvas, game_width, centre_y)

    def goods_act(self, pests=None):
        # Every good acts on its own timer; flour and projectiles it makes are routed to the right list
        new_objs = []
        for tile in list(self.__tiles):
            if not isinstance(tile, Tile):
                continue

            if not tile.good:
                continue

            # Stunned goods (hit by a Basher) do nothing until it wears off
            if not tile.good.can_act():
                continue

            new_objs.append(tile.good.act(self.canvas, pests))

        return new_objs
