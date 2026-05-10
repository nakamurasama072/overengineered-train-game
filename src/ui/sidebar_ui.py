from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Callable, Optional
from ui.market_ui import MarketUI
from engine.comps.card import TrainCard

BG        = "#1a1a2e"
FG        = "#e0e0e0"
ACCENT    = "#c9a227"
MUTED     = "#7a7a9a"
FONT_HEAD = ("Georgia", 13, "bold")
FONT_BODY = ("Georgia", 10)


class UserInterface(ABC):
    """Abstract base for all UI panels."""

    @abstractmethod
    def build_ui(self) -> None:
        pass


class SidebarUI(tk.Frame, UserInterface):
    """
    Left sidebar panel.
    Shows the current setup phase status and game log.
    """

    def __init__(
        self, 
        parent: tk.Widget, 
        width: int,
        on_market_click: Optional[Callable[[int], None]] = None,
        on_train_deck_click: Optional[Callable[[], None]] = None,
        on_ticket_deck_click: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent, bg=BG, width=width)
        self.pack_propagate(False)
        self.__on_market_click = on_market_click
        self.__on_train_deck_click = on_train_deck_click
        self.__on_ticket_deck_click = on_ticket_deck_click
        self.__status_var = tk.StringVar(value="Press START to begin.")
        self.__train_pieces_var = tk.StringVar(value="Train pieces: --")
        self.__log_lines: list[str] = []
        self.__market_ui: MarketUI | None = None
        self.build_ui()

    def build_ui(self) -> None:
        # Title
        tk.Label(
            self,
            text="TICKET TO RIDE",
            bg=BG,
            fg=ACCENT,
            font=("Georgia", 15, "bold"),
            pady=18,
        ).pack(fill="x")

        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=16)

        # Status
        tk.Label(
            self,
            text="STATUS",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
            padx=16,
        ).pack(fill="x", pady=(14, 2))

        tk.Label(
            self,
            textvariable=self.__status_var,
            bg=BG,
            fg=FG,
            font=FONT_BODY,
            anchor="w",
            padx=16,
            wraplength=200,
            justify="left",
        ).pack(fill="x")

        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=16, pady=14)

        # Train pieces
        tk.Label(
            self,
            text="PLAYER",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
            padx=16,
        ).pack(fill="x")

        tk.Label(
            self,
            textvariable=self.__train_pieces_var,
            bg=BG,
            fg=FG,
            font=FONT_BODY,
            anchor="w",
            padx=16,
        ).pack(fill="x")

        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=16, pady=14)

        # Market & Decks
        tk.Label(
            self,
            text="MARKET & DECKS",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
            padx=16,
        ).pack(fill="x")

        decks_frame = tk.Frame(self, bg=BG)
        decks_frame.pack(fill="x", padx=16, pady=8)
        
        tk.Button(
            decks_frame,
            text="Train Deck",
            bg=ACCENT,
            fg="#1a1a2e",
            font=("Georgia", 9, "bold"),
            cursor="hand2",
            command=self.__on_train_deck_click
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        
        tk.Button(
            decks_frame,
            text="Ticket Deck",
            bg=ACCENT,
            fg="#1a1a2e",
            font=("Georgia", 9, "bold"),
            cursor="hand2",
            command=self.__on_ticket_deck_click
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        self.__market_ui = MarketUI(self, on_card_click=self.__on_market_click)
        self.__market_ui.pack(fill="x", padx=16, pady=5)

        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=16, pady=14)

        # Log
        tk.Label(
            self,
            text="GAME LOG",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
            padx=16,
        ).pack(fill="x")

        # Create a container for the canvas and scrollbar
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=16, pady=8)

        # Create the canvas and scrollbar
        self.__canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        self.__scrollbar = tk.Scrollbar(container, orient="vertical", command=self.__canvas.yview)
        self.__log_frame = tk.Frame(self.__canvas, bg=BG)

        self.__canvas.configure(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.pack(side="right", fill="y")
        self.__canvas.pack(side="left", fill="both", expand=True)

        self.__canvas_window = self.__canvas.create_window((0, 0), window=self.__log_frame, anchor="nw")

        # Update scrollregion dynamically when the frame changes size
        self.__log_frame.bind(
            "<Configure>",
            lambda e: self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))
        )
        self.__canvas.bind(
            "<Configure>",
            lambda e: self.__canvas.itemconfig(self.__canvas_window, width=e.width)
        )

    def update_train_pieces(self, count: int) -> None:
        """Update the train pieces display."""
        self.__train_pieces_var.set(f"Train pieces: {count}")

    def set_status(self, message: str) -> None:
        """Update the status message."""
        self.__status_var.set(message)

    def add_log(self, message: str) -> None:
        """Append a line to the game log."""
        self.__log_lines.append(message)
        tk.Label(
            self.__log_frame,
            text=f"• {message}",
            bg=BG,
            fg=FG,
            font=("Georgia", 9),
            anchor="w",
            wraplength=200,
            justify="left",
        ).pack(fill="x", pady=2)
        
        # Auto-scroll to the bottom when a new log is added
        self.__log_frame.update_idletasks()
        self.__canvas.yview_moveto(1.0)

    def update_market(self, cards: list[TrainCard]) -> None:
        """Update the market cards display."""
        if self.__market_ui:
            self.__market_ui.update_market(cards)