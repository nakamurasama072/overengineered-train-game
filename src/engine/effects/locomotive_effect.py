from engine.effects.effect import Effect

class LocomotiveEffect(Effect):
    """
    Represents the strict drawing rules for a face-up Locomotive (Wild) Card.
    """

    def can_be_drawn(self, turn_manager) -> bool:
        """
        Checks if a face-up Locomotive can be drawn.
        Returns True ONLY if the player has drawn 0 cards so far this turn.
        """
        return turn_manager.get_cards_drawn_this_turn() == 0

    def process_draw(self, turn_manager) -> None:
        """
        Processes the cost of a face-up Locomotive draw. 
        Increments the TurnManager's counter twice, as it costs 2 actions.
        """
        turn_manager.increment_cards_drawn()
        turn_manager.increment_cards_drawn()