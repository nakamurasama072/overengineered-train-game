from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from engine.effects.effect import Effect
from engine.comps.color_enums import TrainColor

if TYPE_CHECKING:
    from engine.map.city import City

class Card(ABC):
    """
    Abstract class for cards.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Return the type of this card.
        :return: The type of this card.
        """
        pass


class TrainCard(Card):
    """
    The train card class.
    """
    def __init__(self, color: TrainColor, effect: Effect) -> None:
        """
        Constructor.
        """
        super().__init__()
        if color is TrainColor.GRAY:
            raise ValueError("Train cards cannot use the gray route color.")
        self.__color = color
        self.__effect = effect


    def get_type(self) -> str:
        """
        Get the type of this card.
        :return: TrainCard
        """
        return "TrainCard"

    def get_color(self) -> TrainColor:
        """
        Get the train card color.
        :return: The train card color.
        """
        return self.__color
    
    def get_effect(self):
        """
        Retrieves the injected Effect object associated with this card.
        Used by Actions to determine the draw rules dynamically.
        """
        return self.__effect

    def __repr__(self) -> str:
        return f"TrainCard({self.__color.name.lower()})"


class DestinationTicketCard(Card):
    """
    Represents a Destination Ticket card in the game.
    """
    def __init__(self, source: City, destination: City, points: int):
        """
        Constructor.
        :param source: City
        :param destination: City
        :param points: int
        """
        super().__init__()
        if points <= 0:
            raise ValueError("Destination ticket points must be positive.")
        self.__source = source
        self.__destination = destination
        self.__points = points
        self.__completed = False

    def get_source(self) -> City:
        """
        Get the source city.
        :return: The source city.
        """
        return self.__source

    def get_destination(self) -> City:
        """
        Get the destination city.
        :return: The destination city.
        """
        return self.__destination

    def get_points(self) -> int:
        """
        Get the ticket value.
        :return: The point value of this ticket.
        """
        return self.__points

    def complete_route(self) -> None:
        """
        Marks the destination ticket as successfully completed.
        """
        self.__completed = True

    def get_type(self) -> str:
        """
        Get the type of this card.
        :return: DestinationTicketCard
        """
        return "DestinationTicketCard"

    def is_complete(self) -> bool:
        """
        Retrieves the completion status of the destination ticket.
        :return: True if completed, False otherwise
        """
        return self.__completed

    def __repr__(self) -> str:
        source = self.__source.get_name()
        destination = self.__destination.get_name()
        return f"DestinationTicketCard({source} -> {destination}, {self.__points})"