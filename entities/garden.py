from __future__ import annotations
import random
from entities.living.goods.base_good import BaseGood
from entities.tile import Tile
from entities.entity import Entity
from entities.living.pests.ant import Ant
from entities.living.pests.base_pest import BasePest


class Garden(Entity):
    def __init__(self, canvas, x, y):
        colour = "#FFFF00"
        self.position = (x, y)
        self.rows, self.columns = 5, 9
        self.grid_size: int = 90
        super().__init__(
            canvas, x, y,
            self.columns * self.grid_size,
            self.rows * self.grid_size,
            colour
        )
        self.tiles = self._create_tiles(self.canvas)  # Holds the rects that make up the grid on the floor

    def _create_tiles(self, canvas):
        positions = []
        x_margin, y_margin = self.position
        colour_a = "#e0fa5f"
        colour_b = "#c8e04a"
        for i in range(self.columns):  # columns
            for j in range(self.rows):  # rows
                colour = colour_a if (i + j) % 2 == 0 else colour_b
                positions.append(
                    (
                        x_margin + self.grid_size * i,
                        y_margin + self.grid_size * j,
                        colour
                    )
                )

        tiles: list[Tile] = []
        for x, y, colour in positions:
            tiles.append(Tile(canvas, x, y, self.grid_size, colour))
        return tiles

    def tile_blocking(self, pest: BasePest) -> Tile | None:
        # Returns the tile whose good the pest's left edge has reached, if any
        _, py = pest.rect.centre
        for tile in self.tiles:
            if not tile.good:
                continue
            if isinstance(tile, Tile) and isinstance(tile.good, BaseGood) and pest.is_blocked_by(tile.good):
                return tile
        return None

    def spawn_ant(self, game_width) -> Ant:
        row = random.randrange(self.rows)
        # Spawn just off the right edge of the canvas, centred in the row
        centre_y = self.position[1] + self.grid_size * row + self.grid_size // 2
        return Ant(self.canvas, game_width, centre_y)

    def goods_act(self):
        # Every good acts on its own timer; flour and projectiles it makes are routed to the right list
        new_objs = []
        for tile in list(self.tiles):
            if not isinstance(tile, Tile):
                continue

            if not tile.good:
                continue

            new_objs.append(tile.good.act(self.canvas))

        return new_objs
