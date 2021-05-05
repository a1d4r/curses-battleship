from enum import Enum
from typing import List

from .square import Square, SquareState


class PlaceShipError(Exception):
    pass


class Direction(Enum):
    """Directions to locate ship in the field."""
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def __init__(self, dx: int, dy: int):
        """
        Init with offset in horizontal and vertical coordinates
        while moving in this direction.
        """
        self.dx = dx
        self.dy = dy


class Ship:
    """Class representing ship in the field."""
    def __init__(self, squares: List[Square]):
        self.squares = squares
        for square in squares:
            square.ship = self

    @property
    def size(self) -> int:
        """Return size of the ship, in squares."""
        return len(self.squares)

    def is_destroyed(self) -> bool:
        """Check if the ship is completely destroyed."""
        return all(square.state == SquareState.HIT for square in self.squares)

    def __str__(self):
        return ''.join(str(square) for square in self.squares)

    def __repr__(self):
        return f'Ship(id={hex(id(self))}, size={self.size}, destroyed={self.is_destroyed()})'
