# Grid Game

A Pygame-based tactical grid game featuring unit movement, combat, and collision resolution.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `grid_game.py`: Main game loop and initialization
- `game_state.py`: Central game state management and rendering
- `move_collision.py`: Collision resolution system for unit movements
- `level_grid.py`: Grid management and cell operations
- `Unit/`: Unit classes and behaviors
- `colors.py`: Game color definitions
- `grid_position.py`: Grid position utilities
- `enums.py`: Game enumerations
- `tests/`: Unit tests

## Features

- 15x15 tactical grid
- Unit management system
  - Multiple unit types (including SpearUnit)
  - Unit grouping and selection
  - Unit movement and facing direction
  - Marching formation control
- Collision resolution system
  - Boundary collision detection
  - Occupied cell handling
  - Multiple units collision resolution
  - Opposite clan collision handling
- Combat system
- Cell painting and text display
- Color management system

## How to Play

1. Run the game:
```bash
python grid_game.py
```

2. Controls:
- Select units by clicking
- Move selected units with arrow keys
- Press 'M' to toggle marching formation
- Press 'O' to paint cells
- Press 'P' to set cell text
- Close the window to exit the game

## Development

The project uses a modular architecture with clear separation of concerns:
- Game state management
- Unit behavior and movement
- Collision detection and resolution
- Grid and cell management
- Rendering and display 