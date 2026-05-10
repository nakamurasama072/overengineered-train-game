from __future__ import annotations

from engine.deck.card_collection import CardCollection
from engine.comps.card import Card


class DiscardPile(CardCollection):
    """
    The discard pile for played or discarded cards.
    """

    def __init__(self) -> None:
        super().__init__()

    def add_to_bottom(self, card: Card) -> None:
        """
        Add a card to the bottom of the discard pile.
        Used when returning unwanted destination tickets.
        :param card: The card to add.
        """
        self._cards.insert(0, card)