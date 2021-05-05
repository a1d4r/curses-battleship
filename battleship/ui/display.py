import curses
import curses.ascii
from curses import textpad
from typing import List

from battleship.logic.player import Player, Computer, BasePlayer
from battleship.field.grid import Grid
from battleship.logic.settings import DEFEAT_MESSAGE, VICTORY_MESSAGE


class DisplayManager:
    """Class representing manager for displaying game element on the screen."""
    def __init__(self, scr):
        self.scr = scr

    def display_grid(self, grid: Grid, row: int, col: int, player: BasePlayer) -> None:
        """Display grid on the screen with the specified square selected."""
        self.scr.clear()
        height, width = self.scr.getmaxyx()

        rect_corners = (
            height // 2 - grid.height // 2 - 1,
            width // 2 - grid.width - 1,
            height // 2 + (grid.height + 1) // 2,
            width // 2 + grid.width + 1,
        )

        move_str = f'Move of a {str(player)}'
        move_str_y = height // 2 - grid.height // 2 - 2
        move_str_x = width // 2 - len(move_str) // 2 + 1
        self.scr.addstr(move_str_y, move_str_x, move_str)

        textpad.rectangle(self.scr, *rect_corners)

        for i, row_list in enumerate(grid):
            for j, square in enumerate(row_list):
                y = rect_corners[0] + i + 1
                x = rect_corners[1] + j * 2 + 2
                if isinstance(player, Player):
                    char = square.str_for_enemy()
                else:
                    char = str(square)
                if i == row and j == col:
                    self.scr.addstr(y, x, char, curses.color_pair(1))
                else:
                    self.scr.addstr(y, x, char)
        self.scr.refresh()

    def display_menu(self, menu: List[str], menu_entry_index: int) -> None:
        """Display menu on the screen with the specified selected entry."""
        self.scr.clear()
        height, width = self.scr.getmaxyx()

        for i, entry in enumerate(menu):
            x = width // 2 - len(entry) // 2
            y = height // 2 - len(menu) // 2 + i
            if i == menu_entry_index:
                self.scr.addstr(y, x, entry, curses.color_pair(1))
            else:
                self.scr.addstr(y, x, entry)

        self.scr.refresh()

    def display_end_game_message(self, player: BasePlayer) -> None:
        """Display message like You won (or you lost)."""
        if isinstance(player, Computer):
            message = DEFEAT_MESSAGE
        elif isinstance(player, Player):
            message = VICTORY_MESSAGE
        else:
            raise NotImplementedError

        self.display_message_center(message)

    def display_message_center(self, message: str) -> None:
        """Display message at the center of the screen."""
        self.scr.clear()
        height, width = self.scr.getmaxyx()
        y = height // 2
        x = width // 2 - len(message) // 2
        self.scr.addstr(y, x, message)
        self.scr.refresh()
        self.scr.getch()
