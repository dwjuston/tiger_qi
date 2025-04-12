"""
Game state module to store global variables and state.
This module serves as a central location for game state management.
"""

import pygame
import random
from grid_position import GridPosition
from level_grid import LevelGrid
from Unit import Unit, SpearUnit
from enums import UnitClan
from colors import GameColor, combine_colors

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_M = 15  # Number of rows
GRID_N = 15  # Number of columns
WINDOW_WIDTH = GRID_N * CELL_SIZE
WINDOW_HEIGHT = GRID_M * CELL_SIZE

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid Game")

# Initialize grid data
grid_colors = [[GameColor.WHITE.value for _ in range(GRID_N)] for _ in range(GRID_M)]
grid_texts = [['' for _ in range(GRID_N)] for _ in range(GRID_M)]
grid_text_sizes = [[24 for _ in range(GRID_N)] for _ in range(GRID_M)]  # Default font size

# Fonts
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 36)  # Larger font for selected units

# Available colors for painting
AVAILABLE_COLORS = [
    GameColor.RED.value,
    GameColor.ORANGE.value,
    GameColor.YELLOW.value,
    GameColor.GREEN.value,
    GameColor.BLUE.value,
    GameColor.PURPLE.value,
    GameColor.LIGHT_BLUE.value
]

# Counter for incremental positions
current_position = 0

# Flag to toggle between board states
show_board = False

# Selected units (list to store multiple units)
selected_units = []

# Level grid (singleton)
level_grid = LevelGrid(GRID_M, GRID_N)

# Game units
ally1 = SpearUnit("A", UnitClan.Ally, GridPosition(1, 1), GridPosition(0, 1))  # Facing north
ally2 = Unit("B", UnitClan.Ally, GridPosition(4, 4), GridPosition(1, 0))  # Facing east
enemy1 = Unit("C", UnitClan.Enemy, GridPosition(1, 4), GridPosition(0, -1))  # Facing south
enemy2 = Unit("D", UnitClan.Enemy, GridPosition(4, 1), GridPosition(-1, 0))  # Facing west

# Initialize game units
def initialize_game():
    """Initialize the game state with units and their positions"""
    global ally1, ally2, enemy1, enemy2, selected_units
    
    # Set group IDs
    ally1.set_group_id(1)
    ally2.set_group_id(1)
    enemy1.set_group_id(2)
    enemy2.set_group_id(2)
    
    # Place units on the grid
    level_grid.move(ally1, GridPosition(1, 1))
    level_grid.move(ally2, GridPosition(4, 4))
    level_grid.move(enemy1, GridPosition(1, 4))
    level_grid.move(enemy2, GridPosition(4, 1))
    
    # Set the selected units to ally1 and ally2 initially (group 1)
    select_units_by_group(1)

def select_units_by_group(group_id: int):
    """Select all units that belong to the specified group"""
    global selected_units
    
    # Clear the current selection
    selected_units = []
    
    # Reset all text sizes to default
    for i in range(GRID_M):
        for j in range(GRID_N):
            grid_text_sizes[i][j] = 24
    
    # Find all units with the specified group_id
    for unit in level_grid.units.values():
        if unit.group_id == group_id:
            selected_units.append(unit)
            
            # Set larger font size for selected units
            python_pos = unit.loc.to_python(GRID_M)
            row, col = python_pos
            if 0 <= row < GRID_M and 0 <= col < GRID_N:
                grid_text_sizes[row][col] = 36
    
    # If no units found, print a message
    if not selected_units:
        print(f"No units found in group {group_id}")

def update_selected_units_face(direction):
    """Update the face direction of all selected units"""
    global selected_units
    
    if not selected_units:
        return
    
    # Update the face direction based on the input
    if direction == 'W':  # North
        new_face = GridPosition(0, 1)
    elif direction == 'S':  # South
        new_face = GridPosition(0, -1)
    elif direction == 'A':  # West
        new_face = GridPosition(-1, 0)
    elif direction == 'D':  # East
        new_face = GridPosition(1, 0)
    else:
        return
    
    # Update all selected units
    for unit in selected_units:
        unit.face = new_face

def toggle_selected_units_marching():
    """Toggle the marching state of all selected units"""
    global selected_units
    
    if not selected_units:
        return
    
    # Toggle marching state for all selected units
    for unit in selected_units:
        unit.is_marching = not unit.is_marching

def process_movement_requests():
    """Process movement requests from the level grid"""
    # Get movement requests
    movement_requests = level_grid.movement_request
    
    # Process each movement request
    for destination, unit_list in movement_requests.items():
        # Check if the destination is within the grid bounds
        python_pos = destination.to_python(GRID_M)
        row, col = python_pos
        
        if 0 <= row < GRID_M and 0 <= col < GRID_N:
            # Check if there's already a unit at the destination
            if destination in level_grid.units:
                # Skip this movement request
                continue
            
            # Move the unit to the destination
            for unit in unit_list:
                level_grid.move(unit, destination)
                print(f"Unit {unit.name} moved to {destination}")

def paint_cell(grid_pos: GridPosition):
    """Paint the cell at the given grid position with a random color, overlaying the current color"""
    global current_position
    
    # Convert grid position to Python coordinates
    python_pos = grid_pos.to_python(GRID_M)
    row, col = python_pos
    
    if 0 <= row < GRID_M and 0 <= col < GRID_N:
        # Get the current color of the cell
        current_color = grid_colors[row][col]
        
        # Pick a random color from the available colors
        new_color = random.choice(AVAILABLE_COLORS)
        
        # Combine the current color with the new color (50% new color, 50% current color)
        # This creates an overlay effect
        blended_color = combine_colors(new_color, current_color, 0.5)
        
        # Update the cell color
        grid_colors[row][col] = blended_color

def set_cell_text(grid_pos: GridPosition, text: str, font_size: int = 24):
    """Set the text of the cell at the given grid position with specified font size"""
    # Convert grid position to Python coordinates
    python_pos = grid_pos.to_python(GRID_M)
    row, col = python_pos
    
    if 0 <= row < GRID_M and 0 <= col < GRID_N:
        grid_texts[row][col] = str(text)
        grid_text_sizes[row][col] = font_size

def paint_board():
    """Paint the board based on the level_grid's units and their attack ranges"""
    global grid_colors, grid_texts, grid_text_sizes
    
    # Clear the grid
    for i in range(GRID_M):
        for j in range(GRID_N):
            grid_colors[i][j] = GameColor.WHITE.value
            grid_texts[i][j] = ''
            grid_text_sizes[i][j] = 24  # Reset font sizes
    
    # First, paint the attack ranges
    # Get attack grids
    ally_attack_grid = level_grid.ally_attack_grid
    enemy_attack_grid = level_grid.enemy_attack_grid
    
    # Paint ally attack positions (light blue)
    for grid_position in ally_attack_grid:
        python_pos = grid_position.to_python(GRID_M)
        row, col = python_pos
        
        if 0 <= row < GRID_M and 0 <= col < GRID_N:
            # Only paint if there's no unit at this position
            if grid_position not in level_grid.units:
                # Get the current color (should be white at this point)
                current_color = grid_colors[row][col]
                
                # Overlay light blue (70% light blue, 30% current color)
                blended_color = combine_colors(GameColor.LIGHT_BLUE.value, current_color, 0.7)
                
                # Update the cell color
                grid_colors[row][col] = blended_color
    
    # Paint enemy attack positions (orange)
    for grid_position in enemy_attack_grid:
        python_pos = grid_position.to_python(GRID_M)
        row, col = python_pos
        
        if 0 <= row < GRID_M and 0 <= col < GRID_N:
            # Only paint if there's no unit at this position
            if grid_position not in level_grid.units:
                # Get the current color
                current_color = grid_colors[row][col]
                
                # If this position is already painted with ally attack color, blend with orange
                if current_color != GameColor.WHITE.value:
                    # Overlay orange (70% orange, 30% current color)
                    blended_color = combine_colors(GameColor.ORANGE.value, current_color, 0.7)
                else:
                    # Just use orange
                    blended_color = GameColor.ORANGE.value
                
                # Update the cell color
                grid_colors[row][col] = blended_color
    
    # Then, paint the units (blending with any attack range colors)
    for grid_position, unit in level_grid.units.items():
        # Convert grid position to Python coordinates
        python_pos = grid_position.to_python(GRID_M)
        row, col = python_pos
        
        if 0 <= row < GRID_M and 0 <= col < GRID_N:
            # Get the current color (might be an attack range color)
            current_color = grid_colors[row][col]
            
            # Set color based on unit clan and marching state
            if unit.unit_clan == UnitClan.Ally and unit.is_marching == True:
                # Blend blue with current color (70% blue, 30% current color)
                blended_color = combine_colors(GameColor.BLUE.value, current_color, 0.7)
            elif unit.unit_clan == UnitClan.Ally and unit.is_marching == False:
                # Blend green with current color (70% green, 30% current color)
                blended_color = combine_colors(GameColor.LIGHT_BLUE.value, current_color, 0.7)
            elif unit.unit_clan == UnitClan.Enemy and unit.is_marching == True:
                # Blend purple with current color (70% purple, 30% current color)
                blended_color = combine_colors(GameColor.PURPLE.value, current_color, 0.7)
            else:  # Enemy not marching
                # Blend red with current color (70% red, 30% current color)
                blended_color = combine_colors(GameColor.ORANGE.value, current_color, 0.7)
            
            # Update the cell color
            grid_colors[row][col] = blended_color
            
            # Set text to unit name and health
            # Check if this unit is selected
            font_size = 36 if unit in selected_units else 24
            set_cell_text(grid_position, f"{unit.name}: {unit.health}", font_size)

def draw_grid():
    """Draw the grid with colors and text"""
    screen.fill(GameColor.WHITE.value)
    
    # Draw cells
    for i in range(GRID_M):
        for j in range(GRID_N):
            # Draw cell background
            pygame.draw.rect(screen, grid_colors[i][j],
                           (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Draw cell border
            pygame.draw.rect(screen, GameColor.BLACK.value,
                           (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            
            # Draw cell text with appropriate font size
            if grid_texts[i][j]:
                # Choose font based on size
                if grid_text_sizes[i][j] == 36:
                    text_surface = large_font.render(grid_texts[i][j], True, GameColor.BLACK.value)
                else:
                    text_surface = font.render(grid_texts[i][j], True, GameColor.BLACK.value)
                
                text_rect = text_surface.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2,
                                                        i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

def process_attacks():
    """Process attack requests from both ally and enemy units"""
    # Get attack grids
    ally_attack_grid = level_grid.ally_attack_grid
    enemy_attack_grid = level_grid.enemy_attack_grid
    
    # Process ally attacks
    for position, attack_count in ally_attack_grid.items():
        if position in level_grid.units:
            unit = level_grid.units[position]
            if unit.unit_clan == UnitClan.Enemy:
                # Apply damage based on attack count
                level_grid.attack(position, attack_count)
                print(f"Ally units attacked {unit.name} for {attack_count} damage")
    
    # Process enemy attacks
    for position, attack_count in enemy_attack_grid.items():
        if position in level_grid.units:
            unit = level_grid.units[position]
            if unit.unit_clan == UnitClan.Ally:
                # Apply damage based on attack count
                level_grid.attack(position, attack_count)
                print(f"Enemy units attacked {unit.name} for {attack_count} damage") 