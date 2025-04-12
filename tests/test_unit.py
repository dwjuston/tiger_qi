import unittest
from Unit import Unit
from grid_position import GridPosition
from enums import UnitClan

class TestUnit(unittest.TestCase):
    def test_initialization(self):
        """Test that a unit is created with the correct properties"""
        # Create a unit with specific properties
        name = "TestUnit"
        clan = UnitClan.Ally
        loc = GridPosition(2, 3)
        face = GridPosition(0, 1)  # Facing north
        
        unit = Unit(name, clan, loc, face)
        
        # Check basic properties
        self.assertEqual(unit.name, name)
        self.assertEqual(unit.unit_clan, clan)
        self.assertEqual(unit.loc, loc)
        self.assertEqual(unit.face, face)
        
        # Check default values
        self.assertEqual(unit.health, 5)
        self.assertEqual(unit.attack, 1)
        self.assertTrue(unit.is_marching)
        self.assertEqual(unit.priority, 1)
        
        # Check UUID format
        self.assertEqual(len(unit.uuid), 8)
        
        # Check default attack range
        expected_range = [
            GridPosition(-1, 0),  # Left
            GridPosition(1, 0),   # Right
            GridPosition(0, 1)    # Front
        ]
        self.assertEqual(len(unit.relative_attack_range), 3)
        for i, pos in enumerate(unit.relative_attack_range):
            self.assertEqual(pos, expected_range[i])
    
    def test_attack_range(self):
        """Test that the attack range is correctly calculated based on facing direction"""
        # Create a unit facing north
        unit_north = Unit("NorthUnit", UnitClan.Ally, GridPosition(2, 3), GridPosition(0, 1))
        
        # Attack range should be relative to the unit's position and facing direction
        attack_range = unit_north.attack_range
        
        # For a unit facing north, the attack positions should be:
        # Left: (1, 3)
        # Right: (3, 3)
        # Front: (2, 4)
        expected_positions = [
            GridPosition(1, 3),  # Left
            GridPosition(3, 3),  # Right
            GridPosition(2, 4)   # Front
        ]
        
        self.assertEqual(len(attack_range), 3)
        for i, pos in enumerate(attack_range):
            self.assertEqual(pos, expected_positions[i])
        
        # Test with a unit facing east
        unit_east = Unit("EastUnit", UnitClan.Ally, GridPosition(2, 3), GridPosition(1, 0))
        
        # For a unit facing east, the attack positions should be:
        # Left: (2, 4)
        # Right: (2, 2)
        # Front: (3, 3)
        attack_range_east = unit_east.attack_range
        expected_positions_east = [
            GridPosition(2, 4),  # Left (was front)
            GridPosition(2, 2),  # Right (was back)
            GridPosition(3, 3)   # Front (was right)
        ]
        
        self.assertEqual(len(attack_range_east), 3)
        for i, pos in enumerate(attack_range_east):
            self.assertEqual(pos, expected_positions_east[i])
    
    def test_move_destination(self):
        """Test that the move destination is correctly calculated based on facing direction"""
        # Create a unit facing north
        unit_north = Unit("NorthUnit", UnitClan.Ally, GridPosition(2, 3), GridPosition(0, 1))
        
        # Move destination should be one step in the facing direction
        destination = unit_north.move_destination
        expected_destination = GridPosition(2, 4)  # One step north
        
        self.assertEqual(destination, expected_destination)
        
        # Test with a unit facing east
        unit_east = Unit("EastUnit", UnitClan.Ally, GridPosition(2, 3), GridPosition(1, 0))
        
        # Move destination should be one step east
        destination_east = unit_east.move_destination
        expected_destination_east = GridPosition(3, 3)  # One step east
        
        self.assertEqual(destination_east, expected_destination_east)
        
        # Test with is_marching set to False
        unit_north.is_marching = False
        self.assertIsNone(unit_north.move_destination)
        
        # Test with is_marching set back to True
        unit_north.is_marching = True
        self.assertEqual(unit_north.move_destination, expected_destination)

if __name__ == '__main__':
    unittest.main() 