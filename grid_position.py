from __future__ import annotations 
from enums import UnitClan

class GridPosition:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"GridPosition({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GridPosition):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: GridPosition) -> GridPosition:
        return GridPosition(self.x + other.x, self.y + other.y)

    def __sub__(self, other: GridPosition) -> GridPosition:
        return GridPosition(self.x - other.x, self.y - other.y)

    def check_bounds(self, row_num: int, col_num: int) -> bool:
        return 0 <= self.x < col_num and 0 <= self.y < row_num

    def adjust_with_direction(self, direction: GridPosition) -> GridPosition:
        # adjusted with front
        if direction == GridPosition(0, 1):
            return self
        # adjusted with right: rotate 90 degree
        elif direction == GridPosition(1, 0):
            return GridPosition(self.y, -self.x)
        # adjusted with back: rotate 180 degree
        elif direction == GridPosition(0, -1):
            return GridPosition(-self.x, -self.y)
        # adjusted with left: rotate 270 degree
        elif direction == GridPosition(-1, 0):
            return GridPosition(-self.y, self.x)

    def to_python(self, max_row: int) -> tuple[int, int]:
        # in python, x means xth row, y means jth column, top left is the origin
        # in game, x means col index, y means row index, bottom left is the origin
        return max_row - self.y - 1, self.x
