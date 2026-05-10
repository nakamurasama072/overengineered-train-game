from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
import random
from engine.comps.color_enums import TrainColor

from engine.comps.card import Card


class CardCollection(ABC):
    """
    A collection of cards.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        self._cards: List[Card] = []

    def add(self, card: Card) -> None:
        """
        Add a card to the collection.
        :param card: A card to add.
        """
        self._cards.append(card)

    def remove(self, card: Card) -> None:
        """
        Remove a card from the collection.
        :param card: A card to remove.
        """
        self._cards.remove(card)

    def is_empty(self) -> bool:
        """
        Check if the collection is empty.
        :return: a boolean indicating if the collection is empty.
        """
        return len(self._cards) == 0

    def clear(self) -> None:
        """
        Clear the collection.
        """
        self._cards.clear()

    def size(self) -> int:
        """
        Get the number of cards.
        :return: Card count.
        """
        return len(self._cards)
    
    def peek(self, index: int):
        """
        Allows viewing a card at a specific index without removing it from the deck.
        Returns the Card object if it exists, or None if the slot is empty.
        """
        # Ensure the index is valid to prevent list errors
        if 0 <= index < len(self._cards):
            return self._cards[index]
        return None
    
    def add_card_at(self, index: int, card: Card) -> None:
        """
        Inserts a card into the face-up market at the specified index.
        Used to replenish the exact slot a player just drew from.
        """
        self._cards.insert(index, card)
    
class FaceUpDrawDeck(CardCollection):
    """
    Represents the 5 face-up cards available in the market.
    Inherits peek(), add(), and remove() from CardCollection.
    """

    def __init__(self) -> None:
        super().__init__()

    def get_all_cards(self) -> list[Card]:
        """Returns the list of all currently face-up cards."""
        return self._cards

    def remove_card_at(self, index: int) -> Card:
        """
        Removes and returns the card at the given index.
        This is the method the DrawTrainCardsAction is looking for.
        """
        if 0 <= index < len(self._cards):
            return self._cards.pop(index)
        raise IndexError(f"Market index {index} is out of bounds.")