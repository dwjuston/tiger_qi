import unittest
from grid_position import GridPosition

class TestGridPosition(unittest.TestCase):
    def test_creation(self):
        """Test creation of GridPosition objects"""
        pos = GridPosition(3, 4)
        self.assertEqual(pos.x, 3)
        self.assertEqual(pos.y, 4)
        
        # Test with negative coordinates
        pos_neg = GridPosition(-2, -3)
        self.assertEqual(pos_neg.x, -2)
        self.assertEqual(pos_neg.y, -3)
    
    def test_addition_subtraction(self):
        """Test addition and subtraction of GridPosition objects"""
        pos1 = GridPosition(3, 4)
        pos2 = GridPosition(1, 2)
        
        # Test addition
        result_add = pos1 + pos2
        self.assertEqual(result_add.x, 4)
        self.assertEqual(result_add.y, 6)
        
        # Test subtraction
        result_sub = pos1 - pos2
        self.assertEqual(result_sub.x, 2)
        self.assertEqual(result_sub.y, 2)
        
        # Test with negative results
        pos3 = GridPosition(1, 1)
        result_neg = pos3 - pos1
        self.assertEqual(result_neg.x, -2)
        self.assertEqual(result_neg.y, -3)
    
    def test_adjust_with_face_direction(self):
        """Test adjusting positions based on face direction"""
        # Test case: if you can attack right (1,0) and face south (0,-1)
        # The actual relative cell should be left (-1,0)
        attack_right = GridPosition(1, 0)  # Relative attack position (right)
        face_south = GridPosition(0, -1)   # Unit facing south
        
        # First adjust the attack position based on face direction
        adjusted = attack_right.adjust_with_direction(face_south)
        
        # The adjusted position should be left (-1,0)
        self.assertEqual(adjusted.x, -1)
        self.assertEqual(adjusted.y, 0)
        
        # Additional test cases for other directions
        # Test facing north (0,1) - no change
        face_north = GridPosition(0, 1)
        adjusted_north = attack_right.adjust_with_direction(face_north)
        self.assertEqual(adjusted_north.x, 1)
        self.assertEqual(adjusted_north.y, 0)
        
        # Test facing east (1,0) - rotate 90 degrees clockwise
        face_east = GridPosition(1, 0)
        adjusted_east = attack_right.adjust_with_direction(face_east)
        self.assertEqual(adjusted_east.x, 0)
        self.assertEqual(adjusted_east.y, -1)
        
        # Test facing west (-1,0) - rotate 270 degrees clockwise
        face_west = GridPosition(-1, 0)
        adjusted_west = attack_right.adjust_with_direction(face_west)
        self.assertEqual(adjusted_west.x, 0)
        self.assertEqual(adjusted_west.y, 1)
    
    def test_to_python_coordinate(self):
        """Test conversion from game grid position to Python/pygame coordinates"""
        # Test case: grid position (2,4) in a 5-row grid
        # Should convert to (4,1) in Python coordinates (2nd column, 2nd row from top)
        pos = GridPosition(2, 3) # 3rd column, 4th row from bottom left => 3rd row, 3rd column from top left => (6-3-1, 2)
        max_row = 6
        
        python_pos = pos.to_python(max_row)
        self.assertEqual(python_pos, (2, 2))
        
        # Test bottom-left corner (0,0)
        bottom_left = GridPosition(0, 0) # 1st column, 1st row => 6th row, 1st column => (6-0-1, 0)
        python_bottom_left = bottom_left.to_python(max_row)
        self.assertEqual(python_bottom_left, (5, 0))  # Should be bottom row
        
        # Test top-right corner (4,4)
        top_right = GridPosition(4, 4) # 5th column, 5th row => 2nd row, 5th column => (6-4-1, 4)
        python_top_right = top_right.to_python(max_row)
        self.assertEqual(python_top_right, (1, 4))  # Should be top row

if __name__ == '__main__':
    unittest.main() 