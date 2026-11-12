from __future__ import annotations
import time
from app.rectangle import Rectangle
from levels.level_collector import LevelCollector, pest_ids
from levels.wave_manager import WaveManager
from entities.living.pests.base_pest import BasePest
from entities.flour import Flour
from entities.projectiles.projectile import Projectile
from entities.living.goods.popping_candy import PoppingCandy
from entities.living.goods.profiterole import Profiterole
from entities.garden import Garden
from entities.cardholder import CardHolder
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.window import Window

initial_flour = 75


class World:
    # Owns the board objects that are drawn on the canvas: the garden, the inventory, the flour counter, pests, flours and projectiles
    def __init__(self, window: Window, level_number: int = 1) -> None:
        self.__window = window
        self.__garden = Garden(self.__window.canvas, 40, 120)
        self.__card_holder = CardHolder(self.__window.canvas, 180, 20)

        # === LEVEL SETTINGS ===
        self.__level_collector = LevelCollector()
        self.__level_number = level_number
        self.__waves = WaveManager(self.__level_collector.get_level(self.__level_number), pest_ids)
        self.__next_button: Rectangle | None = None  # shown once a level is complete
        self.__game_over = False  # set when a pest reaches the left of the screen

        # === GAME OBJECTS ===
        self.__pests: list[BasePest] = []
        self.__flours: list[Flour] = []
        self.__projectiles: list[Projectile] = []

        self.__flour: int = initial_flour  # This is the currency to make pastry goods

        # Text in top left to display flour count
        self.__flour_text = self.__window.canvas.create_text(
            10, 20,
            text=f"{self.__flour}",  # amount of flour
            anchor="nw",  # top-left of the text sits at (10, 10)
            font=("Arial", 70, "bold"),
            fill="#3d405b",
        )

        # Text in top right to display the wave
        self.__wave_text = self.__window.canvas.create_text(
            self.__window.width - 10, 20,
            text="",
            anchor="ne",
            font=("Arial", 24, "bold"),
            fill="#3d405b",
        )

    @property
    def garden(self) -> Garden:
        return self.__garden

    @property
    def card_holder(self) -> CardHolder:
        return self.__card_holder

    @property
    def level_number(self) -> int:
        return self.__level_number

    @property
    def game_over(self) -> bool:
        return self.__game_over

    @property
    def flour(self) -> int:
        return self.__flour

    @flour.setter
    def flour(self, value: int) -> None:
        self.__flour = value

    def tick(self) -> None:
        self.update_flour()

        # ===== RECHARGE CARDS =====
        self.__card_holder.update_cooldowns()

        # ===== GOODS ACT =====
        self.add_goods(self.__garden.goods_act(self.__pests))

        # ===== BOMBES GO OFF =====
        self.update_bombes()

        # ===== SPAWN ANTS =====
        self.spawn_pest_if_due()

        # ===== PESTS WALK =====
        self.update_pests()

        # ===== MOVE PROJECTILES =====
        self.update_projectiles()

        # ===== DRAW FLOUR ON TOP  =====
        self.raise_flours()

    def update_flour(self) -> None:
        for flour in list(self.__flours):
            flour.move()
            if flour.finished_move():
                self.__flour += flour.amount
                self.__flours.remove(flour)
        # Update flour counter
        self.__window.canvas.itemconfig(self.__flour_text, text=f"{self.__flour}")

    def add_goods(self, new_objs) -> None:
        # Routes the flour and projectiles made by goods to their lists
        for obj in new_objs:
            if isinstance(obj, Flour):
                self.__flours.append(obj)
            elif isinstance(obj, Projectile):
                self.__projectiles.append(obj)

    def __pest_at(self, projectile: Projectile) -> BasePest | None:
        # Returns the first pest the projectile is overlapping, if any
        for pest in self.__pests:
            if projectile.hits(pest):
                return pest
        return None

    def spawn_pest_if_due(self) -> None:
        # The current wave decides which pest spawns on the right edge of a random row
        pest_class = self.__waves.next_pest(time.monotonic(), len(self.__pests))
        if pest_class:
            self.__pests.append(self.__garden.spawn_pest(pest_class, self.__window.width))
        self.update_wave_text()

    def update_wave_text(self) -> None:
        if self.__waves.finished:
            text = "Winner Winner Chicken Dinner!"
        elif self.__waves.wave_number == 0:
            text = f"Level {self.__level_number} - Get ready"
        else:
            text = f"Level {self.__level_number} - Wave {self.__waves.wave_number}/{self.__waves.total_waves}"
        self.__window.canvas.itemconfig(self.__wave_text, text=text)

        # Offer the next level once this one is complete, if there is one
        has_next = self.__level_number < self.__level_collector.level_count()
        if self.__waves.finished and has_next and self.__next_button is None:
            self.__next_button = Rectangle(self.__window.canvas, 350, 300, 200, 70, "#3d405b")
            self.__next_button.set_text("Next Level", colour="#ffffff", size=16)

    def start_next_level(self) -> None:
        # Clears the goods off the garden, then loads the next level's waves
        for tile in self.__garden.tiles:
            if tile.good:
                tile.good.destroy()
                tile.clear_good()

        # Clear world values
        self.__flour = initial_flour
        self.__flours.clear()
        self.__projectiles.clear()
        self.__pests.clear()

        if self.__next_button:
            self.__next_button.delete()
            self.__next_button = None

        self.__level_number += 1
        self.__waves = WaveManager(self.__level_collector.get_level(self.__level_number), pest_ids)
        self.update_wave_text()

    def clicked_next_button(self, pos: tuple[int, int]) -> bool:
        return self.__next_button is not None and self.__next_button.collide_point(pos)

    def update_bombes(self) -> None:
        # Cherry Bombes explode on their own once their fuse runs out
        for tile in self.__garden.tiles:
            good = tile.good
            if isinstance(good, Profiterole) and good.is_primed:
                for hit_pest in good.detonate(self.__pests):
                    if hit_pest.is_dead:
                        hit_pest.destroy()
                        self.__pests.remove(hit_pest)
                good.destroy()
                tile.clear_good()

    def update_pests(self) -> None:
        # Pests walk left unless blocked by a good, which they attack instead
        for pest in list(self.__pests):
            if pest not in self.__pests:  # already killed by a mine this frame
                continue
            blocking_tile = self.__garden.tile_blocking(pest)
            # Colliding with a tile which has a good
            if blocking_tile and blocking_tile.good:
                # Check the good blocking the pest is valid
                blocking_good = blocking_tile.good
                if not blocking_good:
                    continue

                # An armed mine goes off instead of being eaten
                if isinstance(blocking_good, PoppingCandy) and blocking_good.is_armed:
                    for hit_pest in blocking_good.detonate(self.__pests):
                        if hit_pest.is_dead:
                            hit_pest.destroy()
                            self.__pests.remove(hit_pest)
                    blocking_good.destroy()
                    blocking_tile.clear_good()
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
                self.__game_over = True

            # Remove pests that have left the screen
            if pest.has_left_screen():
                pest.destroy()
                self.__pests.remove(pest)
            else:
                # Draw pests above goods (flour is raised after, so it stays on top)
                pest.rect.raise_to_top()

    def update_projectiles(self) -> None:
        # projectiles fly right and damage the first pest they touch
        for projectile in list(self.__projectiles):
            projectile.move()
            hit_pest = self.__pest_at(projectile)
            if hit_pest:
                hit_pest.take_damage(projectile.damage_to_deal())
                projectile.add_hit_pest(hit_pest)  # Stores it in a list so it cant hit the same pest twice
                projectile.piercing -= hit_pest.layer_count

                if hit_pest.is_dead:
                    hit_pest.destroy()
                    self.__pests.remove(hit_pest)

                if projectile.piercing <= 0:
                    projectile.destroy()
                    self.__projectiles.remove(projectile)

            # If the projectile goes off the screen, kill it
            elif projectile.rect.left > self.__window.width:
                projectile.destroy()
                self.__projectiles.remove(projectile)

            projectile.rect.raise_to_top()

    def raise_flours(self) -> None:
        # Draw flour on top of everything else
        for obj in self.__flours:
            if isinstance(obj, Flour):
                obj.rect.raise_to_top()

    def collect_flour_at(self, pos: tuple[int, int]) -> int:
        # Collects every flour under the click and returns their total amount
        for flour in list(self.__flours):
            if not flour.rect.collide_point(point=pos):
                continue

            # Collecting starts it moving to the flour display
            x1, y1, x2, y2 = self.__window.canvas.bbox(self.__flour_text)
            flour.click(((x1 + x2) // 2, (y1 + y2) // 2))
