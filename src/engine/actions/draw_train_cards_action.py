from engine.actions.game_action import GameAction
from engine.effects.standard_effect import StandardEffect

class DrawTrainCardsAction(GameAction):
    """
    Encapsulates the entire transaction of a player drawing a Train Card, 
    either blindly from the deck or face-up from the market.
    """

    def __init__(self, player, turn_manager, draw_deck, face_up_deck, card_index=None):
        """
        Initializes the action with all required dependencies.
        If card_index is None, the action defaults to a face-down blind draw.
        """
        self.__player = player
        self.__turn_manager = turn_manager
        self.__draw_deck = draw_deck
        self.__face_up_deck = face_up_deck
        self.__card_index = card_index 

    def validate(self) -> bool:
        """
        Validates the draw request against the player's current turn budget.
        Returns True if the draw is legal, False otherwise.
        """
        if self.__card_index is None:
            # Blind draw rule: Always follows standard card budget rules
            dummy_effect = StandardEffect()
            return dummy_effect.can_be_drawn(self.__turn_manager)
        else:
            # Face-up rule: Peek at the specific card to get its unique effect
            target_card = self.__face_up_deck.peek(self.__card_index)
            if target_card is None:
                return False 
            
            card_effect = target_card.get_effect()
            return card_effect.can_be_drawn(self.__turn_manager)

    def execute(self) -> None:
        """
        Executes the draw. Moves the card to the player's hand, updates 
        the TurnManager's budget, and refills the face-up market if necessary.
        """
        if self.__card_index is None:
            # Execute face-down blind draw
            card = self.__draw_deck.draw() # Fixed method name
            if card is not None:           # Added safety check
                self.__player.draw_train_card_from_train_deck(card)
                dummy_effect = StandardEffect()
                dummy_effect.process_draw(self.__turn_manager)
                    
        else:
            # Execute face-up market draw
            target_card = self.__face_up_deck.peek(self.__card_index)
            card_effect = target_card.get_effect()
            
            card = self.__face_up_deck.remove_card_at(self.__card_index) 
            self.__player.draw_train_card_from_train_deck(card)
            
            card_effect.process_draw(self.__turn_manager)
            
            # Refill the empty market slot
            if not self.__draw_deck.is_empty():
                new_card = self.__draw_deck.draw()
                self.__face_up_deck.add_card_at(self.__card_index, new_card)