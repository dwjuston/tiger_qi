"""
SpearUnit class that inherits from Unit.
This unit has a unique attack pattern and higher damage.
"""

from grid_position import GridPosition
from .Unit import Unit


class SwordUnit(Unit):
    def __init__(self, name: str, unit_clan, loc: GridPosition, face: GridPosition):
        """Initialize a SpearUnit with the same parameters as Unit"""
        super().__init__(name, unit_clan, loc, face)

        self.attack = 1
        self.relative_attack_range = [
            GridPosition(0, 1),  # One step forward
            GridPosition(-1, 0),  # Left
            GridPosition(1, 0),  # Right
        ]
