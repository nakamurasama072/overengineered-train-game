from __future__ import annotations

from typing import Optional

from engine.deck.card_collection import CardCollection
from engine.comps.card import Card


class DrawDeck(CardCollection):
    """
    Base class for drawable decks.
    Supports drawing from the top and shuffling.
    """

    def __init__(self) -> None:
        super().__init__()

    def draw(self) -> Optional[Card]:
        """
        Draw a card from the top of the deck.
        :return: The top card, or None if empty.
        """
        if self.is_empty():
            return None
        return self._cards.pop()

    def extend(self, cards: list[Card]) -> None:
        """
        Add multiple cards to the deck.
        :param cards: Cards to add.
        """
        self._cards.extend(cards)

    def shuffle(self, randomizer=None) -> None:
        """
        Shuffle the deck.
        :param randomizer: Optional random.Random instance for reproducibility.
        """
        import random
        if randomizer is None:
            random.shuffle(self._cards)
        else:
            randomizer.shuffle(self._cards)

    def add_to_bottom(self, card: Card) -> None:
        """
        Adds a card to the bottom of the deck.
        Used for returning rejected Destination Tickets.
        """
        # index 0 is the bottom of the deck, since pop() takes from the end
        self._cards.insert(0, card)


class TrainDrawDeck(DrawDeck):
    """
    The deck of Train Car cards to draw from.
    """

    def __init__(self) -> None:
        super().__init__()


class DestinationTicketDrawDeck(DrawDeck):
    """
    The deck of Destination Ticket cards to draw from.
    """

    def __init__(self) -> None:
        super().__init__()


