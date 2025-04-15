"""
SpearUnit class that inherits from Unit.
This unit has a unique attack pattern and higher damage.
"""
from grid_position import GridPosition
from .Unit import Unit

class GuardianUnit(Unit):
    def __init__(self, name: str, unit_clan, loc: GridPosition, face: GridPosition):
        """Initialize a SpearUnit with the same parameters as Unit"""
        super().__init__(name, unit_clan, loc, face)
        self.attack = 0
        self.relative_attack_range = []
        self.relative_defense_range = [
            GridPosition(0, 1),
            GridPosition(-1, 1),
            GridPosition(1, 1),
            GridPosition(-1, 2),
            GridPosition(1, 2),
        ]
        self.guardian_defense = 1