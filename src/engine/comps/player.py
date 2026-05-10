from __future__ import annotations

from typing import TYPE_CHECKING

from engine.comps.color_enums import PlayerColor, TrainColor
from engine.deck.player_hand import PlayerHand

if TYPE_CHECKING:
    from engine.comps.card import DestinationTicketCard, TrainCard
    from engine.map.route import Route


class Player:
    """
    The player class.
    """

    DEFAULT_TRAIN_PIECES = 7

    def __init__(self, name: str, color: PlayerColor) -> None:
        """
        Constructor.
        :param name: The player's name.
        :param color: The player's color.
        """
        self.__name: str = name
        self.__color: PlayerColor = color
        self.__train_pieces: int = self.DEFAULT_TRAIN_PIECES
        self.__hand: PlayerHand = PlayerHand()

    def get_name(self) -> str:
        """
        Get the player name.
        :return: Player name.
        """
        return self.__name

    def get_color(self) -> PlayerColor:
        """
        Get the player color.
        :return: Player color.
        """
        return self.__color

    def get_train_pieces(self) -> int:
        """
        Get the number of train pieces remaining.
        :return: Train pieces remaining.
        """
        return self.__train_pieces

    def get_hand(self) -> PlayerHand:
        """
        Get the player's hand.
        :return: The player's hand.
        """
        return self.__hand

    def get_train_cards(self) -> list[TrainCard]:
        """
        Get a snapshot of the player's train cards.
        :return: The player's train cards.
        """
        return self.__hand.get_train_cards()

    def get_destination_tickets(self) -> list[DestinationTicketCard]:
        """
        Get a snapshot of the player's destination tickets.
        :return: The player's destination tickets.
        """
        return self.__hand.get_destination_tickets()

    def draw_train_card_from_train_deck(self, card: TrainCard) -> None:
        """
        Draw a train card from the face-down draw deck into hand.
        :param card: A train card.
        """
        self.__hand.add(card)

    def play_train_card(self, card: TrainCard) -> None:
        """
        Remove a train card from hand when played.
        :param card: A train card.
        """
        self.__hand.remove(card)

    def draw_destination_ticket(self, card: DestinationTicketCard) -> None:
        """
        Draw a destination ticket into hand.
        :param card: A destination ticket card.
        """
        self.__hand.add(card)

    def use_train_pieces(self, amount: int) -> None:
        """
        Use a number of train pieces when claiming a route.
        :param amount: Number of pieces to use.
        """
        if amount < 0:
            raise ValueError("Cannot use a negative number of train pieces.")
        if amount > self.__train_pieces:
            raise ValueError("Not enough train pieces remaining.")
        self.__train_pieces -= amount

    def is_last_round_trigger(self) -> bool:
        """
        Returns True if this player has 0-2 train pieces left,
        triggering the last round.
        :return: True if last round should be triggered.
        """
        return self.__train_pieces <= 2

    def claim_route(self, route: Route) -> list[TrainCard]:
        """
        Claim a route for this player.
        Validates availability, card sufficiency, and train piece sufficiency.
        Removes matching cards from hand and places train pieces on route.
        Scoring is handled externally by ScoreManager via Game.
        :param route: The route to claim.
        :return: A list of the train cards spent to claim the route.
        """
        if route.is_claimed():
            raise ValueError("Route is already claimed.")
        if self.__train_pieces < route.get_length():
            raise ValueError("Not enough train pieces to claim this route.")

        cards_to_use = self._resolve_cards(route)
        if len(cards_to_use) < route.get_length():
            raise ValueError("Not enough matching cards to claim this route.")

        for card in cards_to_use:
            self.__hand.remove(card)

        route.claim(self)
        self.use_train_pieces(route.get_length())
        return cards_to_use

    def _resolve_cards(self, route: Route) -> list[TrainCard]:
        """
        Find matching cards in hand for the given route.
        Prefers exact color matches, fills remainder with WILD locomotives.
        :param route: The route to resolve cards for.
        :return: List of cards to use.
        """
        route_color = route.get_color()
        hand = self.__hand.get_train_cards()
        needed = route.get_length()
        wilds = [c for c in hand if c.get_color() == TrainColor.WILD]

        if route_color == TrainColor.GRAY:
            color_groups: dict = {}
            for card in hand:
                if card.get_color() == TrainColor.WILD:
                    continue
                color_groups.setdefault(card.get_color(), []).append(card)
            best: list = []
            for cards in color_groups.values():
                if len(cards) > len(best):
                    best = cards
            selected = best[:needed]
            selected += wilds[:needed - len(selected)]
            return selected

        exact = [c for c in hand if c.get_color() == route_color]
        selected = exact[:needed]
        selected += wilds[:needed - len(selected)]
        return selected

    def __repr__(self) -> str:
        return f"Player({self.__name})"