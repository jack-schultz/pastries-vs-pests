from __future__ import annotations
import time
from app.rectangle import Rectangle
from levels.level_collector import LevelCollector, pest_ids
from levels.wave_manager import WaveManager
from entities.living.pests.base_pest import BasePest
from entities.flour import Flour
from entities.projectiles.projectile import Projectile
from entities.garden import Garden
from entities.cardholder import CardHolder
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.window import Window

initial_flour = 500


class World:
    # Owns the board objects that are drawn on the canvas: the garden, the inventory, the flour counter, pests, flours and projectiles
    def __init__(self, window: Window) -> None:
        self.window = window
        self.garden = Garden(self.window.canvas, 40, 120)
        self.card_holder = CardHolder(self.window.canvas, 180, 20)

        # === LEVEL SETTINGS ===
        self.level_collector = LevelCollector()
        self.level_number = 1
        self.waves = WaveManager(self.level_collector.get_level(self.level_number), pest_ids)
        self.next_button: Rectangle | None = None  # shown once a level is complete
        self.game_over = False  # set when a pest reaches the left of the screen

        # === GAME OBJECTS ===
        self.pests: list[BasePest] = []
        self.flours: list[Flour] = []
        self.projectiles: list[Projectile] = []

        self.flour: int = initial_flour  # This is the currency to make pastry goods

        # Text in top left to display flour count
        self.flour_text = self.window.canvas.create_text(
            10, 20,
            text=f"{self.flour}",  # amount of flour
            anchor="nw",  # top-left of the text sits at (10, 10)
            font=("Arial", 70, "bold"),
            fill="#3d405b",
        )

        # Text in top right to display the wave
        self.wave_text = self.window.canvas.create_text(
            self.window.width - 10, 20,
            text="",
            anchor="ne",
            font=("Arial", 24, "bold"),
            fill="#3d405b",
        )

    def update_flour(self) -> None:
        for flour in list(self.flours):
            flour.move()
            if flour.finished_move():
                self.flour += flour.amount
                self.flours.remove(flour)
        # Update flour counter
        self.window.canvas.itemconfig(self.flour_text, text=f"{self.flour}")

    def add_goods(self, new_objs) -> None:
        # Routes the flour and projectiles made by goods to their lists
        for obj in new_objs:
            if isinstance(obj, Flour):
                self.flours.append(obj)
            elif isinstance(obj, Projectile):
                self.projectiles.append(obj)

    def __pest_at(self, projectile: Projectile) -> BasePest | None:
        # Returns the first pest the projectile is overlapping, if any
        for pest in self.pests:
            if projectile.hits(pest):
                return pest
        return None

    def spawn_pest_if_due(self) -> None:
        # The current wave decides which pest spawns on the right edge of a random row
        pest_class = self.waves.next_pest(time.monotonic(), len(self.pests))
        if pest_class:
            self.pests.append(self.garden.spawn_pest(pest_class, self.window.width))
        self.update_wave_text()

    def update_wave_text(self) -> None:
        if self.waves.finished:
            text = "Winner Winner Chicken Dinner!"
        elif self.waves.wave_number == 0:
            text = f"Level {self.level_number} - Get ready"
        else:
            text = f"Level {self.level_number} - Wave {self.waves.wave_number}/{self.waves.total_waves}"
        self.window.canvas.itemconfig(self.wave_text, text=text)

        # Offer the next level once this one is complete, if there is one
        has_next = self.level_number < self.level_collector.level_count()
        if self.waves.finished and has_next and self.next_button is None:
            self.next_button = Rectangle(self.window.canvas, 350, 300, 200, 70, "#3d405b")
            self.next_button.set_text("Next Level", colour="#ffffff", size=16)

    def start_next_level(self) -> None:
        # Clears the goods off the garden, then loads the next level's waves
        for tile in self.garden.tiles:
            if tile.good:
                tile.good.destroy()
                tile.clear_good()

        # Clear world values
        self.flour = initial_flour
        self.flours.clear()
        self.projectiles.clear()
        self.pests.clear()

        if self.next_button:
            self.next_button.delete()
            self.next_button = None

        self.level_number += 1
        self.waves = WaveManager(self.level_collector.get_level(self.level_number), pest_ids)
        self.update_wave_text()

    def clicked_next_button(self, pos: tuple[int, int]) -> bool:
        return self.next_button is not None and self.next_button.collide_point(pos)

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

            # A pest touching the left edge of the screen means the player loses
            if pest.rect.left <= 0:
                self.game_over = True

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
            hit_pest = self.__pest_at(projectile)
            if hit_pest:
                hit_pest.take_damage(projectile.damage_to_deal())
                projectile.add_hit_pest(hit_pest)  # Stores it in a list so it cant hit the same pest twice
                projectile.piercing -= hit_pest.layer_count

                if hit_pest.is_dead:
                    hit_pest.destroy()
                    self.pests.remove(hit_pest)

                if projectile.piercing <= 0:
                    projectile.destroy()
                    self.projectiles.remove(projectile)

            # If the projectile goes off the screen, kill it
            elif projectile.rect.left > self.window.width:
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
        for flour in list(self.flours):
            if not flour.rect.collide_point(point=pos):
                continue

            # Collecting starts it moving to the flour display
            x1, y1, x2, y2 = self.window.canvas.bbox(self.flour_text)
            flour.click(((x1 + x2) // 2, (y1 + y2) // 2))
