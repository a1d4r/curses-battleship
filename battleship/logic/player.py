from battleship.field.grid import Grid


class BasePlayer:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.grid.place_ships_randomly()
        self.col = 0
        self.row = 0

    def shoot(self) -> bool:
        """Shoot the selected square."""
        return self.grid.shoot_square(self.row, self.col)

    def has_won(self) -> bool:
        """Return `True` if the player has won (no enemy ships left)."""
        return self.grid.all_ships_destroyed()

    def __str__(self):
        return self.__class__.__name__


class Player(BasePlayer):
    """Class representing a real player."""
    pass


class Computer(BasePlayer):
    """Class representing a player controlled by computer."""
    pass
