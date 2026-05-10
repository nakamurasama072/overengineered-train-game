from __future__ import annotations

from engine.comps.color_enums import PlayerColor


class ScoringMarker:
    """
    The scoring marker class.
    """
    def __init__(self, player_color: PlayerColor) -> None:
        self.__color: PlayerColor = player_color
        self.__position: int = 0

    def get_color(self) -> PlayerColor:
        """
        Get the color of the scoring marker.
        :return: Player color.
        """
        return self.__color

    def move(self, points: int) -> None:
        """
        Move the scoring marker by a number of points.
        :param points: Score delta.
        """
        self.__position += points

    def get_position(self) -> int:
        """
        Get the current score track position.
        :return: Current score.
        """
        return self.__position