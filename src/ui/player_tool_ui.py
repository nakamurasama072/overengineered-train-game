from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ui.card_ui import TrainCardUI, DestinationTicketCardUI

if TYPE_CHECKING:
    from engine.comps.card import DestinationTicketCard, TrainCard

BG       = "#16213e"
FG       = "#e0e0e0"
ACCENT   = "#c9a227"
MUTED    = "#7a7a9a"
DIVIDER  = "#2a2a4a"


class UserInterface(ABC):
    @abstractmethod
    def build_ui(self) -> None:
        pass


class PlayerToolUI(tk.Frame, UserInterface):
    """
    Bottom panel showing the player's hand.
    Left side: train cards in a wrapping row x column grid.
    Right side: destination tickets stacked vertically.
    """

    def __init__(self, parent: tk.Widget, height: int) -> None:
        super().__init__(parent, bg=BG, height=height)
        self.pack_propagate(False)
        self.__train_container: tk.Frame | None = None
        self.__ticket_container: tk.Frame | None = None
        self.__card_frames: list[tk.Frame] = []
        self.__on_skip_callback = None
        self.build_ui()

    def set_on_end_turn_callback(self, callback) -> None:
        """Register a callback for when the skip button is clicked."""
        self.__on_skip_callback = callback

    def build_ui(self) -> None:
        # Header bar
        header = tk.Frame(self, bg=ACCENT, height=3)
        header.pack(fill="x")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=10)

        # Left — train cards
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(
            left,
            text="TRAIN CARDS",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 6))

        self.__train_container = tk.Frame(left, bg=BG)
        self.__train_container.pack(fill="both", expand=True)
        self.__train_container.bind("<Configure>", self._reflow_train_cards)

        # Skip button
        tk.Button(
            body,
            text="SKIP TURN",
            bg=ACCENT,
            fg="#1a1a2e",
            font=("Georgia", 10, "bold"),
            padx=16,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self._on_skip_clicked,
        ).pack(side="right", anchor="se", padx=(0, 8))

        # Divider
        tk.Frame(body, bg=DIVIDER, width=2).pack(side="left", fill="y", padx=16)

        # Right — destination tickets
        right = tk.Frame(body, bg=BG, width=220)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)

        tk.Label(
            right,
            text="DESTINATION TICKETS",
            bg=BG,
            fg=MUTED,
            font=("Georgia", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 6))

        self.__ticket_container = tk.Frame(right, bg=BG)
        self.__ticket_container.pack(fill="both", expand=True)

    def _on_skip_clicked(self) -> None:
        """Called when the skip button is clicked."""
        if self.__on_skip_callback:
            self.__on_skip_callback()

    def show_train_cards(self, cards: list[TrainCard]) -> None:
        """
        Render train cards into the left container.
        """
        for child in self.__train_container.winfo_children():
            child.destroy()
        self.__card_frames = []
        for card in cards:
            frame = TrainCardUI(self.__train_container, card)
            self.__card_frames.append(frame)
        self.__train_container.after(50, self._reflow_train_cards)

    def show_destination_tickets(self, tickets: list[DestinationTicketCard]) -> None:
        """
        Render destination tickets into the right container, stacked vertically.
        """
        for child in self.__ticket_container.winfo_children():
            child.destroy()
        for ticket in tickets:
            card = DestinationTicketCardUI(self.__ticket_container, ticket)
            card.pack(pady=(0, 6), anchor="w")

    def _reflow_train_cards(self, event=None) -> None:
        """
        Reflow train cards into rows based on available container width.
        """
        if not self.__card_frames:
            return
        container_width = self.__train_container.winfo_width()
        if container_width <= 1:
            return
        card_w = TrainCardUI.CARD_W + 6
        cards_per_row = max(1, container_width // card_w)
        for i, frame in enumerate(self.__card_frames):
            frame.grid(
                row=i // cards_per_row,
                column=i % cards_per_row,
                padx=(0, 6),
                pady=(0, 6),
            )