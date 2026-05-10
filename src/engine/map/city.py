from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.map.route import Route


class City:
    """
    Represents a city node on the board map.
    """

    def __init__(self, name: str) -> None:
        """
        Constructor.
        :param name: The name of the city.
        """
        self.__name: str = name
        self.__routes: list[Route] = []

    def add_route(self, route: Route) -> None:
        """
        Register a route connected to this city.
        Called automatically by Route on construction.
        :param route: Route connected to this city.
        """
        self.__routes.append(route)

    def get_name(self) -> str:
        """
        Get the city name.
        :return: The city name.
        """
        return self.__name

    def get_routes(self) -> list[Route]:
        """
        Get all routes connected to this city.
        :return: A copy of the connected routes.
        """
        return list(self.__routes)

    def __repr__(self) -> str:
        return f"City({self.__name})"