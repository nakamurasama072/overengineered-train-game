from abc import ABC, abstractmethod

class Effect(ABC):
    """
    Abstract base class representing the specific rules and turn costs 
    associated with drawing a particular type of Train Card.
    """
    
    @abstractmethod
    def can_be_drawn(self, turn_manager) -> bool:
        """
        Evaluates the current turn budget to determine if the player 
        is legally allowed to draw this specific type of card.
        """
        pass

    @abstractmethod
    def process_draw(self, turn_manager) -> None:
        """
        Updates the player's turn budget within the TurnManager 
        after this specific type of card has been successfully drawn.
        """
        pass