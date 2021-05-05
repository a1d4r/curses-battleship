from enum import Enum

from battleship.logic.settings import UNKNOWN_CHAR, FREE_CHAR, OCCUPIED_CHAR, \
    HIT_CHAR, DESTROYED_CHAR


class SquareState(Enum):
    """States of a square in the grid."""
    FREE = (0, FREE_CHAR)  # Free, the ship can be placed here
    RESERVED = (1, FREE_CHAR)  # There is a ship in an adjacent cell
    OCCUPIED = (2, OCCUPIED_CHAR)  # There is a ship in this cell
    HIT = (3, HIT_CHAR)  # The part of the ship in this cell is hit

    def __init__(self, id: int, char: str):
        """Init with id (int number) and char (square text representation)."""
        self.id = id
        self.char = char


class Square:
    """Class representing square of the field."""
    def __init__(self):
        self.ship = None
        self.discovered = False
        self.state = SquareState.FREE

    def shoot(self) -> bool:
        """Shoot at this square. Return `True` if a ship was hit."""
        if self.discovered:
            return False
        self.discovered = True
        if self.state == SquareState.OCCUPIED:
            self.state = SquareState.HIT
            return True
        return False

    def is_free(self) -> bool:
        """Return True if there is (was) no ship in the square."""
        return self.ship is None

    def str_for_enemy(self) -> str:
        """Return character representing this square from an enemy's perspective."""
        if self.discovered:
            return str(self)
        else:
            return UNKNOWN_CHAR

    def __str__(self):
        if self.ship is not None and self.ship.is_destroyed():
            return DESTROYED_CHAR
        else:
            return self.state.char

    def __repr__(self):
        return f'Square(id={hex(id(self))}, state={self.state}, discovered={self.discovered})'
