from __future__ import annotations

from enum import Enum


class TrainColor(Enum):
    """
    Represents the color of a train card or route.
    The value is the hex color used for rendering.
    GRAY indicates any single color may be used to claim the route.
    WILD is the locomotive card that acts as a wildcard.
    """
    RED    = "#c0392b"
    BLUE   = "#2980b9"
    GREEN  = "#27ae60"
    YELLOW = "#c9a227"
    BLACK  = "#2c2c2c"
    WHITE  = "#ecf0f1"
    ORANGE = "#d35400"
    PINK   = "#c0678a"
    GRAY   = "#7f8c8d"
    WILD   = "#7f6a4f"


class PlayerColor(Enum):
    """
    Represents the color of a player's train pieces and scoring marker.
    The value is the hex color used for rendering.
    """
    RED    = "#c0392b"
    BLUE   = "#2980b9"
    GREEN  = "#27ae60"
    YELLOW = "#c9a227"
    BLACK  = "#2c2c2c"