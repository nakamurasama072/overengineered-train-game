from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ui.train_piece_ui import TrainPieceUI
from engine.map.board import Board
from engine.comps.player import Player
from engine.map.route import Route
from ui.user_interface import UserInterface

# Approximate positions for the London map (relative 0.0-1.0).
CITY_POSITIONS: dict[str, tuple[float, float]] = {
    "Regent's Park":      (0.22, 0.08),
    "King's Cross":       (0.51, 0.08),
    "Brick Lane":         (0.91, 0.19),
    "Baker Street":       (0.11, 0.26),
    "British Museum":     (0.39, 0.41),
    "The Charterhouse":   (0.69, 0.25),
    "St Paul's":          (0.73, 0.50),
    "Tower of London":    (0.94, 0.50),
    "Piccadilly Circus":  (0.33, 0.61),
    "Covent Garden":      (0.49, 0.54),
    "Trafalgar Square":   (0.46, 0.69),
    "Waterloo":           (0.64, 0.70),
    "Globe Theatre":      (0.81, 0.73),
    "Elephant & Castle":  (0.84, 0.92),
    "Hyde Park":          (0.10, 0.79),
    "Buckingham Palace":  (0.27, 0.90),
    "Big Ben":            (0.47, 0.83),
}

BG_MAP    = "#1e2d40"

PIECE_WIDTH = 18
PIECE_HEIGHT = 10
CITY_FILL = "#c9a227"
CITY_OUT  = "#f0e6c8"
ROUTE_W   = 3
CITY_R    = 7
LABEL_FG  = "#f0e6c8"

class MapUI(tk.Frame, UserInterface):
    """
    Draws the board map on a Tkinter canvas.
    Cities are dots, routes are coloured lines.
    """

    def __init__(self, parent: tk.Widget, board: Board, width: int, height: int) -> None:
        super().__init__(parent, bg=BG_MAP)
        self.__board = board
        self.__width = width
        self.__height = height
        self.__canvas: tk.Canvas | None = None
        self.__on_route_click = None
        self.build_ui()

    def set_on_route_click(self, callback) -> None:
        """Register a callback for when a route is clicked."""
        self.__on_route_click = callback

    def build_ui(self) -> None:
        self.__canvas = tk.Canvas(
            self,
            bg=BG_MAP,
            width=self.__width,
            height=self.__height,
            highlightthickness=0,
        )
        self.__canvas.pack(fill="both", expand=True)

    def draw_map(self) -> None:
        """
        Draw all routes and cities from the board onto the canvas.
        Called after game.setup() completes the board build.
        """
        self.__canvas.delete("all")
        self._draw_routes()
        self._draw_cities()

    def _draw_routes(self) -> None:
        for route in self.__board.get_routes():
            start = route.get_start_city().get_name()
            dest  = route.get_destination_city().get_name()
            if start not in CITY_POSITIONS or dest not in CITY_POSITIONS:
                continue
            x1, y1 = self._to_px(*CITY_POSITIONS[start])
            x2, y2 = self._to_px(*CITY_POSITIONS[dest])
            color = route.get_color().value
            line = self.__canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=ROUTE_W + 2,
                capstyle="round",
            )
            self.__canvas.tag_bind(line, "<Button-1>", lambda e, r=route: self._on_route_clicked(r))

            # Draw route length label at midpoint
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            oval = self.__canvas.create_oval(
                mx - 7, my - 7, mx + 7, my + 7,
                fill=BG_MAP, outline=color, width=1,
            )
            txt = self.__canvas.create_text(
                mx, my,
                text=str(route.get_length()),
                fill=LABEL_FG,
                font=("Georgia", 7, "bold"),
            )
            
            # Bind the length label and background to the click event too!
            self.__canvas.tag_bind(oval, "<Button-1>", lambda e, r=route: self._on_route_clicked(r))
            self.__canvas.tag_bind(txt, "<Button-1>", lambda e, r=route: self._on_route_clicked(r))

    def draw_train_pieces(self, route: Route, player: Player) -> None:
        """
        Delegate train piece rendering to TrainPieceUI.
        :param route: The claimed route.
        :param player: The player who claimed it.
        """
        piece_ui = TrainPieceUI(
            self.__canvas, player, route,
            self.__width, self.__height
        )
        piece_ui.build_ui(CITY_POSITIONS)

    def _on_route_clicked(self, route) -> None:
        """Notify the click callback if set."""
        if self.__on_route_click:
            self.__on_route_click(route)

    def _draw_cities(self) -> None:
        for city in self.__board.get_cities():
            name = city.get_name()
            if name not in CITY_POSITIONS:
                continue
            x, y = self._to_px(*CITY_POSITIONS[name])
            self.__canvas.create_oval(
                x - CITY_R, y - CITY_R,
                x + CITY_R, y + CITY_R,
                fill=CITY_FILL,
                outline=CITY_OUT,
                width=2,
            )
            self.__canvas.create_text(
                x, y + CITY_R + 8,
                text=name,
                fill=LABEL_FG,
                font=("Georgia", 7),
                anchor="n",
            )

    def _to_px(self, rx: float, ry: float) -> tuple[int, int]:
        return int(rx * self.__width), int(ry * self.__height)