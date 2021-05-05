from typing import Dict, Tuple
from random import choice, randrange

from .square import Square, SquareState
from .ship import Ship, Direction, PlaceShipError
from battleship.logic.settings import MAX_PERCENT_SQUARES_OCCUPIED


class Grid:
    """Class representing battle field."""
    def __init__(self, height: int = 10, width: int = 10):
        self.height = height
        self.width = width
        self._grid = [[Square() for _ in range(width)] for _ in range(height)]
        self._ships = []

    def _get_ship_endpoints(self, row: int, col: int, size: int,
                            dir_: Direction) -> Tuple[int, int, int, int]:
        """Return endpoints of a ship such that row1 <= row2 and col1 <= col2."""
        row1, row2 = row, row + dir_.dy * (size - 1)
        col1, col2 = col, col + dir_.dx * (size - 1)
        row1, row2 = min(row1, row2), max(row1, row2)
        col1, col2 = min(col1, col2), max(col1, col2)
        return row1, col1, row2, col2

    def _free_for_ship(self, row: int, col: int, size: int, dir_: Direction) -> bool:
        """Check if a ship can be placed between the specified points."""
        row1, col1, row2, col2 = self._get_ship_endpoints(row, col, size, dir_)
        if row1 < 0 or row2 >= self.height or col1 < 0 or col2 >= self.width:
            return False
        else:
            return all(self._grid[row][col].state == SquareState.FREE
                       for row in range(row1, row2 + 1)
                       for col in range(col1, col2 + 1))

    def _place_ship(self, row: int, col: int, size: int, dir_: Direction) -> None:
        """Place a ship in the specified position."""
        row1, col1, row2, col2 = self._get_ship_endpoints(row, col, size, dir_)
        if not self._free_for_ship(row, col, size, dir_):
            raise PlaceShipError('Ship is out of the field')

        # Reserve squares
        for row in range(max(0, row1 - 1), min(self.height, row2 + 2)):
            for col in range(max(0, col1 - 1), min(self.width, col2 + 2)):
                self._grid[row][col].state = SquareState.RESERVED

        # Occupy cells, place ship
        squares = []
        for row in range(row1, row2 + 1):
            for col in range(col1, col2 + 1):
                self._grid[row][col].state = SquareState.OCCUPIED
                squares.append(self._grid[row][col])
        self._ships.append(Ship(squares))

    def _place_ship_randomly(self, size: int) -> None:
        """Place a ship of the specified size randomly in the field."""
        # The for loop is needed to avoid running infinite loop
        for i in range(100 * self.width * self.height):
            dir_ = choice([dir_ for dir_ in Direction])
            row = randrange(self.height)
            col = randrange(self.width)
            try:
                self._place_ship(row, col, size, dir_)
            except PlaceShipError:
                pass
            else:
                break
        else:
            raise PlaceShipError(f'Cannot place a ship of size {size} in the grid.')

    def _calculate_ships_count(self) -> Dict[int, int]:
        """Return a dictionary containing count of ship by its size."""
        num_ships_by_size = {1: 1}
        num_ships, max_size = 1, 1
        while 100 * num_ships <= MAX_PERCENT_SQUARES_OCCUPIED * self.width * self.height:
            max_size += 1
            num_ships_by_size[max_size] = 1
            for size in range(1, max_size):
                num_ships_by_size[size] += 1
            num_ships += sum(range(max_size + 1))
        for size in range(1, max_size + 1):  # to make ships take < 20% of the field
            num_ships_by_size[size] -= 1
        return num_ships_by_size

    def place_ships_randomly(self) -> None:
        """Fill the field by randomly placed ships."""
        num_ships_by_size = self._calculate_ships_count()

        for size, num in reversed(num_ships_by_size.items()):  # larger ships first
            for _ in range(num):
                self._place_ship_randomly(size)

    def shoot_square(self, row: int, col: int) -> bool:
        """
        Shoot a square at the specified position.
        Return `True` if a ship was hit.
        """
        return self._grid[row][col].shoot()

    def all_ships_destroyed(self) -> bool:
        """Return `True` if all ships in this grid are destroyed."""
        return all(ship.is_destroyed() for ship in self._ships)

    def __getitem__(self, item):
        return self._grid[item]

    def __len__(self):
        return len(self._grid)

    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self._grid)

    def __repr__(self):
        return f'Grid(id={hex(id(self))}, height={self.height}, width={self.width})'
