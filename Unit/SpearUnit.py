"""
SpearUnit class that inherits from Unit.
This unit has a unique attack pattern and higher damage.
"""
from grid_position import GridPosition
from .Unit import Unit

class SpearUnit(Unit):
    """
    A specialized unit with a unique attack pattern.
    Attack range: (0,1), (0,2), (1,1), (-1,1)
    Damage: 2
    """
    
    def __init__(self, name: str, unit_clan, loc: GridPosition, face: GridPosition):
        """Initialize a SpearUnit with the same parameters as Unit"""
        super().__init__(name, unit_clan, loc, face)

        self.attack = 2
        self.relative_attack_range = [
            GridPosition(0, 1),   # One step forward
            GridPosition(0, 2),   # Two steps forward
        ]