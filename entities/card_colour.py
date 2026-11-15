from __future__ import annotations
from enum import Enum


class CardColour(Enum):
    """Colours used to draw cards."""
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
