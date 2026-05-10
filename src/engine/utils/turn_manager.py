from __future__ import annotations


class TurnManager:
    """
    Manages turn state for the active player.
    Tracks how many cards have been drawn this turn
    and enforces the 2-card draw budget.
    """

    MAX_CARDS_PER_TURN = 2

    def __init__(self, num_players: int) -> None:
        """
        Constructor.
        :param num_players: The total number of players in the game.
        """
        self._current_player_index: int = 0
        self._cards_drawn_this_turn: int = 0
        self._num_players: int = num_players

    def start_turn(self) -> None:
        """
        Resets turn-specific counters for the new active player.
        """
        self._cards_drawn_this_turn = 0

    def end_turn(self) -> None:
        """
        Advances to the next player and resets the draw counter.
        """
        self._current_player_index = (
            self._current_player_index + 1
        ) % self._num_players
        self.start_turn()

    def increment_cards_drawn(self, count: int = 1) -> None:
        """
        Increment the draw counter after a card is drawn.
        :param count: 1 for a standard card, 2 for a face-up locomotive.
        """
        self._cards_drawn_this_turn += count

    def get_cards_drawn_this_turn(self) -> int:
        """
        Returns how many cards have been drawn this turn.
        :return: Integer count (0, 1, or 2).
        """
        return self._cards_drawn_this_turn

    def has_finished_drawing(self) -> bool:
        """
        Returns True if the player has used their full draw budget.
        :return: True if cards drawn >= MAX_CARDS_PER_TURN.
        """
        return self._cards_drawn_this_turn >= self.MAX_CARDS_PER_TURN

    def get_current_player_index(self) -> int:
        """
        Returns the index of the currently active player.
        :return: Current player index.
        """
        return self._current_player_index