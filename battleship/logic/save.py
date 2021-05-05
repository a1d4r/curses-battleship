import pickle

from battleship.logic.game import Game
from .settings import SAVE_FILENAME


class SaveError(Exception):
    pass


class SaveManager:
    """Class representing manager for saving/loading game states."""
    def save_game(self, game: Game) -> None:
        """Save game state to a file."""
        if game is None:
            raise SaveError(f'The game has not started yet')
        try:
            with open(SAVE_FILENAME, 'wb') as f:
                pickle.dump(game, f)
        except OSError as e:
            raise SaveError(f'Cannot open file: {e.strerror}')

    def load_game(self, scr, display_manager) -> Game:
        """Load game state from a file."""
        try:
            with open(SAVE_FILENAME, 'rb') as f:
                game = pickle.load(f)
            game.display_manager = display_manager
            game.scr = scr
            return game
        except OSError as e:
            raise SaveError(f'Cannot open file: {e.strerror}')
        except pickle.PickleError as e:
            raise SaveError(f'Wrong format of data: {str(e)}')
