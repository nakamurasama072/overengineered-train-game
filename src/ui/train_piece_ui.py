from __future__ import annotations

import math
import tkinter as tk
from typing import TYPE_CHECKING

from engine.comps.color_enums import PlayerColor
from engine.comps.player import Player
from engine.map.route import Route

PIECE_WIDTH = 25   # length of each train piece rectangle
PIECE_HEIGHT = 15   # width of each train piece rectangle
PLACE_DELAY = 120  # ms between each piece appearing


class TrainPieceUI:
    """
    Responsible for rendering a player's claimed train pieces
    along a route on the map canvas.

    build_ui() calculates all piece positions then calls place_pieces()
    to render them one by one with a short delay between each.
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        player: Player,
        route: Route,
        canvas_width: int,
        canvas_height: int,
    ) -> None:
        """
        Constructor.
        :param canvas: The Tkinter canvas to draw on.
        :param player: The player who claimed the route.
        :param route: The claimed route.
        :param canvas_width: Full canvas width in pixels.
        :param canvas_height: Full canvas height in pixels.
        """
        self.__canvas = canvas
        self.__player = player
        self.__route = route
        self.__canvas_width = canvas_width
        self.__canvas_height = canvas_height

    def build_ui(self, city_positions: dict[str, tuple[float, float]]) -> None:
        """
        Calculate evenly spaced piece positions along the route
        and trigger place_pieces() to render them sequentially.
        :param city_positions: Dict mapping city names to relative (rx, ry) positions.
        """
        start = self.__route.get_start_city().get_name()
        dest = self.__route.get_destination_city().get_name()

        if start not in city_positions or dest not in city_positions:
            print(f"TrainPieceUI: city position missing for '{start}' or '{dest}'")
            return

        x1, y1 = self._to_px(*city_positions[start])
        x2, y2 = self._to_px(*city_positions[dest])
        n = self.__route.get_length()
        angle = math.atan2(y2 - y1, x2 - x1)

        positions = []
        for i in range(n):
            t = (i + 0.5) / n
            cx = int(x1 + t * (x2 - x1))
            cy = int(y1 + t * (y2 - y1))
            positions.append((cx, cy))

        self.place_pieces(positions, angle, n)

    def place_pieces(
        self,
        positions: list[tuple[int, int]],
        angle: float,
        count: int,
        index: int = 0,
    ) -> None:
        """
        Place train pieces one at a time, scheduling each appearance
        with a short delay to create a simple sequential effect.
        :param positions: List of (cx, cy) centre points for each piece.
        :param angle: Rotation angle of the route line in radians.
        :param count: Total number of pieces to place.
        :param index: Current piece index being placed.
        """
        if index >= count:
            return

        cx, cy = positions[index]
        self._draw_piece(cx, cy, angle)

        self.__canvas.after(
            PLACE_DELAY,
            lambda: self.place_pieces(positions, angle, count, index + 1),
        )

    def _draw_piece(self, cx: int, cy: int, angle: float) -> None:
        """
        Draw a single rotated train piece rectangle at (cx, cy).
        :param cx: Centre x in pixels.
        :param cy: Centre y in pixels.
        :param angle: Rotation angle in radians.
        """
        color = self.__player.get_color().value
        fg = "#ffffff" if self.__player.get_color() is PlayerColor.BLACK else "#1a1a2e"
        label = self.__player.get_name()[:3].upper()

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        hw = PIECE_WIDTH / 2
        hh = PIECE_HEIGHT / 2

        corners = [
            (cx + cos_a * hw - sin_a * hh, cy + sin_a * hw + cos_a * hh),
            (cx - cos_a * hw - sin_a * hh, cy - sin_a * hw + cos_a * hh),
            (cx - cos_a * hw + sin_a * hh, cy - sin_a * hw - cos_a * hh),
            (cx + cos_a * hw + sin_a * hh, cy + sin_a * hw - cos_a * hh),
        ]

        self.__canvas.create_polygon(
            corners,
            fill=color,
            outline="#ffffff",
            width=1,
        )
        self.__canvas.create_text(
            cx, cy,
            text=label,
            fill=fg,
            font=("Georgia", 5, "bold"),
        )

    def _to_px(self, rx: float, ry: float) -> tuple[int, int]:
        return int(rx * self.__canvas_width), int(ry * self.__canvas_height)