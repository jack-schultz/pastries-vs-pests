from __future__ import annotations
from entities.entity import Entity
from entities.damage import Damage
from armour.base_armour import BaseArmour


class Living(Entity):
    """Base class for entities with health that can be hurt and die."""

    def __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            colour,
            health: int,
            armour: BaseArmour | None = None,
            layer_count: int = 1) -> None:
        super().__init__(canvas, x, y, width, height, colour)
        self.__health = health
        self.__max_health = health
        self.__armour = armour
        self.__layer_count = layer_count
        # Canvas ids of the bar's background and fill.
        self.__health_bar: tuple[int, int] | None = None

    @property
    def health(self) -> int:
        return self.__health

    @property
    def max_health(self) -> int:
        return self.__max_health

    @max_health.setter
    def max_health(self, new_max_health):
        health_fraction = self.__health / self.__max_health
        self.__max_health = new_max_health
        self.__health = round(health_fraction * new_max_health)

    @property
    def armour(self) -> BaseArmour | None:
        return self.__armour

    @property
    def layer_count(self) -> int:
        # Pests and armour have layers. Sum both (exclude broken armour)
        # and remove from piercing value.
        if self.__armour is not None and not self.__armour.is_broken:
            return self.__layer_count + self.__armour.layer_count
        return self.__layer_count

    @property
    def is_dead(self) -> bool:
        return self.__health <= 0

    def take_damage(self, damage: Damage | float) -> None:
        # If a float comes through, treat it as default damage.
        if not isinstance(damage, Damage):
            damage = Damage(damage)

        remaining = damage.amount
        if self.__armour is not None:
            remaining = self.__armour.absorb(damage)
        self.__health -= remaining
        self.__update_health_bar()
        self._on_damaged()

    def _on_damaged(self) -> None:
        # Subclasses cam change how they look after being hit So they
        # can flash red or similar.
        pass

    def __update_health_bar(self) -> None:
        # A small bar above the entity. Shows once it has been hurt.
        if self.is_dead:
            return

        left, top = self.rect.left, self.rect.top
        width = self.rect.w
        if self.__health_bar is None:
            # Create the health bar on first hit.
            background = self.rect.draw(
                "rectangle", left, top - 9, left + width, top - 4,
                fill="#3d405b", outline="")
            fill = self.rect.draw(
                "rectangle", left, top - 9, left + width, top - 4,
                fill="#4caf50", outline="")
            self.__health_bar = (background, fill)

        _, fill = self.__health_bar
        fraction = max(0.0, self.__health / self.__max_health)

        # The fill shrinks to match the remaining health.
        canvas = self.canvas
        # Get points, _ is what we are updating.
        x1, y1, _, y2 = canvas.coords(self.__health_bar[0])
        canvas.coords(fill, x1, y1, x1 + width * fraction, y2)

        # Set colour based on percentage.
        if fraction > 0.6:
            colour = "#4caf50"
        elif fraction > 0.3:
            colour = "#ffb300"
        else:
            colour = "#e53935"
        canvas.itemconfig(fill, fill=colour)
