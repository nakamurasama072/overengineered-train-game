from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod

from engine.game import Game
from ui.map_ui import MapUI
from ui.player_tool_ui import PlayerToolUI
from ui.sidebar_ui import SidebarUI
from ui.user_interface import UserInterface
from engine.actions.draw_train_cards_action import DrawTrainCardsAction
from engine.actions.draw_destination_tickets_action import DrawDestinationTicketsAction
BG_ROOT  = "#0f1923"
ACCENT   = "#c9a227"
FG       = "#e0e0e0"
BTN_BG   = "#c9a227"
BTN_FG   = "#1a1a2e"

SETUP_DELAY_MS = 900  # delay between each setup phase animation

class GameUI(tk.Tk, UserInterface):
    """
    Root window and main controller for the UI.
    Owns all panels and drives the setup animation sequence.
    """

    SIDEBAR_W_RATIO    = 0.20
    PLAYER_TOOL_H_RATIO = 0.25

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__sidebar: SidebarUI | None = None
        self.__map_ui: MapUI | None = None
        self.__player_tool: PlayerToolUI | None = None
        self.build_ui()

    def build_ui(self) -> None:
        # Window setup
        self.attributes("-fullscreen", True) # This is why it feels "zoomed"
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.configure(bg=BG_ROOT)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        sidebar_w     = int(sw * self.SIDEBAR_W_RATIO)
        player_tool_h = int(sh * self.PLAYER_TOOL_H_RATIO)
        
        # 1. CREATE AND PACK THE SIDEBAR FIRST[cite: 14]
        self.__sidebar = SidebarUI(
            self, 
            width=sidebar_w, 
            on_market_click=self._on_market_card_clicked,
            on_train_deck_click=self._on_train_deck_clicked,
            on_ticket_deck_click=self._on_ticket_deck_clicked
        )
        self.__sidebar.pack(side="left", fill="y")

        # 2. CREATE THE RIGHT CONTAINER[cite: 14]
        right = tk.Frame(self, bg=BG_ROOT)
        right.pack(side="left", fill="both", expand=True)

        # 3. ATTACH MAP AND TOOLS TO THE RIGHT CONTAINER[cite: 14, 15, 17]
        map_w = sw - sidebar_w
        map_h = sh - player_tool_h

        self.__map_ui = MapUI(right, self.__game.get_board(), map_w, map_h)
        self.__map_ui.pack(fill="both", expand=True)

        self.__player_tool = PlayerToolUI(right, height=player_tool_h)
        self.__player_tool.pack(fill="x", side="bottom")

        # Start frame logic remains at the end
        self.__start_frame = tk.Frame(self, bg=BG_ROOT)
        self.__start_frame.place(relx=0.5, rely=0.5, anchor="center")


        tk.Label(
            self.__start_frame,
            text="TICKET TO RIDE",
            bg=BG_ROOT,
            fg=ACCENT,
            font=("Georgia", 36, "bold"),
        ).pack(pady=(0, 8))

        tk.Label(
            self.__start_frame,
            text="London Edition",
            bg=BG_ROOT,
            fg=FG,
            font=("Georgia", 14),
        ).pack(pady=(0, 32))

        tk.Button(
            self.__start_frame,
            text="START GAME",
            bg=BTN_BG,
            fg=BTN_FG,
            font=("Georgia", 14, "bold"),
            padx=32,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self._on_start_clicked,
        ).pack()

    def _on_start_clicked(self) -> None:
        """
        Called when the START button is clicked.
        Runs game.setup() then animates each phase sequentially.
        """
        self.__start_frame.place_forget()
        self.__game.setup()
        self._animate_phase_1()

    def _animate_phase_1(self) -> None:
        """Phase 1 — Build the map."""
        self.__sidebar.set_status("Building the map...")
        self.__sidebar.add_log("Building map")
        self.__map_ui.draw_map()
        self.after(SETUP_DELAY_MS, self._animate_phase_2)

    def _animate_phase_2(self) -> None:
        """Phase 2 — Deal train cards."""
        self.__sidebar.set_status("Drawing train cards...")
        self.__sidebar.add_log("Dealt 5 train cards")
        train_cards = self.__game.get_player().get_train_cards()
        self.__player_tool.show_train_cards(train_cards)
        self.after(SETUP_DELAY_MS, self._animate_phase_3)

    def _animate_phase_3(self) -> None:
        """Phase 3 — Deal destination ticket."""
        self.__sidebar.set_status("Drawing destination ticket...")
        self.__sidebar.add_log("Dealt 1 destination ticket")
        tickets = self.__game.get_player().get_destination_tickets()
        self.__player_tool.show_destination_tickets(tickets)
        self.after(SETUP_DELAY_MS, self._animate_complete)

    def _on_end_turn_clicked(self) -> None:
        """Called when the player clicks End Turn."""
        cards_drawn = self.__game.get_turn_manager().get_cards_drawn_this_turn()
        if cards_drawn == 1:
            self.__sidebar.set_status("You must draw a second card before ending your turn.")
            return
        self.__game.end_turn()
        self.__sidebar.add_log(f"Turn ended — Round {self.__game.get_current_round()}")

        if self.__game.is_game_over():
            self._show_game_over()
        elif self.__game.is_last_round():
            self.__sidebar.set_status("Last round! Take your final turn.")
        else:
            self.__sidebar.set_status("Turn ended.")

    def _show_game_over(self) -> None:
        """Display a game over overlay centered over the full game window."""
        player = self.__game.get_player()
        score = self.__game.get_score_manager().get_score(player)

        overlay = tk.Frame(self, bg="#0f1923", bd=2, relief="ridge")
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=280)

        tk.Label(
            overlay,
            text="GAME OVER",
            bg="#0f1923",
            fg="#c9a227",
            font=("Georgia", 28, "bold"),
        ).pack(pady=(36, 8))

        tk.Frame(overlay, bg="#c9a227", height=2).pack(fill="x", padx=40)

        tk.Label(
            overlay,
            text=player.get_name(),
            bg="#0f1923",
            fg="#e0e0e0",
            font=("Georgia", 16),
        ).pack(pady=(18, 4))

        tk.Label(
            overlay,
            text=f"Final Score: {score}",
            bg="#0f1923",
            fg="#c9a227",
            font=("Georgia", 22, "bold"),
        ).pack(pady=(0, 24))

        tk.Button(
            overlay,
            text="END GAME",
            bg="#c9a227",
            fg="#0f1923",
            font=("Georgia", 11, "bold"),
            padx=24,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.destroy,
        ).pack()

    def _animate_complete(self) -> None:
        """All setup phases done."""
        self.__sidebar.set_status("Setup complete. Game ready.")
        self.__sidebar.add_log("Setup complete")
        self.__sidebar.update_train_pieces(self.__game.get_player().get_train_pieces())
        self.__map_ui.set_on_route_click(self._on_route_clicked)
        self.__player_tool.set_on_end_turn_callback(self._on_end_turn_clicked)
        market_cards = self.__game.get_face_up_deck().get_all_cards()
        self.__sidebar.update_market(market_cards)

    def _on_route_clicked(self, route) -> None:
        """
        Handle a route click. Attempt to claim the route for the player.
        """
        # 1. NEW: Block action if player is in the middle of drawing cards
        if self.__game.get_turn_manager().get_cards_drawn_this_turn() > 0:
            self.__sidebar.set_status("Cannot claim: You have already drawn cards this turn.")
            return
        
        # Block if player has already completed their action for the turn
        if self.__game.has_player_acted():
            self.__sidebar.set_status("Cannot claim: You have already acted this turn.")
            return

        player = self.__game.get_player()
        try:
            player.claim_route(route)
            score_manager = self.__game.get_score_manager()
            points = score_manager.get_route_score(route.get_length())
            score_manager.add_score(player, points)
            self.__game.check_last_round()

            # Draw train pieces on the map
            self.__map_ui.draw_train_pieces(route, player)

            # Refresh UI
            self.__player_tool.show_train_cards(player.get_train_cards())
            self.__player_tool.show_destination_tickets(player.get_destination_tickets())
            self.__sidebar.update_train_pieces(player.get_train_pieces())
            
            status_msg = f"Claimed {route.get_start_city().get_name()} → {route.get_destination_city().get_name()} ({points} pts)"
            self.__sidebar.set_status(status_msg)
            self.__sidebar.add_log(status_msg)

            if self.__game.is_last_round():
                self.__sidebar.set_status("Last round triggered!")
                self.__sidebar.add_log("Last round triggered")

            # Mark that the player has acted and must now end their turn
            self.__game.record_player_action()
            self.__sidebar.set_status("Route claimed. Please end your turn.")

        except ValueError as e:
            self.__sidebar.set_status(f"Cannot claim: {e}")

    def _on_market_card_clicked(self, card_index: int) -> None:
        """Mediator: Packages the action and refreshes visuals."""
        # Block if player has already completed their action for the turn
        if self.__game.has_player_acted():
            self.__sidebar.set_status("Cannot draw: You have already acted this turn.")
            return

        # 1. Create and send the action
        action = DrawTrainCardsAction(
            player=self.__game.get_player(),
            turn_manager=self.__game.get_turn_manager(), 
            draw_deck=self.__game.get_train_draw_deck(),
            face_up_deck=self.__game.get_face_up_deck(),
            card_index=card_index
        )
        try:
            self.__game.on_player_action(action)
        except ValueError as e:
            self.__sidebar.set_status(f"Cannot draw: {e}")
            return
        
        # 2. Update all UI components to reflect the new game state
        player = self.__game.get_player()
        self.__player_tool.show_train_cards(player.get_train_cards())
        
        # Refresh the market cards in the sidebar
        market_cards = self.__game.get_face_up_deck().get_all_cards() 
        self.__sidebar.update_market(market_cards)
        
        # Log the action
        self.__sidebar.add_log(f"Drew card from market index {card_index}")
        
        # Notify if the market was flushed
        if self.__game.was_market_flushed():
            self.__sidebar.add_log("Market flushed: 3 Locomotives!")
            self.__sidebar.set_status("Market flushed due to 3 Locomotives.")

    # 2. Add the mediator method for drawing a blind train card
    def _on_train_deck_clicked(self) -> None:
        """Mediator: Packages the blind draw action and refreshes visuals."""
        
        # Block if player has already completed their action for the turn
        if self.__game.has_player_acted():
            self.__sidebar.set_status("Cannot draw: You have already acted this turn.")
            return

        # 1. Create and execute the action (leaving card_index empty defaults it to None!)
        action = DrawTrainCardsAction(
            player=self.__game.get_player(),
            turn_manager=self.__game.get_turn_manager(),
            draw_deck=self.__game.get_train_draw_deck(),
            face_up_deck=self.__game.get_face_up_deck()
        )
        try:
            self.__game.on_player_action(action)
        except ValueError as e:
            self.__sidebar.set_status(f"Cannot draw: {e}")
            return

        # 2. Now refresh the UI with the newly updated hand
        player = self.__game.get_player()
        self.__player_tool.show_train_cards(player.get_train_cards())
        
        self.__sidebar.add_log("Drew a blind train card.")

    def _on_ticket_deck_clicked(self) -> None:
        """Mediator: Handle clicking the destination ticket deck with a modal pop-up."""
        
        # 1. Block if the player is mid-turn (e.g. already drew 1 train card)
        if self.__game.get_turn_manager().get_cards_drawn_this_turn() > 0:
            self.__sidebar.set_status("Cannot draw tickets: You already drew a train card.")
            return

        # Block if player has already completed their action for the turn
        if self.__game.has_player_acted():
            self.__sidebar.set_status("Cannot draw tickets: You have already acted this turn.")
            return

        ticket_deck = self.__game.get_destination_ticket_draw_deck()
        
        # 2. Draw up to 3 cards into "limbo"
        limbo_cards = []
        for _ in range(3):
            card = ticket_deck.draw()
            if card:
                limbo_cards.append(card)
                
        if not limbo_cards:
            self.__sidebar.set_status("The Destination Ticket deck is empty!")
            return

        # 3. Create a modal pop-up window
        modal = tk.Toplevel(self)
        modal.title("Select Destination Tickets")
        modal.geometry("400x350")
        modal.configure(bg="#0f1923")
        modal.grab_set() # Locks the main window until this is resolved
        
        tk.Label(
            modal, text="Keep at least ONE ticket:", 
            bg="#0f1923", fg="#c9a227", font=("Georgia", 14, "bold")
        ).pack(pady=15)

        # Variables to track which checkboxes are ticked
        checkbox_vars = []
        
        for ticket in limbo_cards:
            var = tk.BooleanVar(value=False)
            checkbox_vars.append(var)
            
            text = f"{ticket.get_source().get_name()} → {ticket.get_destination().get_name()} ({ticket.get_points()} pts)"
            chk = tk.Checkbutton(
                modal, text=text, variable=var,
                bg="#0f1923", fg="#e0e0e0", selectcolor="#2a2a4a",
                font=("Georgia", 11), cursor="hand2"
            )
            chk.pack(anchor="w", padx=40, pady=5)

        def on_confirm():
            kept = []
            returned = []
            for i, var in enumerate(checkbox_vars):
                if var.get():
                    kept.append(limbo_cards[i])
                else:
                    returned.append(limbo_cards[i])
                    
            if len(kept) < 1:
                self.__sidebar.set_status("You must select at least 1 ticket.")
                return
                
            # 4. Create and dispatch the Action
            action = DrawDestinationTicketsAction(
                player=self.__game.get_player(),
                turn_manager=self.__game.get_turn_manager(),
                ticket_deck=ticket_deck,
                kept_tickets=kept,
                returned_tickets=returned
            )
            self.__game.on_player_action(action)
            
            # 5. Refresh UI and End Turn
            player = self.__game.get_player()
            self.__player_tool.show_destination_tickets(player.get_destination_tickets())
            self.__sidebar.add_log(f"Drew {len(kept)} Destination Tickets")
            self.__sidebar.set_status("Tickets drawn. Please skip/end your turn.")
            
            modal.destroy()

        def on_close():
            # If the user clicks the X to cancel, put the cards back on top of the deck
            for card in reversed(limbo_cards):
                ticket_deck.add(card) # Re-add to top
            modal.destroy()

        modal.protocol("WM_DELETE_WINDOW", on_close)

        tk.Button(
            modal, text="CONFIRM SELECTION", command=on_confirm,
            bg="#c9a227", fg="#1a1a2e", font=("Georgia", 12, "bold"),
            padx=20, pady=10, cursor="hand2"
        ).pack(pady=30)