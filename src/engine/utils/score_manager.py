from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.comps.player import Player

ROUTE_SCORE_TABLE: dict[int, int] = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15,
}

LONGEST_PATH_BONUS: int = 10


class ScoreManager:
    """
    Manages all player scores for the game.
    Owns a dictionary of players to their scores.
    All score mutations go through ScoreManager.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.__players: dict[Player, int] = {}

    def add_player_to_dict(self, player: Player) -> None:
        """
        Register a player with an initial score of 0.
        :param player: The player to register.
        """
        self.__players[player] = 0

    def add_score(self, player: Player, points: int) -> None:
        """
        Add points to a player's score.
        :param player: The player to award points to.
        :param points: The number of points to add.
        """
        if player not in self.__players:
            raise ValueError("Player not registered with ScoreManager.")
        self.__players[player] += points

    def get_score(self, player: Player) -> int:
        """
        Get a player's current score.
        :param player: The player.
        :return: The player's current score.
        """
        if player not in self.__players:
            raise ValueError("Player not registered with ScoreManager.")
        return self.__players[player]

    def get_route_score(self, route_length: int) -> int:
        """
        Get the points awarded for claiming a route of a given length.
        :param route_length: The length of the route.
        :return: Points to award.
        """
        return ROUTE_SCORE_TABLE.get(route_length, 0)

    def get_ticket_bonus(self, ticket_points: int) -> int:
        """
        Get the bonus for completing a destination ticket.
        :param ticket_points: The point value of the ticket.
        :return: Points to award.
        """
        return ticket_points

    def get_ticket_penalty(self, ticket_points: int) -> int:
        """
        Get the penalty for an incomplete destination ticket.
        :param ticket_points: The point value of the ticket.
        :return: Points to deduct as a negative value.
        """
        return -ticket_points

    def get_longest_path_bonus(self) -> int:
        """
        Get the longest continuous path bonus.
        :return: Points awarded for the longest path.
        """
        return LONGEST_PATH_BONUS

    def get_all_scores(self) -> dict[Player, int]:
        """
        Get a snapshot of all player scores.
        :return: A copy of the players score dictionary.
        """
        return dict(self.__players)