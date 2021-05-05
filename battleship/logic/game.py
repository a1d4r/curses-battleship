import curses
import curses.ascii
from random import randrange
from functools import singledispatchmethod

from .player import Player, Computer, BasePlayer
from battleship.ui.display import DisplayManager
from battleship.field.grid import Grid


class Game:
    """Class representing main logic of the game."""
    def __init__(self, scr, display_manager: DisplayManager,
                 grid_height: int, grid_width: int):
        self.scr = scr
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.display_manager = display_manager
        self._players = [Player(Grid(grid_height, grid_width)),
                         Computer(Grid(grid_height, grid_width))]
        self._current_player = 0  # index of player whose turn is
        self.menu_called = False  # to be able to open menu using ESC key
        self.game_over = False

    def main_loop(self) -> None:
        """Main loop of the game (player moves)"""
        while True:
            player = self._players[self._current_player]
            hit = True
            while hit:
                self.select_square(player)
                if self.menu_called:  # go to menu
                    self.menu_called = False
                    return
                hit = player.shoot()
                if player.has_won():
                    self.display_manager.display_end_game_message(player)
                    self.game_over = True
                    return
            self._current_player = (self._current_player + 1) % len(self._players)

    # Using dispatching instead of polymorphism to avoid storing curses code
    # in Player classes
    @singledispatchmethod
    def select_square(self, player: BasePlayer) -> None:
        """Player selects a square to shot"""
        raise NotImplementedError()

    @select_square.register(Player)
    def _(self, player: BasePlayer) -> None:
        """Real player selects a square to shoot."""
        while True:
            self.display_manager.display_grid(
                player.grid, player.row, player.col, player)
            key = self.scr.getch()

            if key == curses.KEY_UP:
                player.row = max(0, player.row - 1)
            elif key == curses.KEY_RIGHT:
                player.col = min(player.grid.width - 1, player.col + 1)
            elif key == curses.KEY_DOWN:
                player.row = min(player.grid.height - 1, player.row + 1)
            elif key == curses.KEY_LEFT:
                player.col = max(0, player.col - 1)
            elif key in {curses.KEY_ENTER, 10, 13}:  # enter
                break
            elif key == curses.ascii.ESC:
                self.menu_called = True
                return

    @select_square.register(Computer)
    def _(self, player: BasePlayer) -> None:
        """Computer selects a square to shoot."""
        player.row = randrange(player.grid.height)
        player.col = randrange(player.grid.width)
        self.display_manager.display_grid(
            player.grid, player.row, player.col, player)
        key = self.scr.getch()
        if key == curses.ascii.ESC:
            self.menu_called = True

    def __getstate__(self):
        attributes = self.__dict__.copy()
        del attributes['display_manager']
        del attributes['scr']
        return attributes

