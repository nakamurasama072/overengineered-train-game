import tkinter as tk
from ui.card_ui import TrainCardUI
from engine.comps.card import TrainCard
from typing import Callable

class MarketUI(tk.Frame):
    """
    Passive view for the 5 face-up cards.
    Does not perform logic; only displays cards and forwards clicks.
    """
    def __init__(self, parent: tk.Widget, on_card_click: Callable[[int], None]):
        super().__init__(parent, bg="#1a1a2e")
        self.__on_card_click = on_card_click

    def update_market(self, cards: list[TrainCard]) -> None:
        """
        Clears and re-renders the cards provided by the GameUI.
        """
        for child in self.winfo_children():
            child.destroy()
        
        for i, card in enumerate(cards):
            if card:
                ui_card = TrainCardUI(
                    self, 
                    card, 
                    callback=lambda idx=i: self.__on_card_click(idx)
                )
                ui_card.pack(side="top", pady=5)