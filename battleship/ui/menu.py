import curses
import curses.ascii
from enum import Enum
from typing import List

from battleship.ui.display import DisplayManager
from battleship.logic.game import Game
from battleship.logic.save import SaveManager, SaveError


class MenuEntries(Enum):
    """Entries of the main menu."""
    PLAY = (0, 'Play')
    SAVE = (1, 'Save')
    LOAD = (2, 'Load')
    EXIT = (3, 'Exit')

    def __init__(self, index: int, label: str):
        self.index = index
        self.label = label

    @staticmethod
    def as_list() -> List[str]:
        return [entry.label for entry in MenuEntries]


class Menu:
    """Class representing menu."""
    def __init__(self, scr, grid_height: int, grid_width: int):
        self.scr = scr
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.display_manager = DisplayManager(scr)
        self.game = None
        self.exit = False

    def main_loop(self) -> None:
        """Main loop of the game (menu)"""
        menu_entry_index = 0

        while not self.exit:
            self.display_manager.display_menu(MenuEntries.as_list(),
                                              menu_entry_index)
            key = self.scr.getch()

            if key == curses.KEY_UP:
                menu_entry_index = max(0, menu_entry_index - 1)
            elif key == curses.KEY_DOWN:
                menu_entry_index = min(len(MenuEntries) - 1, menu_entry_index + 1)
            elif key in {curses.KEY_ENTER, 10, 13}:  # enter
                self.select_menu_entry(menu_entry_index)
            elif key == ord('q'):  # exit
                break

            self.scr.refresh()

    def select_menu_entry(self, menu_entry_index: int) -> None:
        if menu_entry_index == MenuEntries.PLAY.index:
            if self.game is None or self.game.game_over:
                self.game = Game(self.scr, self.display_manager,
                                 self.grid_height, self.grid_width)
            self.game.main_loop()
        elif menu_entry_index == MenuEntries.SAVE.index:  # Save
            save_manager = SaveManager()
            try:
                save_manager.save_game(self.game)
            except SaveError as e:
                self.display_manager.display_message_center(str(e))
            else:
                self.display_manager.display_message_center(
                    'The game has been successfully saved!')
        elif menu_entry_index == MenuEntries.LOAD.index:  # Load
            save_manager = SaveManager()
            try:
                self.game = save_manager.load_game(
                    self.scr, self.display_manager)
            except SaveError as e:
                self.display_manager.display_message_center(str(e))
            else:
                self.game.main_loop()
        elif menu_entry_index == MenuEntries.EXIT.index:  # Exit
            self.exit = True
