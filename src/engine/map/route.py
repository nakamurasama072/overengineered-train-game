from __future__ import annotations

from typing import TYPE_CHECKING

from engine.comps.color_enums import TrainColor

if TYPE_CHECKING:
    from engine.comps.player import Player
    from engine.map.city import City


class Route:
    """
    Represents a route between two cities on the board.
    Owned by Board as part of the map composition.
    """

    def __init__(
        self,
        start_city: City,
        destination_city: City,
        length: int,
        color: TrainColor,
    ) -> None:
        """
        Constructor.
        :param start_city: The starting city.
        :param destination_city: The destination city.
        :param length: The length of the route.
        :param color: The color of the route.
        """
        if length <= 0:
            raise ValueError("Route length must be positive.")
        self.__start_city = start_city
        self.__destination_city = destination_city
        self.__length = length
        self.__color = color
        self.__claimable: bool = True
        self.__claimed_by: Player | None = None
        self.__start_city.add_route(self)
        self.__destination_city.add_route(self)

    def is_claimed(self) -> bool:
        """
        Determine if the route has been claimed by a player.
        :return: True if claimed, False otherwise.
        """
        return self.__claimed_by is not None

    def claim(self, player: Player) -> None:
        """
        Claim this route on behalf of a player.
        :param player: The player claiming the route.
        """
        if not self.__claimable:
            raise ValueError("This route is not claimable.")
        if self.is_claimed():
            raise ValueError("This route has already been claimed.")
        self.__claimed_by = player
        self.__claimable = False

    def get_start_city(self) -> City:
        return self.__start_city

    def get_destination_city(self) -> City:
        return self.__destination_city

    def get_length(self) -> int:
        return self.__length

    def get_color(self) -> TrainColor:
        return self.__color

    def get_claimed_by(self) -> Player | None:
        return self.__claimed_by

    def is_claimable(self) -> bool:
        return self.__claimable

    def __repr__(self) -> str:
        start = self.__start_city.get_name()
        destination = self.__destination_city.get_name()
        return (
            f"Route({start} -> {destination}, "
            f"length={self.__length}, "
            f"color={self.__color.name.lower()})"
        )