from __future__ import annotations

from typing import List
from engine.comps.card import TrainCard

class TrainDiscardDeck:
    """
    Holds flushed or spent TrainCards.
    """
    
    def __init__(self) -> None:
        self.__cards: List[TrainCard] = []

    def add(self, card: TrainCard) -> None:
        """Adds a single card to the discard pile."""
        self.__cards.append(card)

    def extend(self, cards: List[TrainCard]) -> None:
        """Adds multiple cards to the discard pile."""
        self.__cards.extend(cards)

    def take_all(self) -> List[TrainCard]:
        """Returns all cards and empties the discard pile."""
        cards = self.__cards[:]
        self.__cards.clear()
        return cards

    def get_count(self) -> int:
        """Returns the number of discarded cards."""
        return len(self.__cards)

    def is_empty(self) -> bool:
        """Returns whether the discard pile is empty."""
        return len(self.__cards) == 0
