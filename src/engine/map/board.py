from __future__ import annotations

from engine.map.city import City
from engine.map.route import Route
from engine.utils.game_constants import CITY_NAMES, ROUTE_DATA


class Board:
    """
    The board class, representing the game board.
    Owns City and Route as compositions.
    Board starts empty and is built via build_map().
    """

    def __init__(self) -> None:
        """
        Constructor. Board starts empty until build_map() is called.
        """
        self.__cities: dict[str, City] = {}
        self.__routes: list[Route] = []

    def build_map(self) -> None:
        """
        Build the map by creating all cities and routes from game constants.
        Cities register routes automatically on Route construction.
        """
        self.__cities = {name: City(name) for name in CITY_NAMES}
        self.__routes = [
            Route(
                self.__cities[start],
                self.__cities[destination],
                length,
                color,
            )
            for start, destination, color, length in ROUTE_DATA
        ]

    def get_cities(self) -> list[City]:
        """
        Get all cities on the board.
        :return: A list of all cities.
        """
        return list(self.__cities.values())

    def get_routes(self) -> list[Route]:
        """
        Get all routes on the board.
        :return: A list of all routes.
        """
        return list(self.__routes)

    def get_city(self, name: str) -> City | None:
        """
        Find a city by name.
        :param name: City name.
        :return: The city if found, None otherwise.
        """
        return self.__cities.get(name)