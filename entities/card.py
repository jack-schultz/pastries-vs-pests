from __future__ import annotations
from enum import Enum
from typing import Callable, TypedDict
from entities.entity import Entity
from entities.living.goods.base_good import BaseGood
from app.rectangle import Rectangle


class CardColour(Enum):
    READY_FILL = "#e63946"
    HOVER_FILL = "#f25c68"
    SELECTED_FILL = "#ff8a94"
    DISABLED_FILL = "#8d8d8d"
    RECHARGE_FILL = "#7a1d24"
    OVERLAY_FILL = "#3b0d11"
    SELECTED_OUTLINE = "#ffd166"
    HOVER_OUTLINE = "#ffffff"
    TEXT_COLOUR = "#ffffff"
    MEET_COST_COLOUR = "#ffffff"
    SHORT_COST_COLOUR = "#ffb3b3"


class ToolType(Enum):
    GLOVE = "glove"
    BIN = "bin"


# defiles the keys and type hints them for a dict
class ReplaceInfo(TypedDict):  # total=false allows a dict with only 1 key
    replace: Callable[..., BaseGood]
    cost: int


class Card(Entity):
    def __init__(
        self, canvas, x, y,
        width, height, name: str, cost: int,
        good_class: Callable[[Rectangle], BaseGood] | None, cooldown: float = 5.0,
        tool: ToolType | None = None,
        replaces: dict[type[BaseGood], ReplaceInfo] | None = None,
    ) -> None:
        super().__init__(canvas, x, y, width, height, CardColour.READY_FILL.value)
        self.__name = name
        self.__cost = cost
        self.__good_class = good_class
        self.__tool = tool
        # Existing good class -> (good class to spawn in its place, cost of the replacement)
        self.__replaces: dict[type[BaseGood], ReplaceInfo] = replaces or {}
        self.__cooldown_frames = round(cooldown * 60)
        self.__frames_left = 0  # 0 means ready to select

        # Display state, only redrawn when something changes
        self.__flour = 0
        self.__selected = False
        self.__hovered = False
        self.__last_state: tuple | None = None

        # Dark overlay that drains from the top down as the card recharges
        self.__overlay = canvas.create_rectangle(
            x, y, x + width, y,
            fill=CardColour.OVERLAY_FILL.value, outline="", state="hidden",
        )
        # Name across the top
        self.__name_text = canvas.create_text(
            x + width / 2, y + 16,
            text=name, fill=CardColour.TEXT_COLOUR.value,
            font=("Arial", 9, "bold"),
            width=width - 6, justify="center",
        )
        # Cost badge along the bottom, with a little icon representing flour
        badge_h = 20
        self.__badge = canvas.create_rectangle(
            x, y + height - badge_h, x + width, y + height,
            fill="#3d405b", outline="",
        )
        self.__flour_icon = canvas.create_rectangle(
            x + 10, y + height - badge_h / 2 - 5,
            x + 20, y + height - badge_h / 2 + 5,
            fill="#ffffff", outline="",
        )
        self.__cost_text = canvas.create_text(
            x + width / 2 + 6, y + height - badge_h / 2,
            text=str(cost) if cost else "Free", fill=CardColour.MEET_COST_COLOUR.value,
            font=("Arial", 11, "bold"),
        )

        # Free cards have no flour to show, so centre the word instead
        if cost == 0:
            canvas.itemconfig(self.__flour_icon, state="hidden")
            canvas.coords(self.__cost_text, x + width / 2, y + height - badge_h / 2)

        # Reason the card can't be used right now, in the middle of the card
        self.__status_text = canvas.create_text(
            x + width / 2, y + (height - badge_h) / 2 + 12,
            text="", fill=CardColour.TEXT_COLOUR.value,
            font=("Arial", 8, "bold"),
            width=width - 4, justify="center",
        )
        # Border drawn on top of everything so the badge doesn't hide it
        self.__highlight = canvas.create_rectangle(
            x + 1, y + 1, x + width - 1, y + height - 1,
            fill="", outline="", width=0,
        )
        self.__bounds = (x, y, x + width, y + height - badge_h)

        self.__refresh_display()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cost(self) -> int:
        return self.__cost

    @property
    def tool(self) -> ToolType | None:
        return self.__tool

    @property
    def is_ready(self) -> bool:
        return self.__frames_left == 0

    def can_afford(self, flour: int) -> bool:
        return flour >= self.__cost

    def is_usable(self, flour: int) -> bool:
        # Usable means recharged and affordable
        return self.is_ready and self.can_afford(flour)

    def start_cooldown(self) -> None:
        # Called when the card's good is placed, like Plants vs Zombies
        self.__frames_left = self.__cooldown_frames
        self.__refresh_display()

    def tick_cooldown(self) -> None:
        if self.__frames_left > 0:
            self.__frames_left -= 1
            self.__refresh_display()

    def update_display(self, flour: int, selected: bool, hovered: bool) -> None:
        # Called every frame by the card holder so the card reflects the current game state
        self.__flour = flour
        self.__selected = selected
        self.__hovered = hovered
        self.__refresh_display()

    def __refresh_display(self) -> None:
        recharging = not self.is_ready
        affordable = self.can_afford(self.__flour)
        # Round the seconds so the card only redraws when what's shown changes
        state = (
            self.__selected, self.__hovered, affordable, recharging,
            None if affordable else self.__flour,  # "Need N more" changes with flour
            round(self.__frames_left / 6) if recharging else 0,
        )
        if state == self.__last_state:
            return
        self.__last_state = state

        canvas = self.canvas
        x1, y1, x2, y2 = self.__bounds

        # ===== RECHARGING =====
        if recharging:
            self.rect.set_colour(CardColour.RECHARGE_FILL.value)
            canvas.itemconfig(self.__highlight, outline="", width=0)
            # Overlay covers the fraction of the card still recharging
            fraction = self.__frames_left / self.__cooldown_frames
            canvas.coords(self.__overlay, x1, y1, x2, y1 + (y2 - y1) * fraction)
            canvas.itemconfig(self.__overlay, state="normal")
            canvas.itemconfig(
                self.__status_text,
                text=f"Recharging\n{self.__frames_left / 60:.1f}s",
            )
            canvas.itemconfig(
                self.__cost_text,
                fill=CardColour.MEET_COST_COLOUR.value if affordable else CardColour.SHORT_COST_COLOUR.value,
            )
            return

        canvas.itemconfig(self.__overlay, state="hidden")

        # ===== NOT ENOUGH FLOUR =====
        if not affordable:
            self.rect.set_colour(CardColour.DISABLED_FILL.value)
            canvas.itemconfig(self.__highlight, outline="", width=0)
            canvas.itemconfig(
                self.__status_text,
                text=f"Need {self.__cost - self.__flour}\nmore flour",
            )
            canvas.itemconfig(self.__cost_text, fill=CardColour.SHORT_COST_COLOUR.value)
            return

        # ===== USABLE =====
        canvas.itemconfig(self.__status_text, text="")
        canvas.itemconfig(self.__cost_text, fill=CardColour.MEET_COST_COLOUR.value)
        if self.__selected:
            self.rect.set_colour(CardColour.SELECTED_FILL.value)
            canvas.itemconfig(self.__highlight, outline=CardColour.SELECTED_OUTLINE.value, width=4)
            canvas.itemconfig(self.__status_text, text="Selected")
        elif self.__hovered:
            self.rect.set_colour(CardColour.HOVER_FILL.value)
            canvas.itemconfig(self.__highlight, outline=CardColour.HOVER_OUTLINE.value, width=2)
        else:
            self.rect.set_colour(CardColour.READY_FILL.value)
            canvas.itemconfig(self.__highlight, outline="", width=0)

    def can_place_on(self, existing: BaseGood | None) -> bool:
        # Empty tile means any card can be placed
        if existing is None:
            return True

        # Occupied tile means only allowed if this card has a replace fot that good
        good_class = type(existing)
        if good_class in self.__replaces:
            return True

        return False

    def __rule_for(self, existing_good: BaseGood | None) -> ReplaceInfo | None:
        # The replacement rule for this exact good class, if the card has one
        if existing_good is None:
            return None
        # get replaces item from dict by type of existing good
        return self.__replaces.get(type(existing_good))

    def good_class_for(self, existing: BaseGood | None) -> Callable[..., BaseGood] | None:
        # Uses the replacement class when the rule matches, otherwise the card's own good
        rule: ReplaceInfo | None = self.__rule_for(existing)
        if rule:
            return rule["replace"]  # 0 is good class
        return self.__good_class

    def cost_for(self, existing_good: BaseGood | None) -> int:
        # Replacing costs the rule's own price, otherwise the card's normal cost
        rule: ReplaceInfo | None = self.__rule_for(existing_good)
        if rule:
            return rule["cost"]  # 1 is cost
        return self.__cost

    def create_good(self, canvas, x, y, existing: BaseGood | None = None) -> BaseGood | None:
        # The card knows which good it sells, so the caller doesn't need to
        good_class = self.good_class_for(existing)
        if not good_class:
            return None
        return good_class(canvas, x, y)

    def destroy(self) -> None:
        super().destroy()
        for item in (
            self.__name_text, self.__badge, self.__flour_icon,
            self.__cost_text, self.__overlay, self.__status_text,
            self.__highlight
        ):
            self.canvas.delete(item)
