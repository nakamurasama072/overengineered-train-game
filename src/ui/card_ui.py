from __future__ import annotations

import tkinter as tk

from engine.comps.card import DestinationTicketCard, TrainCard

TICKET_BG   = "#fdf6e3"
TICKET_FG   = "#2c2c2c"
CARD_RADIUS = 6


class CardUI(tk.Frame):
    """
    Abstract-like base widget for a single card.
    Subclassed by TrainCardUI and DestinationTicketCardUI.
    """

    CARD_W = 80
    CARD_H = 54

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(
            parent,
            width=self.CARD_W,
            height=self.CARD_H,
            relief="ridge",
            bd=2,
            **kwargs,
        )
        self.grid_propagate(False)
        self.pack_propagate(False)

    def build_ui(self) -> None:
        raise NotImplementedError


class TrainCardUI(CardUI):
    """
    Visual widget for a single TrainCard.
    """
    def __init__(self, parent: tk.Widget, card: TrainCard, callback=None) -> None:
        bg = card.get_color().value
        super().__init__(parent, bg=bg)
        self.__card = card
        self.__bg = bg
        self.__callback = callback  # Store the callback
        self.build_ui()
        
        # Bind the click event to the frame
        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event) -> None:
        """Trigger the callback if it exists."""
        if self.__callback:
            self.__callback()

    def build_ui(self) -> None:
        from engine.comps.color_enums import TrainColor
        fg = "#ffffff" if self.__card.get_color() is TrainColor.BLACK else "#1a1a2e"
        lbl = tk.Label(
            self,
            text=self.__card.get_color().name.title(),
            bg=self.__bg,
            fg=fg,
            font=("Georgia", 8, "bold"),
        )
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        # Ensure clicking the label also triggers the frame's callback
        lbl.bind("<Button-1>", lambda e: self._on_click(e))

class DestinationTicketCardUI(CardUI):
    """
    Visual widget for a single DestinationTicketCard.
    """

    CARD_W = 210
    CARD_H = 65

    def __init__(self, parent: tk.Widget, card: DestinationTicketCard) -> None:
        super().__init__(parent, bg=TICKET_BG)
        self.__card = card
        self.build_ui()

    def build_ui(self) -> None:
        text = (
            f"{self.__card.get_source().get_name()}"
            f"  →  "
            f"{self.__card.get_destination().get_name()}"
            f"\n{self.__card.get_points()} pts"
        )
        tk.Label(
            self,
            text=text,
            bg=TICKET_BG,
            fg=TICKET_FG,
            font=("Georgia", 8, "bold"),
            justify="center",
            wraplength=self.CARD_W - 10,
        ).place(relx=0.5, rely=0.5, anchor="center")

class FaceDownDeckUI(CardUI):
    """
    Visual widget for a face-down draw deck.
    """
    def __init__(self, parent: tk.Widget, label_text: str, bg_color: str, callback=None) -> None:
        super().__init__(parent, bg=bg_color)
        self.__text = label_text
        self.__bg = bg_color
        self.__callback = callback
        self.build_ui()
        
        # Bind the click event to the frame
        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event) -> None:
        """Trigger the callback if it exists."""
        if self.__callback:
            self.__callback()

    def build_ui(self) -> None:
        lbl = tk.Label(
            self,
            text=self.__text,
            bg=self.__bg,
            fg="#ffffff",
            font=("Georgia", 8, "bold"),
            wraplength=70,
            justify="center"
        )
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        # Ensure clicking the label also triggers the frame's callback
        lbl.bind("<Button-1>", lambda e: self._on_click(e))