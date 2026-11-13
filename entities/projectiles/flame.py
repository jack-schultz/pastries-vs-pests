from __future__ import annotations
from entities.damage import DamageType
from entities.projectiles.projectile import Projectile


class Flame(Projectile):
    # burns every pest it touches, and disappears after it has fully stretched
    def __init__(self, canvas, left: float, centre_y: float, range_px: float) -> None:
        super().__init__(
            canvas, left, centre_y,
            size=40,
            colour="#ff7043",
            damage=20,
            speed=0,  # the projectile itself doesn't move, it grows, so we overwrite the move method instead
            piercing=10 ** 9,  # never runs out, it hits every pest it touches
            damage_type=DamageType.FIRE,
        )
        self.__range = range_px  # pixels the flame stretches to
        self.__grow_speed = 9  # pixels per frame
        self.__linger_frames = 20  # frames the fully stretched flame stays before going out
        self.__flicker_colours = ("#ff7043", "#ffb300")

        self.__length = 0.0
        self.__frames_full = 0

        # Flame's left edge at the front of the pastry
        self.rect.left = left
        self.rect.top = centre_y - self.rect.height / 2
        self.rect.w = 0

    def move(self) -> None:
        # Stretch to the right until at full range, then linger a few frames
        if self.__length < self.__range:
            self.__length = min(self.__length + self.__grow_speed, self.__range)
            self.rect.w = self.__length
        else:
            self.__frames_full += 1
        # Flicker between two colours so it looks like fire
        self.rect.set_colour(self.__flicker_colours[self.__frames_full % 2])

    def is_expired(self) -> bool:
        return self.__frames_full >= self.__linger_frames

    def __touches(self, pest) -> bool:
        # The flame's whole body counts, not just its tip
        flame, body = self.rect, pest.rect
        return (
            body.left < flame.right and body.right > flame.left
            and body.top < flame.bottom and body.bottom > flame.top
        )
