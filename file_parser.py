from lazor import Lazor


def load_puzzle(file_path):
    """
    Load and parse a puzzle file in .bff format to extract all game components.

    Args:
        file_path (str): Path to the .bff puzzle file

    Returns:
        tuple: Contains four elements:
            - grid (2D list): Expanded game grid with block positions
            - available_blocks (dict): Count of available blocks by type (A/B/C)
            - lazors (list): Lazor objects with start positions and directions
            - target_points (list): (x,y) coordinates of target points to hit

    Raises:
        AssertionError: If the puzzle has no blocks, targets or lazors
    """
    # Initialize data containers for all puzzle components
    grid = []                # Will store the grid layout
    # Tracks available blocks by type
    available_blocks = {'A': 0, 'B': 0, 'C': 0}
    lazor_data = []          # Stores raw lazor data before creating objects
    target_points = []       # Stores target point coordinates

    # Read and preprocess the puzzle file
    with open(file_path, 'r') as file:
        # Filter out comments (lines starting with #) and empty lines
        lines = [line.strip() for line in file
                 if line.strip() and not line.strip().startswith('#')]

    # Process each line of the file based on its content
    grid_mode = False  # Flag to track when we're processing grid lines
    for line in lines:
        # Handle grid section markers
        if line == "GRID START":
            grid_mode = True
            continue
        elif line == "GRID STOP":
            grid_mode = False
            continue

        if grid_mode:
            # Current line is part of the grid - split into individual cells
            grid.append(line.split())
        elif line[0] in {'A', 'B', 'C'}:
            # Current line specifies block counts (e.g. "A 3")
            block_type, count = line.split()
            available_blocks[block_type] = int(count)
        elif line.startswith('L'):
            # Current line defines a lazor (e.g. "L 2 3 1 0")
            # Format: L x y dx dy (position and direction vector)
            _, x, y, vx, vy = line.split()
            lazor_data.append(((int(x), int(y)), (int(vx), int(vy))))
        elif line.startswith('P'):
            # Current line defines a target point (e.g. "P 4 5")
            _, x, y = line.split()
            target_points.append((int(x), int(y)))

    # Convert the grid to expanded format if needed
    if grid:
        # Calculate dimensions for expanded grid (2n+1 in each dimension)
        # This creates space between blocks for lazor paths
        expanded_height = len(grid) * 2 + 1
        expanded_width = len(grid[0]) * 2 + 1 if grid else 0

        # Initialize empty expanded grid filled with zeros (empty spaces)
        expanded_grid = [[0 for _ in range(expanded_width)]
                         for _ in range(expanded_height)]

        # Place blocks from original grid into expanded grid
        # Note: Original grid positions are mapped to odd indices in expanded
        # grid
        for y, row in enumerate(grid, start=1):
            for x, block_char in enumerate(row, start=1):
                if block_char in {'A', 'B', 'C', 'o', 'x'}:
                    # Convert to 1-based coordinates in expanded grid
                    expanded_grid[y * 2 - 1][x * 2 - 1] = block_char
        grid = expanded_grid

    # Create Lazor objects from the parsed lazor data
    lazors = [Lazor(pos, dir_vec) for pos, dir_vec in lazor_data]

    # Validate that the puzzle has all required components
    total_blocks = sum(available_blocks.values())
    assert total_blocks > 0, "Puzzle must contain at least one block"
    assert target_points, "Puzzle must specify at least one target point"
    assert lazors, "Puzzle must specify at least one lazor"

    return grid, available_blocks, lazors, target_points
