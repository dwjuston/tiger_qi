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


    def get_surrounding_grid_cells(self, grid_position: GridPosition) -> list[GridPosition]:
        """Get the surrounding grid cells of a given position"""
        surrounding_cells = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_pos = GridPosition(grid_position.x + dx, grid_position.y + dy)
                if 0 <= new_pos.x < self.COL_NUM and 0 <= new_pos.y < self.ROW_NUM:
                    surrounding_cells.append(new_pos)
        return surrounding_cells
    def count_surrounding_opponents(self, unit: Unit) -> int:
        cells = self.get_surrounding_grid_cells(unit.loc)
        count = 0
        for cell in cells:
            if cell in self.units and self.units[cell].unit_clan != unit.unit_clan:
                count += 1
        return count


    @property
    def ally_attack_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and attack counts for ally units"""
        attack_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Ally:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
            elif unit.unit_clan == UnitClan.Enemy and unit.friendly_fire:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
        return attack_grid

    @property
    def ally_defense_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and defense counts for ally units"""
        defense_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Ally:
                for defense_pos in unit.defense_range:
                    defense_grid[defense_pos] += unit.guardian_defense
                if unit.self_defense > 0:
                    defense_grid[unit.loc] += unit.self_defense  # add self defense
        return defense_grid

    @property
    def ally_attack_result_grid(self) -> dict[GridPosition, int]:
        ally_attack_grid = self.ally_attack_grid
        enemy_defense_grid = self.enemy_defense_grid

        # remove attack positions with no unit
        keys_to_remove = []
        for attack_pos, damage in ally_attack_grid.items():
            if attack_pos not in self.units or self.units[attack_pos].unit_clan == UnitClan.Ally:
                keys_to_remove.append(attack_pos)
        for key in keys_to_remove:
            del ally_attack_grid[key]

        # defense
        keys_to_remove = []
        for attack_pos, damage in ally_attack_grid.items():
            if attack_pos in enemy_defense_grid:
                damage -= enemy_defense_grid[attack_pos]
                ally_attack_grid[attack_pos] = damage
            if damage < 0:
                keys_to_remove.append(attack_pos)
        for key in keys_to_remove:
            del ally_attack_grid[key]

        # coop: if the unit under attack is surrounded by 2 opponent units, damage plus 1; if 3 or more, damage plus 2
        for attack_pos, damage in ally_attack_grid.items():
            unit_under_attack = self.units.get(attack_pos)
            surrounding_opponent_count = self.count_surrounding_opponents(unit_under_attack)
            if surrounding_opponent_count == 2:
                damage += 1
                ally_attack_grid[attack_pos] = damage
            elif surrounding_opponent_count >= 3:
                damage += 2
                ally_attack_grid[attack_pos] = damage

        return ally_attack_grid

    @property
    def enemy_attack_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and attack counts for enemy units"""
        attack_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Enemy:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
            elif unit.unit_clan == UnitClan.Ally and unit.friendly_fire:
                for attack_pos in unit.attack_range:
                    attack_grid[attack_pos] += unit.attack
        return attack_grid

    @property
    def enemy_defense_grid(self) -> dict[GridPosition, int]:
        """Get a dictionary of positions and defense counts for enemy units"""
        defense_grid = defaultdict(lambda: 0)
        for unit in self.units.values():
            if unit.unit_clan == UnitClan.Enemy:
                for defense_pos in unit.defense_range:
                    defense_grid[defense_pos] += unit.guardian_defense
                if unit.self_defense > 0:
                    # add self defense
                    defense_grid[unit.loc] += unit.self_defense
        return defense_grid

    @property
    def enemy_attack_result_grid(self) -> dict[GridPosition, int]:
        enemy_attack_grid = self.enemy_attack_grid
        ally_defense_grid = self.ally_defense_grid

        # remove attack positions with no unit
        keys_to_remove = []
        for attack_pos, damage in enemy_attack_grid.items():
            if attack_pos not in self.units or self.units[attack_pos].unit_clan == UnitClan.Enemy:
                keys_to_remove.append(attack_pos)
        for key in keys_to_remove:
            del enemy_attack_grid[key]

        # defense
        keys_to_remove = []
        for attack_pos, damage in enemy_attack_grid.items():
            if attack_pos in ally_defense_grid:
                damage -= ally_defense_grid[attack_pos]
                enemy_attack_grid[attack_pos] = damage
            if damage < 0:
                keys_to_remove.append(attack_pos)
        for key in keys_to_remove:
            del enemy_attack_grid[key]

        # coop: if the unit under attack is surrounded by 2 opponent units, damage plus 1; if 3 or more, damage plus 2
        for attack_pos, damage in enemy_attack_grid.items():
            unit_under_attack = self.units.get(attack_pos)
            surrounding_opponent_count = self.count_surrounding_opponents(unit_under_attack)
            if surrounding_opponent_count == 2:
                damage += 1
                enemy_attack_grid[attack_pos] = damage
            elif surrounding_opponent_count >= 3:
                damage += 2
                enemy_attack_grid[attack_pos] = damage

        return enemy_attack_grid

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
