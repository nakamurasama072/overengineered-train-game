from __future__ import annotations

import random

from engine.comps.card import DestinationTicketCard, TrainCard
from engine.comps.color_enums import PlayerColor, TrainColor
from engine.comps.player import Player
from engine.deck.draw_decks import TrainDrawDeck, DestinationTicketDrawDeck
from engine.deck.train_discard_deck import TrainDiscardDeck
from engine.utils.turn_manager import TurnManager
from engine.map.board import Board
from engine.utils.game_constants import DESTINATION_TICKET_DATA
from engine.utils.score_manager import ScoreManager
from engine.actions.draw_train_cards_action import DrawTrainCardsAction
from engine.effects.standard_effect import StandardEffect
from engine.deck.card_collection import FaceUpDrawDeck
from engine.effects.locomotive_effect import LocomotiveEffect


class Game:
    """
    Aggregate root and controller for the Ticket to Ride game.
    Owns all domain objects and orchestrates the initial game state via setup().
    """

    def __init__(self, randomizer: random.Random | None = None) -> None:
        """
        Constructor. Initialises all components but does not build state.
        Call setup() to build the initial game state.
        :param randomizer: Optional random instance for reproducible shuffling.
        """
    
        self.__randomizer = randomizer or random.Random()
        self.__board = Board()
        self.__score_manager = ScoreManager()
        self.__player: Player | None = None
        self.__is_last_round: bool = False
        self.__game_over: bool = False
        self.__current_round: int = 1
        self.__player_acted_this_turn: bool = False
        self.__market_flushed: bool = False

        self.__train_draw_deck = TrainDrawDeck()
        self.__train_discard_deck = TrainDiscardDeck()
        self.__turn_manager = TurnManager(num_players=1)
        self.__face_up_deck = FaceUpDrawDeck()
        self.__destination_ticket_draw_deck = DestinationTicketDrawDeck()
        self._populate_train_draw_deck()
        

    def setup(self) -> None:
        """
        Build the full initial game state in order:
        1. Add player
        2. Build the board map
        3. Register player with ScoreManager
        4. Deal train cards
        5. Deal destination ticket
        """
        self._add_player()
        self.__board.build_map()
        self.__score_manager.add_player_to_dict(self.__player)
        self._populate_destination_tickets()
        self._initialize_market()
        self._deal_train_cards()
        self._deal_destination_ticket()

    def _add_player(self) -> None:
        """
        Create the single player for the prototype.
        """
        self.__player = Player("Red", PlayerColor.RED)

    def _deal_train_cards(self) -> None:
        """
        Deal 7 hardcoded yellow train cards into the player's hand.
        Injects the StandardEffect required by the new TrainCard constructor.
        """
        for _ in range(7):
            # Pass both the color AND the effect to the constructor[cite: 1]
            yellow_card = TrainCard(TrainColor.YELLOW, StandardEffect())
            self.__player.draw_train_card_from_train_deck(yellow_card)

    def _deal_destination_ticket(self) -> None:
        """
        Deal 1 hardcoded London destination ticket to the player.
        """
        source_name, destination_name, points = DESTINATION_TICKET_DATA[0]
        source_city = self.__board.get_city(source_name)
        destination_city = self.__board.get_city(destination_name)
        if source_city is None or destination_city is None:
            raise ValueError("Destination ticket cities are missing from the board.")
        ticket = DestinationTicketCard(source_city, destination_city, points)
        self.__player.draw_destination_ticket(ticket)

    def on_player_action(self, action) -> None:
        """
        Validate and execute a player action.
        Apply scoring and check for last round after execution.
        :param action: A GameAction subclass instance.
        """
        if not action.validate():
            raise ValueError("Invalid action.")
        # 2. Execute the move (moves cards, updates TurnManager)
        action.execute()
        
        # 3. Check for 3 locomotives in the market and flush if necessary
        self.__market_flushed = self._check_market_locomotives()

        # Record that the player has acted if the action completes the turn.
        # Drawing train cards is incremental and only completes when the budget is used.
        if not isinstance(action, DrawTrainCardsAction):
            self.record_player_action()
        elif self.__turn_manager.has_finished_drawing():
            self.record_player_action()

        # 4. Final bookkeeping
        self._check_last_round()

    def _populate_train_draw_deck(self) -> None:
        """
        Adds a set of cards to the main deck.
        For testing, this is modified to ensure the first two cards drawn are Wilds.
        """
        cards = []
        # Add some colored cards
        for color in [TrainColor.RED, TrainColor.BLUE, TrainColor.GREEN]:
            for _ in range(10):
                cards.append(TrainCard(color, StandardEffect()))

        # Add 12 Locomotives to be shuffled with the rest
        for _ in range(12):
            cards.append(TrainCard(TrainColor.WILD, LocomotiveEffect()))

        self.__train_draw_deck.extend(cards)
        self.__train_draw_deck.shuffle(self.__randomizer)

        # Add 2 more Locomotives to the top of the deck.
        # Since draw() uses .pop(), these will be the first cards drawn.
        self.__train_draw_deck.add(TrainCard(TrainColor.WILD, LocomotiveEffect()))
        self.__train_draw_deck.add(TrainCard(TrainColor.WILD, LocomotiveEffect()))

    def _initialize_market(self) -> None:
        """Draws 5 cards from the deck to populate the face-up market."""
        for _ in range(5):
            # Draw a card from your main deck and add it to the face-up market
            card = self.__train_draw_deck.draw() 
            self.__face_up_deck.add(card)
        self.__market_flushed = self._check_market_locomotives()

    def _check_last_round(self) -> None:
        """
        Trigger the last round if the player has 0-2 train pieces remaining.
        """
        if self.__player.is_last_round_trigger():
            self.__is_last_round = True

    def end_turn(self) -> None:
        """
        Advance to the next turn.
        Resets draw counter via TurnManager.end_turn().
        """
        if self.__is_last_round:
            self.__game_over = True
        else:
            self.__current_round += 1
            self.__player_acted_this_turn = False
            self.__turn_manager.end_turn()
            self._check_last_round()

    def record_player_action(self) -> None:
        """Mark that the player has acted this turn."""
        self.__player_acted_this_turn = True

    def check_end_condition(self) -> None:
        """
        Public entry point to check if the last round should be triggered.
        Called by the UI after a player action.
        """
        self._check_last_round()

    def is_game_over(self) -> bool:
        """Returns whether the game has ended."""
        return self.__game_over

    def get_current_round(self) -> int:
        """Returns the current round number."""
        return self.__current_round

    def has_player_acted(self) -> bool:
        """Returns whether the player has acted this turn."""
        return self.__player_acted_this_turn

    def check_last_round(self) -> None:
        """
        Public entry point to check and trigger last round.
        Called by UI after a route is claimed.
        """
        self._check_last_round()

    def _populate_destination_tickets(self) -> None:
        """
        Adds a pool of destination tickets to the deck for testing.
        """
        for src_name, dest_name, pts in DESTINATION_TICKET_DATA:
            src = self.__board.get_city(src_name)
            dest = self.__board.get_city(dest_name)
            if src and dest:
                ticket = DestinationTicketCard(src, dest, pts)
                self.__destination_ticket_draw_deck.add(ticket)
            else:
                print(f"Prototype Warning: Skipped ticket '{src_name}' to '{dest_name}'. City missing from board.")
        
        self.__destination_ticket_draw_deck.shuffle(self.__randomizer)

    def _check_market_locomotives(self) -> bool:
        """
        If 3 or more face-up cards are Locomotives, discard all 5 and redraw.
        Repeats until there are fewer than 3 Locomotives.
        Returns True if a flush occurred, False otherwise.
        """
        flushed = False
        while True:
            market_cards = self.__face_up_deck.get_all_cards()
            
            loco_count = sum(1 for card in market_cards if card is not None and card.get_color() == TrainColor.WILD)
                    
            if loco_count < 3:
                break
                
            flushed = True
            # Discard all cards in the market and route to the discard deck
            for card in list(market_cards):
                if card is not None:
                    self.__face_up_deck.remove(card)
                    self.__train_discard_deck.add(card)
                
            # Replenish with 5 new cards
            for _ in range(5):
                new_card = self.draw_train_card_with_reshuffle()
                if new_card:
                    self.__face_up_deck.add(new_card)
        return flushed

    def draw_train_card_with_reshuffle(self) -> TrainCard | None:
        """
        Draws a card from the main deck. If empty, reshuffles the discard pile
        into the main deck and tries drawing again.
        """
        card = self.__train_draw_deck.draw()
        if card is None:
            if self.reshuffle_train_discards():
                card = self.__train_draw_deck.draw()
        return card

    def reshuffle_train_discards(self) -> bool:
        """
        Reshuffles the discard pile back into the draw deck.
        Returns True if a reshuffle occurred, False otherwise.
        """
        if not self.__train_discard_deck.is_empty():
            discards = self.__train_discard_deck.take_all()
            self.__train_draw_deck.extend(discards)
            self.__train_draw_deck.shuffle(self.__randomizer)
            
            # Refill any missing spots in the face-up market now that the deck has cards again
            self._replenish_market()
            return True
        return False
        
    def _replenish_market(self) -> None:
        """
        Scans the face-up market for missing cards and refills them from the main deck.
        """
        market_cards = self.__face_up_deck.get_all_cards()
        for i, card in enumerate(market_cards):
            if card is None:
                new_card = self.draw_train_card_with_reshuffle()
                if new_card:
                    self.__face_up_deck.add_card_at(i, new_card)
                    
        while len(self.__face_up_deck.get_all_cards()) < 5:
            new_card = self.draw_train_card_with_reshuffle()
            if new_card:
                self.__face_up_deck.add(new_card)
            else:
                break
   
    def discard_train_cards(self, cards: list[TrainCard]) -> None:
        """Routes spent train cards into the discard pile."""
        self.__train_discard_deck.extend(cards)
        
        # If the main deck is empty and the market is missing cards, reshuffle immediately!
        market_cards = self.__face_up_deck.get_all_cards()
        if self.__train_draw_deck.is_empty() and (len(market_cards) < 5 or None in market_cards):
            self.reshuffle_train_discards()

    def get_board(self) -> Board:
        return self.__board

    def get_player(self) -> Player:
        return self.__player

    def get_score_manager(self) -> ScoreManager:
        return self.__score_manager

    def get_train_draw_deck(self) -> TrainDrawDeck:
        return self.__train_draw_deck

    def get_destination_ticket_draw_deck(self) -> DestinationTicketDrawDeck:
        return self.__destination_ticket_draw_deck

    def get_train_discard_deck(self) -> TrainDiscardDeck:
        return self.__train_discard_deck

    def is_last_round(self) -> bool:
        return self.__is_last_round
    
    def get_turn_manager(self) -> TurnManager:
        """Returns the turn manager for the UI to check draw budget."""
        return self.__turn_manager

    def get_face_up_deck(self):
        """Returns the face-up market deck."""
        return self.__face_up_deck

    def was_market_flushed(self) -> bool:
        """Returns whether the market was flushed during the last action."""
        return self.__market_flushed