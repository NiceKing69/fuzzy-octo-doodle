# Lazor Puzzle Solver

A Python implementation to solve Lazor puzzle games by simulating laser paths and strategically placing blocks to hit all target points.

## Files Overview

### Core Modules:

1. **main.py**  
   Entry point that orchestrates the puzzle solving process. Handles user input and displays results.

2. **lazor.py**  
   Contains the `Lazor` class that simulates laser behavior:
   - Path calculation through the grid
   - Interactions with different block types (reflect, stop, refract)
   - Target point verification

3. **grid_utils.py**  
   Grid manipulation and display functions:
   - Block placement and position validation
   - Solution visualization
   - Available position detection

4. **solver.py**  
   Implements two solving algorithms:
   - `smart_solution`: Prioritizes blocks in laser paths
   - `brute_force_solution`: Tries random valid placements

5. **file_parser.py**  
   Handles puzzle file (.bff) loading and parsing:
   - Grid construction
   - Block inventory management
   - Laser and target point extraction

## How It Works

1. Reads a puzzle file in .bff format
2. Expands the grid to allow for laser path simulation
3. Attempts solutions
4. Displays the solution grid and block placements

## Usage

1. Run `main.py`
2. Enter your .bff puzzle filename when prompted
3. View the solution (or failure message)

Example:
```bash
python main.py