import numpy as np
from lazor import is_puzzle_solved
from grid_utils import place_block, get_available_positions
from file_parser import load_puzzle

def smart_solution(file_path):
    """
    Attempt to solve the puzzle using a smart approach that prioritizes placing blocks
    in positions that are crossed by lazor paths first.
    
    Args:
        file_path (str): Path to the puzzle file
        
    Returns:
        tuple: (grid, placed_blocks) if solution found, False otherwise
    """
    # Load puzzle data from file
    grid, blocks, lazors, targets = load_puzzle(file_path)
    # Calculate total number of blocks to place
    total_blocks = sum(blocks[block_type] for block_type in blocks)
    # Initialize tracking of attempted positions for backtracking
    attempts = [{'A': [], 'B': [], 'C': []} for _ in range(total_blocks)]
    placed_blocks = []

    # Main solving loop - continues until all blocks are placed or options exhausted
    while len(placed_blocks) <= total_blocks:
        # Get all blocks positions crossed by any lazor's path
        crossed_blocks = [block for lazor in lazors 
                         for block in lazor.get_crossed_blocks_and_path(grid)[0]]

        # Determine possible block types we can place (A and C get priority)
        possible_types = []
        for block_type in ['A', 'C']:
            for block_pos in crossed_blocks:
                # Check if we have blocks of this type left and position not tried before
                if blocks[block_type] > 0 and block_pos not in attempts[len(placed_blocks)][block_type]:
                    possible_types.append(block_type)

        # Special handling for B blocks (can be placed anywhere)
        if blocks['B'] > 0:
            b_positions = []
            available_positions = get_available_positions(grid)
            for pos in available_positions:
                if pos not in attempts[len(placed_blocks)]['B']:
                    b_positions.append(pos)
            if b_positions:
                possible_types.append('B')

        # If we have possible moves to make
        if possible_types:
            # Randomly select a block type from available options
            chosen_type = np.random.choice(possible_types)
            
            # Handle position selection differently for B vs A/C blocks
            if chosen_type != 'B':
                # For A/C blocks, only consider positions crossed by lazors
                valid_positions = [pos for pos in crossed_blocks
                                 if pos not in attempts[len(placed_blocks)][chosen_type]]
                chosen_position = valid_positions[np.random.randint(0, len(valid_positions))]
            else:
                # For B blocks, choose from any available position
                chosen_position = b_positions[np.random.randint(0, len(b_positions))]
            
            # Place the selected block
            grid = place_block(chosen_type, chosen_position, grid)
            # Record this attempt for backtracking purposes
            attempts[len(placed_blocks)][chosen_type].append(chosen_position)
            placed_blocks.append((chosen_position, chosen_type))
            blocks[chosen_type] -= 1

        # If no possible moves but we've placed some blocks (backtrack)
        elif not possible_types and placed_blocks:
            # Remove the last placed block
            last_pos, last_type = placed_blocks[-1]
            grid = place_block('o', last_pos, grid)  # Reset position to empty
            blocks[last_type] += 1  # Return block to available pool
            
            # Reset attempts tracking for this level if not at total blocks
            if len(placed_blocks) != total_blocks:
                attempts[len(placed_blocks)] = {'A': [], 'B': [], 'C': []}
            placed_blocks.pop()

        # If no possible moves and no blocks placed (complete failure)
        elif not possible_types and not placed_blocks:
            return False

        # Check if we've placed all blocks and if solution is valid
        if len(placed_blocks) == total_blocks:
            if is_puzzle_solved(lazors, grid, targets):
                return grid, placed_blocks

def brute_force_solution(file_path):
    """
    Attempt to solve the puzzle by trying random block placements across all
    available positions (less efficient than smart solution).
    
    Args:
        file_path (str): Path to the puzzle file
        
    Returns:
        tuple: (grid, placed_blocks) if solution found, False otherwise
    """
    # Load puzzle data from file
    grid, blocks, lazors, targets = load_puzzle(file_path)
    total_blocks = sum(blocks[block_type] for block_type in blocks)
    # Initialize tracking of attempted positions for backtracking
    attempts = [{'A': [], 'B': [], 'C': []} for _ in range(total_blocks)]
    placed_blocks = []

    # Main solving loop
    while len(placed_blocks) <= total_blocks:
        possible_types = []
        available_positions = get_available_positions(grid)
        
        # Consider all block types and all available positions
        for block_type in ['A', 'B', 'C']:
            for pos in available_positions:
                if blocks[block_type] > 0 and pos not in attempts[len(placed_blocks)][block_type]:
                    possible_types.append(block_type)

        # If we have possible moves to make
        if possible_types:
            # Randomly select a block type and position
            chosen_type = np.random.choice(possible_types)
            valid_positions = [pos for pos in available_positions
                             if pos not in attempts[len(placed_blocks)][chosen_type]]
            
            chosen_position = valid_positions[np.random.randint(0, len(valid_positions))]
            
            # Place the selected block
            grid = place_block(chosen_type, chosen_position, grid)
            # Record this attempt
            attempts[len(placed_blocks)][chosen_type].append(chosen_position)
            placed_blocks.append((chosen_position, chosen_type))
            blocks[chosen_type] -= 1

        # Backtrack if stuck
        elif not possible_types and placed_blocks:
            last_pos, last_type = placed_blocks[-1]
            grid = place_block('o', last_pos, grid)
            blocks[last_type] += 1
            
            if len(placed_blocks) != total_blocks:
                attempts[len(placed_blocks)] = {'A': [], 'B': [], 'C': []}
            placed_blocks.pop()

        # Complete failure case
        elif not possible_types and not placed_blocks:
            return False

        # Check for solution when all blocks placed
        if len(placed_blocks) == total_blocks:
            if is_puzzle_solved(lazors, grid, targets):
                return grid, placed_blocks