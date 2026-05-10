from engine.actions.game_action import GameAction

class DrawDestinationTicketsAction(GameAction):
    """
    Handles the final execution of drawing destination tickets after 
    the player has made their selection.
    """
    def __init__(self, player, turn_manager, ticket_deck, kept_tickets, returned_tickets):
        self.__player = player
        self.__turn_manager = turn_manager
        self.__ticket_deck = ticket_deck
        self.__kept_tickets = kept_tickets
        self.__returned_tickets = returned_tickets

    def validate(self) -> bool:
        """
        Validates that the player hasn't already started drawing train cards.
        Drawing tickets requires a completely fresh turn.
        """
        if self.__turn_manager.get_cards_drawn_this_turn() > 0:
            return False
        if len(self.__kept_tickets) < 1:
            return False # Must keep at least one
        return True

    def execute(self) -> None:
        """
        Gives the kept tickets to the player and returns the rest to the bottom of the deck.
        """
        # 1. Give kept cards to the player
        for ticket in self.__kept_tickets:
            self.__player.draw_destination_ticket(ticket)
            
        # 2. Put returned cards at the bottom of the deck
        for ticket in self.__returned_tickets:
            self.__ticket_deck.add_to_bottom(ticket)
            
        # 3. Consume the entire turn budget
        self.__turn_manager.increment_cards_drawn(2)