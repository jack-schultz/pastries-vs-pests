from __future__ import annotations
import time
import tkinter as tk
from pest import Pest
from card import Card
from flour import Flour
from projectile import Projectile
from tile import Tile
from garden import Garden
from inventory import Inventory


class Window:
    # Holds the Tk window and the canvas everything is drawn on
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bakery vs. Pests")
        self.root.resizable(False, False)

        self.width, self.height = (900, 600)

        # Create the world canvas to store our rects coordinates
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus so it needs this
        self.canvas.pack()

    def run(self) -> None:
        self.root.mainloop()


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


class Game:
    # Holds the game state and rules. Draws onto the window it is given
    def __init__(self) -> None:
        self.window = Window()

        # === INPUT VARIABLES ===
        self.mouse_pos: tuple[int, int] | None = None
        self.selected_card: Card | None = None

        # === GAME VARIABLES ===
        self.flour: int = 50  # This is the currency to make bakery goods

        # === GAME OBJECTS ===
        self.world = World(self.window.canvas, self.flour, self.window.width)

    def _create_game_loop(self) -> None:
        # ========== GAME LOOP =========
        def update():
            # Code which runs every frame goes here
            self.world.update_flour_count(self.flour)

            # ===== GOODS ACT =====
            self.world.add_goods(self.world.garden.goods_act())

            # ===== SPAWN ANTS =====
            self.world.spawn_ant_if_due()

            # ===== PESTS WALK =====
            self.world.update_pests()

            # ===== MOVE PROJECTILES =====
            self.world.update_projectiles()

            # ===== DRAW FLOUR ON TOP  =====
            self.world.raise_flours()

            self.window.root.after(16, update)  # run again in about 16 ms (~60 FPS)

        update()

        # === EVENTS ===
        def on_motion(event: tk.Event) -> None:
            self.mouse_pos = (event.x, event.y)

        def on_click(event: tk.Event) -> None:
            pos = (event.x, event.y)

            # ===== CHECK CLICK POS =====
            # Loop through all clickable (tile, card & flour) objects to find which was clicked
            for tile in list(self.world.garden.tiles):
                if not tile.rect.collide_point(point=pos):
                    continue

                if not isinstance(tile, Tile):
                    continue

                if not self.selected_card:
                    continue

                # Skip if tile already has a good
                if not tile.is_empty:
                    self.selected_card = None
                    continue

                # Skip if not enough flour
                if self.flour < self.selected_card.cost:
                    self.selected_card = None
                    continue

                # Create new good on the tiles
                tile.good = self.selected_card.create_good(
                    self.window.canvas, tile.rect.x + 10, tile.rect.y + 10, tile.rect.w - 20, tile.rect.h - 20
                )

                # Take flour amount and reset selected card
                self.flour -= self.selected_card.cost
                self.selected_card = None

            for card in list(self.world.inventory.cards):
                if not card.rect.collide_point(point=pos):
                    continue

                if not isinstance(card, Card):
                    continue

                # If card is already selected, deselect
                if self.selected_card == card:
                    self.selected_card = None
                    continue

                # Select card
                self.selected_card = card

            self.flour += self.world.collect_flour_at(pos)

        self.window.canvas.bind("<Motion>", on_motion)  # Mouse movement
        self.window.canvas.bind("<Button-1>", on_click)  # Left mouse click

    def run(self) -> None:
        self._create_game_loop()
        self.window.run()


# # ===== TESTS =====
# game = Game()
# canvas = game.canvas
# results: list[tuple[str, bool]] = []
#
#
# def check(name: str, passed: bool) -> None:
#     results.append((name, passed))
#     print(f"{'PASS' if passed else 'FAIL'}: {name}")
#
#
# print("=== Rectangle ===")
# rect = Rectangle(canvas, 10, 20, 30, 40, "#000000")
# check("rect x/y", (rect.x, rect.y) == (10, 20))
# check("rect w/h", (rect.w, rect.h) == (30, 40))
# check("rect centre", rect.centre == (25, 40))
# rect.move((5, 5))
# check("rect move", (rect.x, rect.y) == (15, 25))
# check("rect collide inside", rect.collide_point((20, 30)))
# check("rect collide outside", not rect.collide_point((0, 0)))
# rect.delete()
#
# print("=== Living ===")
# living = Living(canvas, 0, 0, 10, 10, "#000000", health=20)
# living.take_damage(5)
# check("living health after 5 damage", living.health == 15)
# check("living alive at 15", not living.is_dead)
# living.take_damage(20)
# check("living dead after 20 more damage", living.is_dead)
#
# print("=== Tile ===")
# tile = Tile(canvas, 0, 0, 90, "#ffffff")
# check("tile starts empty", tile.is_empty)
# first = FlourFlower(canvas, 0, 0, 70, 70)
# tile.good = first
# check("tile accepts first good", tile.good is first)
# tile.good = SugarShooter(canvas, 0, 0, 70, 70)
# check("tile rejects second good", tile.good is first)
# tile.clear_good()
# check("tile empty after clear_good", tile.is_empty)
#
# print("=== Flour ===")
# flour = Flour(canvas, 100, 100, amount=25)
# check("flour amount", flour.amount == 25)
# check("flour collect returns amount", flour.collect() == 25)
#
# print("=== Card ===")
# card = Card(canvas, 0, 0, 70, 85, name="The Flour Flower", cost=50, good_class=FlourFlower)
# check("card name", card.name == "The Flour Flower")
# check("card cost", card.cost == 50)
# check("card creates FlourFlower", isinstance(card.create_good(canvas, 0, 0, 70, 70), FlourFlower))
#
# print("=== Goods ===")
# flower = FlourFlower(canvas, 100, 100, 70, 70)
# check("flower waits before first spawn", flower.act(canvas) is None)
# flower._Good__last_action = -1000.0  # Fake the timer so the interval has passed
# check("flower spawns Flour when ready", isinstance(flower.act(canvas), Flour))
#
# shooter = SugarShooter(canvas, 100, 100, 70, 70)
# shooter._Good__last_action = -1000.0
# shot = shooter.act(canvas)
# check("shooter fires Projectile when ready", isinstance(shot, Projectile))
# check("projectile damage is 20", shot.damage == 20)
#
# print("=== Pests ===")
# ant = Ant(canvas, 800, 100)
# check("ant health is 200", ant.health == 200)
# ant.move()
# check("ant moves left", ant.rect.x == 800 - ant.speed)
# check("ant off screen", Ant(canvas, -100, 0).has_left_screen())
# check("ant on screen", not ant.has_left_screen())
#
# blocker = FlourFlower(canvas, 100, 100, 70, 70)  # Centre (135, 135)
# check("ant blocked by good", Ant(canvas, 150, 110).is_blocked_by(blocker))
# check("ant not blocked when far", not Ant(canvas, 300, 110).is_blocked_by(blocker))
#
# victim = FlourFlower(canvas, 100, 100, 70, 70)
# ant = Ant(canvas, 150, 110)
# ant._Pest__last_attack = -1000.0  # Start with the attack timer already expired
# ant.attack(victim)
# ant.attack(victim)  # Second hit is inside the attack interval, so it should do nothing
# check("ant attack respects interval", victim.health == 200)
#
# print("=== Projectile ===")
# shot = Projectile(canvas, 200, 200, size=14, colour="#ff8fab", damage=10, speed=6)
# check("projectile starts at x 213", shot.rect.x == 213)
# shot.move()
# check("projectile moves right", shot.rect.x == 219)
# check("projectile hits pest in path", shot.hits(Ant(canvas, 210, 180)))
# check("projectile misses far pest", not shot.hits(Ant(canvas, 600, 0)))
#
# print("=== Game lists ===")
# check("tile count is rows * columns", len(game.tiles) == game.rows * game.columns)
# check("all tiles start empty", all(t.is_empty for t in game.tiles))
# check("starting flour is 50", game.flour == 50)
# check("pest/flour/projectile lists start empty", not (game.pests or game.flours or game.projectiles))
# check("cards match card_attributes", [c.name for c in game.cards] == [a[0] for a in game.card_attributes])
# check("cards_count matches card_attributes", game.cards_count == len(game.card_attributes))
#
# game._spawn_ant()
# check("spawn adds one ant", len(game.pests) == 1)
# check("spawned ant starts off right edge", game.pests[0].rect.x == game.width)
#
# game.tiles[0].good = FlourFlower(canvas, 50, 130, 70, 70)
# blocker_ant = Ant(canvas, 110, 140)
# check("pest finds blocking tile", game._tile_blocking(blocker_ant) is game.tiles[0])
# check("pest finds no tile in empty row", game._tile_blocking(Ant(canvas, 500, 500)) is None)
#
# passed = sum(1 for _, ok in results if ok)
# print(f"=== {passed}/{len(results)} checks passed ===")
# game.root.destroy()


game = Game()
game.run()
