def display_solution(grid, placed_blocks):
    """
    Display the solved puzzle grid and placed blocks in a user-friendly format.
    """
    # Input validation
    assert isinstance(grid, list), "Grid must be a 2D list"
    assert (isinstance(placed_blocks, list) and 
           all(len(item) == 2 for item in placed_blocks)), \
           "Placed blocks must be a list of (position, block_type) tuples"
    
    print("\n=== SOLUTION ===")
    
    # Display grid (compressed view)
    print("Final Grid Layout:")
    for y in range(1, len(grid), 2):
        row = []
        for x in range(1, len(grid[y]), 2):
            cell = grid[y][x]
            row.append(str(cell) if cell != 0 else '.')
        print(' '.join(row))
    
    # Display placed blocks with numbering
    print("\nPlaced Blocks:")
    for i, (pos, block_type) in enumerate(placed_blocks, 1):
        x, y = pos
        print(f"{i}. Block {block_type} at ({x//2 + 1}, {y//2 + 1})")
    
    # Calculate and display coverage statistics
    total_blocks = len(placed_blocks)
    unique_blocks = len({block_type for _, block_type in placed_blocks})
    print(f"\nSummary: Placed {total_blocks} blocks ({unique_blocks} unique types)")

def place_block(block_type, position, grid):
    """
    Place a block on the game grid at the specified position.
    """
    valid_blocks = {'A', 'B', 'C', 'o', 'x'}
    if block_type not in valid_blocks:
        raise ValueError(f"Invalid block type. Must be one of: {valid_blocks}")
    
    if not (isinstance(position, tuple) and len(position) == 2):
        raise ValueError("Position must be a (x,y) tuple")
    
    x, y = position
    
    # Check grid bounds
    if not (0 <= y < len(grid) and 0 <= x < len(grid[0])):
        raise ValueError(f"Position {position} is outside grid boundaries")
    
    # Place the block
    grid[y][x] = block_type
    
    return grid

def get_available_positions(grid):
    available_positions = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'o':
                available_positions.append((x, y))
    return available_positions