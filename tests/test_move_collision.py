"""
Unit tests for the move_collision module.
"""

import unittest
from grid_position import GridPosition
from Unit.Unit import Unit
from enums import UnitClan
from level_grid import LevelGrid
from move_collision import (
    resolve_boundary_collision,
    resolve_occupied_cell_collision,
    resolve_opposite_clan_collision,
    resolve_multiple_units_collision,
    resolve_movement_collision
)


class TestMoveCollision(unittest.TestCase):
    def test_resolve_boundary_collision(self):
        placeholder_unit = Unit("placeholder", UnitClan.Ally, GridPosition(2, 2), GridPosition(0, 1))
        row_num = 5
        col_num = 5

        movement_requests = {
            # Valid
            GridPosition(1, 1): [placeholder_unit],
            # Out of bounds
            GridPosition(10, 10): [placeholder_unit]
        }
        
        result = resolve_boundary_collision(movement_requests, row_num, col_num)
        assert result == {
            GridPosition(1, 1): [placeholder_unit]
        }
    
    def test_resolve_occupied_cell_collision(self):
        # Create a level grid
        level_grid = LevelGrid(row_num=5, col_num=5)
        
        # Create units
        unit1 = Unit("unit1", UnitClan.Ally, GridPosition(1, 1), GridPosition(0, 1))
        unit1.is_marching = True
        unit2 = Unit("unit2", UnitClan.Ally, GridPosition(1, 2), GridPosition(0, 1))
        unit2.is_marching = False
        
        # Add units to the grid
        level_grid.move(unit1, unit1.loc)
        level_grid.move(unit2, unit2.loc)

        # Create a movement request to the occupied cell
        occupied_pos = unit2.loc
        empty_pos = GridPosition(3, 3)
        
        movement_requests = {
            occupied_pos: [unit1],
            empty_pos: [unit1]
        }
        
        # Test occupied cell collision resolution
        result = resolve_occupied_cell_collision(movement_requests, level_grid.units)
        assert result == {
            empty_pos: [unit1]
        }
    
    def test_resolve_multiple_units_collision(self):
        # Create units with different priorities
        unit1 = Unit("unit1", UnitClan.Ally, GridPosition(0, 0), GridPosition(0, 1))
        unit2 = Unit("unit2", UnitClan.Ally, GridPosition(0, 0), GridPosition(0, 1))
        unit3 = Unit("unit3", UnitClan.Ally, GridPosition(0, 0), GridPosition(0, 1))
        
        unit1.set_priority(2)
        unit2.set_priority(3)
        unit3.set_priority(3)
        
        # Create a movement request with multiple units to the same destination
        destination = GridPosition(1, 1)
        
        movement_requests = {
            destination: [unit1, unit2, unit3]
        }
        
        # Test multiple units collision resolution
        result = resolve_multiple_units_collision(movement_requests)
        
        assert len(result) == 1
        assert list(result.values())[0] == unit2 or list(result.values())[0] == unit3
    
    def test_resolve_opposite_clan_collision(self):
        # Create a level grid
        level_grid = LevelGrid(row_num=5, col_num=5)
        
        # Create units
        ally_unit = Unit("ally", UnitClan.Ally, GridPosition(1, 1), GridPosition(0, 1))
        enemy_unit = Unit("enemy", UnitClan.Enemy, GridPosition(2, 2), GridPosition(0, -1))
        
        # Add units to the grid
        level_grid.move(ally_unit, ally_unit.loc)
        level_grid.move(enemy_unit, enemy_unit.loc)
        
        # Set both units as marching
        ally_unit.is_marching = True
        enemy_unit.is_marching = True
        
        # Convert to single unit format
        movement_requests_single = {
            ally_unit.loc: enemy_unit,
            enemy_unit.loc: ally_unit
        }
        
        # Test opposite clan collision resolution
        result = resolve_opposite_clan_collision(movement_requests_single, level_grid.units)
        
        # Both positions should be removed due to opposite clan collision
        self.assertNotIn(ally_unit.loc, result)
        self.assertNotIn(enemy_unit.loc, result)
    
    def test_resolve_movement_collision(self):
        # Create a level grid
        level_grid = LevelGrid(row_num=5, col_num=5)
        
        # Create units
        unit1 = Unit("unit1", UnitClan.Ally, GridPosition(1, 1), GridPosition(0, 1))
        unit2 = Unit("unit2", UnitClan.Ally, GridPosition(1, 2), GridPosition(0, 1))
        unit3 = Unit("unit3", UnitClan.Enemy, GridPosition(1, 3), GridPosition(0, 1))
        
        # Set priorities
        unit1.set_priority(1)
        unit2.set_priority(2)
        unit3.set_priority(3)
        
        # Add units to the grid
        level_grid.move(unit1, unit1.loc)
        level_grid.move(unit2, unit2.loc)
        level_grid.move(unit3, unit3.loc)
        
        # Create a movement request with various collision scenarios
        valid_pos = GridPosition(2, 2)
        out_of_bounds_pos = GridPosition(10, 10)
        occupied_pos = unit1.loc  # Position occupied by a non-marching unit
        
        # Set unit1 as non-marching
        unit1.is_marching = False
        
        movement_requests = {
            valid_pos: [unit2, unit3],  # Multiple units to same destination
            out_of_bounds_pos: [unit2],  # Out of bounds
            occupied_pos: [unit3]  # Occupied cell
        }
        
        # Test the complete movement collision resolution
        result = resolve_movement_collision(movement_requests, level_grid.units, 5, 5)
        
        # Only the valid position with the highest priority unit should remain
        self.assertIn(valid_pos, result)
        self.assertEqual(result[valid_pos], unit3)  # unit3 has highest priority
        self.assertNotIn(out_of_bounds_pos, result)
        self.assertNotIn(occupied_pos, result)


if __name__ == '__main__':
    unittest.main() 