"""
Main game module that handles the game loop and user input.
"""

import pygame
import sys
from grid_position import GridPosition
from game_state import (
    # Constants
    CELL_SIZE, GRID_M, GRID_N, WINDOW_WIDTH, WINDOW_HEIGHT,
    # Game state variables
    # Functions
    initialize_game, select_units_by_group, update_selected_units_face,
    toggle_selected_units_marching, process_movement_requests, paint_cell,
    set_cell_text, paint_board, draw_grid, process_attacks
)
from colors import GameColor

# Initialize Pygame
pygame.init()

# Constants
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 36)  # Larger font for selected units

# Initialize the game
initialize_game()
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                # Process attacks from both ally and enemy units
                process_attacks()
                # Update the board display
                paint_board()
                
            elif event.key == pygame.K_p:
                # Process movement requests
                process_movement_requests()
                paint_board()
                
            elif event.key == pygame.K_SPACE:
                paint_board()
                
            # Handle number keys for selecting units by group
            elif event.key == pygame.K_1:
                select_units_by_group(1)
                paint_board()
            elif event.key == pygame.K_2:
                select_units_by_group(2)
                paint_board()
            elif event.key == pygame.K_3:
                select_units_by_group(3)
                paint_board()
            elif event.key == pygame.K_4:
                select_units_by_group(4)
                paint_board()
            elif event.key == pygame.K_5:
                select_units_by_group(5)
                paint_board()
                
            # Handle WASD keys for updating the selected units' face direction
            elif event.key == pygame.K_w:
                update_selected_units_face('W')
                paint_board()
            elif event.key == pygame.K_a:
                update_selected_units_face('A')
                paint_board()
            elif event.key == pygame.K_s:
                update_selected_units_face('S')
                paint_board()
            elif event.key == pygame.K_d:
                update_selected_units_face('D')
                paint_board()
                
            # Handle F key for toggling the selected units' marching state
            elif event.key == pygame.K_f:
                toggle_selected_units_marching()
                paint_board()
        
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()