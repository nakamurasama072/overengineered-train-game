from __future__ import annotations

from engine.game import Game
from ui.game_ui import GameUI


def main() -> None:
    game = Game()
    app = GameUI(game)
    app.mainloop()


if __name__ == "__main__":
    main()