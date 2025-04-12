from enums import UnitClan
from grid_position import GridPosition
from Unit import Unit
from collections import defaultdict

class LevelGrid:
    units: dict[GridPosition, Unit]
    COL_NUM: int
    ROW_NUM: int

    def __init__(self, row_num: int, col_num: int) -> None:
        self.COL_NUM = col_num
        self.ROW_NUM = row_num
        self.units = {}

    def move(self, unit: Unit, destination: GridPosition) -> None:
        # remove unit from old position
        if unit.loc in self.units:
            del self.units[unit.loc]
        # add unit to new position
        self.units[destination] = unit
        # update unit's location
        unit.loc = destination

    def attack(self, destination: GridPosition, damage: int) -> None:
        # Check if the destination is valid and has a unit
        if destination in self.units:
            unit = self.units[destination]
            # Apply damage to the unit
            unit.health -= damage
            # If the unit's health drops to 0 or below, remove it from the grid
            if unit.health <= 0:
                del self.units[destination]

    def to_string(self) -> str:
        """Convert the grid to a string representation"""
        # Create an empty grid
        grid = [['  o  ' for _ in range(self.COL_NUM)] for _ in range(self.ROW_NUM)]
        
        # Fill in the units
        for grid_position, unit in self.units.items():
            # Convert grid position to Python coordinates
            python_pos = grid_position.to_python(self.ROW_NUM)
            row, col = python_pos
            
            if 0 <= row < self.ROW_NUM and 0 <= col < self.COL_NUM:
                grid[row][col] = f"*{unit.name[0]} {unit.health}*"
        
        # Add attack range indicators
        for grid_position, unit in self.units.items():
            for attack_pos in unit.attack_range:
                python_pos = attack_pos.to_python(self.ROW_NUM)
                row, col = python_pos
                
                if 0 <= row < self.ROW_NUM and 0 <= col < self.COL_NUM and grid[row][col] == '  o  ':
                    grid[row][col] = f"# {unit.name[0].lower()} #"
        
        # Convert to string
        result = ""
        for row in reversed(range(self.ROW_NUM)):
            for col in range(self.COL_NUM):
                result += grid[row][col] + " "
            result += "\n"
        
        return result

    @property
    def ally_attack_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and attack counts for ally units"""
        attack_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Ally:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
        return attack_grid

    @property
    def enemy_attack_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and attack counts for enemy units"""
        attack_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Enemy:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
        return attack_grid

    @property
    def movement_request(self) -> dict[GridPosition, list[Unit]]:
        # return a dict of unit name and its destination
        movement_request = defaultdict(lambda: [])
        for unit in self.units.values():
            if unit.is_marching:
                destination = unit.move_destination
                if destination:
                    movement_request[destination].append(unit)
        return movement_request
