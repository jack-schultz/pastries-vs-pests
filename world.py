from __future__ import annotations
import time
import tkinter as tk
from pest import Pest
from flour import Flour
from projectile import Projectile
from garden import Garden
from inventory import Inventory


class World:
    # Owns the board objects that are drawn on the canvas: the garden, the inventory, the flour counter, pests, flours and projectiles
    def __init__(self, canvas: tk.Canvas, flour: int, width: int) -> None:
        self.canvas = canvas
        self.width = width
        self.garden = Garden(canvas, 40, 120)
        self.inventory = Inventory(canvas, 120, 20)

        # === PEST SETTINGS ===
        self.ant_spawn_interval: float = 10  # seconds between ant spawns
        self.last_ant_spawn: float = time.monotonic()

        # === GAME OBJECTS ===
        self.pests: list[Pest] = []
        self.flours: list[Flour] = []
        self.projectiles: list[Projectile] = []

        # Text in top left to display flour count
        self.flour_text = canvas.create_text(
            10, 10,
            text=f"{flour}",  # amount of flour
            anchor="nw",  # top-left of the text sits at (10, 10)
            font=("Arial", 90, "bold"),
            fill="#3d405b",
        )

    def update_flour_count(self, flour: int) -> None:
        self.canvas.itemconfig(self.flour_text, text=f"{flour}")

    def add_goods(self, new_objs) -> None:
        # Routes the flour and projectiles made by goods to their lists
        for obj in new_objs:
            if isinstance(obj, Flour):
                self.flours.append(obj)
            elif isinstance(obj, Projectile):
                self.projectiles.append(obj)

    def _pest_at(self, projectile: Projectile) -> Pest | None:
        # Returns the first pest the projectile is overlapping, if any
        for pest in self.pests:
            if projectile.hits(pest):
                return pest
        return None

    def spawn_ant_if_due(self) -> None:
        # Spawn an ant on the right edge of a random row
        if time.monotonic() - self.last_ant_spawn >= self.ant_spawn_interval:
            self.last_ant_spawn = time.monotonic()
            self.pests.append(self.garden.spawn_ant(self.width))

    def update_pests(self) -> None:
        # Pests walk left unless blocked by a good, which they attack instead
        for pest in list(self.pests):
            blocking_tile = self.garden.tile_blocking(pest)
            # Colliding with a tile which has a good
            if blocking_tile and blocking_tile.good:
                # Check the good blocking the pest is valid
                blocking_good = blocking_tile.good
                if not blocking_good:
                    continue
                # Pest attacks good till its dead
                pest.attack(blocking_good)
                if blocking_good.is_dead:
                    blocking_good.destroy()
                    blocking_tile.clear_good()
            else:
                # If not colliding, moves
                pest.move()

            # Remove pests that have left the screen
            if pest.has_left_screen():
                pest.destroy()
                self.pests.remove(pest)
            else:
                # Draw pests above goods (flour is raised after, so it stays on top)
                pest.rect.raise_to_top()

    def update_projectiles(self) -> None:
        # projectiles fly right and damage the first pest they touch
        for projectile in list(self.projectiles):
            projectile.move()
            hit_pest = self._pest_at(projectile)
            if hit_pest:
                hit_pest.take_damage(projectile.damage)
                if hit_pest.is_dead:
                    hit_pest.destroy()
                    self.pests.remove(hit_pest)
                    projectile.destroy()
                    self.projectiles.remove(projectile)

            # If the projectile goes off the screen, kill it
            elif projectile.rect.x > self.width:
                projectile.destroy()
                self.projectiles.remove(projectile)

            projectile.rect.raise_to_top()

    def raise_flours(self) -> None:
        # Draw flour on top of everything else
        for obj in self.flours:
            if isinstance(obj, Flour):
                obj.rect.raise_to_top()

    def collect_flour_at(self, pos: tuple[int, int]) -> int:
        # Collects every flour under the click and returns their total amount
        total = 0
        for flour in list(self.flours):
            if not flour.rect.collide_point(point=pos):
                continue

            # Collecting removes it from the canvas and returns its amount
            total += flour.collect()
            self.flours.remove(flour)
        return total
