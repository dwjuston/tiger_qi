"""
Enemy module for managing enemy units and their behaviors.
"""

import random
from typing import List, Dict, Optional, Tuple
from grid_position import GridPosition
from Unit.Unit import Unit
from enums import UnitClan
from level_grid import LevelGrid

class EnemyPatrolConfig:
    """
    Configuration class for enemy patrol behavior.
    """


class Enemy:
    """
    Enemy class to manage all enemy units and their behaviors.
    """

    south = GridPosition(0, 1)
    north = GridPosition(0, -1)
    east = GridPosition(1, 0)
    west = GridPosition(-1, 0)
    
    def __init__(self, level_grid: LevelGrid):
        """
        Initialize the Enemy manager.
        
        Args:
            level_grid: The level grid where units are placed
            grid_rows: Number of rows in the grid
            grid_cols: Number of columns in the grid
        """
        self.level_grid = level_grid
        self.enemy_units: List[Unit]
        self.patrol_states: Dict[str, Dict] = {}  # Maps unit UUID to patrol state
        
    def spawn_enemy(self, unit_type: str = "Enemy", count: int = 1) -> List[Unit]:
        spawned_units = []
        
        for _ in range(count):
            # Choose a random edge (0: top, 1: right, 2: bottom, 3: left)
            edge = random.randint(0, 3)
            
            if edge == 0:  # Top edge
                x = random.randint(0, self.grid_cols - 1)
                y = self.grid_rows - 1
                face = self.patrol_directions['S']  # Face south
            elif edge == 1:  # Right edge
                x = self.grid_cols - 1
                y = random.randint(0, self.grid_rows - 1)
                face = self.patrol_directions['W']  # Face west
            elif edge == 2:  # Bottom edge
                x = random.randint(0, self.grid_cols - 1)
                y = 0
                face = self.patrol_directions['N']  # Face north
            else:  # Left edge
                x = 0
                y = random.randint(0, self.grid_rows - 1)
                face = self.patrol_directions['E']  # Face east
                
            pos = GridPosition(x, y)
            
            # Create the unit
            unit = Unit(unit_type, UnitClan.Enemy, pos, face)
            unit.is_marching = True
            
            # Add to level grid
            self.level_grid.units[pos] = unit
            self.enemy_units[pos] = unit
            
            # Initialize patrol state
            self.patrol_states[unit.uuid] = {
                'direction': face,
                'patrol_mode': 'forward',  # 'forward' or 'backward'
                'patrol_counter': 0,
                'patrol_threshold': random.randint(3, 7)  # Random patrol distance
            }
            
            spawned_units.append(unit)
            
        return spawned_units
    
    def spawn_enemy_preset(self, preset: List[Dict]) -> List[Unit]:
        """
        Spawn enemy units according to a preset configuration.
        
        Args:
            preset: List of dictionaries with unit configurations
                   Each dict should have: 'x', 'y', 'face', 'unit_type'
                   
        Returns:
            List of spawned units
        """
        spawned_units = []
        
        for unit_config in preset:
            x = unit_config.get('x', 0)
            y = unit_config.get('y', 0)
            face_direction = unit_config.get('face', 'N')
            unit_type = unit_config.get('unit_type', 'Enemy')
            
            pos = GridPosition(x, y)
            face = self.patrol_directions.get(face_direction, self.patrol_directions['N'])
            
            # Create the unit
            unit = Unit(unit_type, UnitClan.Enemy, pos, face)
            unit.is_marching = True
            
            # Add to level grid
            self.level_grid.units[pos] = unit
            self.enemy_units[pos] = unit
            
            # Initialize patrol state
            self.patrol_states[unit.uuid] = {
                'direction': face,
                'patrol_mode': 'forward',
                'patrol_counter': 0,
                'patrol_threshold': random.randint(3, 7)
            }
            
            spawned_units.append(unit)
            
        return spawned_units
    
    def update_patrol(self) -> None:
        """
        Update all enemy units' patrol behavior.
        """
        for unit in list(self.enemy_units.values()):
            if unit.uuid not in self.patrol_states:
                continue
                
            patrol_state = self.patrol_states[unit.uuid]
            
            # Check if unit has reached patrol threshold
            if patrol_state['patrol_counter'] >= patrol_state['patrol_threshold']:
                # Change patrol mode
                if patrol_state['patrol_mode'] == 'forward':
                    patrol_state['patrol_mode'] = 'backward'
                    # Reverse direction
                    patrol_state['direction'] = GridPosition(
                        -patrol_state['direction'].x,
                        -patrol_state['direction'].y
                    )
                    unit.face = patrol_state['direction']
                else:
                    patrol_state['patrol_mode'] = 'forward'
                    # Reverse direction again
                    patrol_state['direction'] = GridPosition(
                        -patrol_state['direction'].x,
                        -patrol_state['direction'].y
                    )
                    unit.face = patrol_state['direction']
                
                patrol_state['patrol_counter'] = 0
                
            # Update marching state based on patrol rules
            # For example, march every 3 turns
            if random.random() < 0.3:  # 30% chance to change marching state
                unit.is_marching = not unit.is_marching
                
            # Increment patrol counter
            patrol_state['patrol_counter'] += 1
            
    def update_face_direction(self) -> None:
        """
        Update face direction of enemy units based on certain rules.
        """
        for unit in self.enemy_units.values():
            if unit.uuid not in self.patrol_states:
                continue
                
            # Example rule: 10% chance to change direction randomly
            if random.random() < 0.1:
                # Choose a random direction
                direction_key = random.choice(list(self.patrol_directions.keys()))
                new_direction = self.patrol_directions[direction_key]
                
                # Update unit's face direction
                unit.face = new_direction
                
                # Update patrol state
                self.patrol_states[unit.uuid]['direction'] = new_direction
                
    def update(self) -> None:
        """
        Update all enemy behaviors.
        """
        self.update_patrol()
        self.update_face_direction()
        
    def get_all_units(self) -> Dict[GridPosition, Unit]:
        """
        Get all enemy units.
        
        Returns:
            Dictionary of positions to units
        """
        return self.enemy_units 