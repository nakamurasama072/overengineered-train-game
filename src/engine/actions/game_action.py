from abc import ABC, abstractmethod

class GameAction(ABC):
    """
    Abstract base class for all player actions (Command Pattern).
    Ensures every action can be validated and executed by the Game controller.
    """
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Checks the current game state to ensure the action is completely legal.
        Returns True if valid, False if the action breaks game rules.
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        Executes the physical game logic, moving pieces and updating game state.
        Must only be called if validate() returns True.
        """
        pass