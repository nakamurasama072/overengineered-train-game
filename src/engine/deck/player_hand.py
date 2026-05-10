from __future__ import annotations

from typing import TYPE_CHECKING, List

from engine.deck.card_collection import CardCollection

if TYPE_CHECKING:
    from engine.comps.card import Card, TrainCard, DestinationTicketCard


class PlayerHand(CardCollection):
    """
    Represents the player's hand of cards.
    Holds both train cards and destination tickets.
    """

    def __init__(self) -> None:
        super().__init__()

    def get_train_cards(self) -> List[TrainCard]:
        """
        Get all train cards in hand.
        :return: List of train cards.
        """
        from engine.comps.card import TrainCard
        return [c for c in self._cards if isinstance(c, TrainCard)]

    def get_destination_tickets(self) -> List[DestinationTicketCard]:
        """
        Get all destination tickets in hand.
        :return: List of destination ticket cards.
        """
        from engine.comps.card import DestinationTicketCard
        return [c for c in self._cards if isinstance(c, DestinationTicketCard)]