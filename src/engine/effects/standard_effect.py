from engine.effects.effect import Effect

class StandardEffect(Effect):
    """
    Represents the drawing rules for a standard colored Train Card 
    (or a blind draw from the face-down deck).
    """

    def can_be_drawn(self, turn_manager) -> bool:
        """
        Checks if a standard card can be drawn. 
        Returns True if the player has drawn less than 2 cards this turn.
        """
        return turn_manager.get_cards_drawn_this_turn() < 2

    def process_draw(self, turn_manager) -> None:
        """
        Processes the cost of a standard card draw. 
        Increments the TurnManager's drawn card counter by 1.
        """
        turn_manager.increment_cards_drawn()