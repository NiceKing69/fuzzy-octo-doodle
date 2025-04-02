class Lazor:
    """
    A class representing a laser beam in the puzzle, with functionality to:
    - Track the laser's path through the grid
    - Handle interactions with different block types
    - Check if target points are hit by the laser
    
    Attributes:
        start_position (tuple): (x,y) starting coordinates of the laser
        direction_vector (tuple): (dx,dy) direction vector of the laser
    """
    
    def __init__(self, start_position, direction_vector):
        """
        Initialize a Lazor object with starting position and direction.
        
        Args:
            start_position (tuple): (x,y) starting coordinates
            direction_vector (tuple): (dx,dy) direction vector
        """
        self.start_position = start_position
        self.direction_vector = direction_vector

    def get_crossed_blocks_and_path(self, game_grid):
        """
        Calculate the laser's path through the grid and identify all blocks it crosses.
        
        Args:
            game_grid (2D list): The game grid with block placements
            
        Returns:
            tuple: (crossed_blocks, lazor_path) where:
                - crossed_blocks: list of (x,y) positions of blocks the laser interacts with
                - lazor_path: list of all (x,y) points the laser passes through
        """
        current_position = self.start_position
        direction = self.direction_vector

        def is_next_position_valid(current_pos, dir_vec):
            """
            Check if the next position in current direction is within grid bounds.
            
            Args:
                current_pos (tuple): Current (x,y) position
                dir_vec (tuple): Current (dx,dy) direction
                
            Returns:
                bool: True if next position is valid, False otherwise
            """
            next_x = current_pos[0] + dir_vec[0]
            next_y = current_pos[1] + dir_vec[1]
            return 0 <= next_x < len(game_grid[0]) and 0 <= next_y < len(game_grid)
        
        def get_next_block(current_pos, dir_vec):
            """
            Identify the next block the laser will interact with based on current position and direction.
            
            Args:
                current_pos (tuple): Current (x,y) position
                dir_vec (tuple): Current (dx,dy) direction
                
            Returns:
                tuple/False: (x,y) of next block position, or False if no block interaction
            """
            curr_x, curr_y = current_pos
            next_x = current_pos[0] + dir_vec[0]
            next_y = current_pos[1] + dir_vec[1]
            
            # Check for block interaction in x-direction (vertical walls)
            if next_x % 2 and curr_y % 2:
                next_block = (next_x, curr_y)
            # Check for block interaction in y-direction (horizontal walls)
            elif curr_x % 2 and next_y % 2:
                next_block = (curr_x, next_y)
            else:
                return False
            return next_block

        def calculate_reflection(current_pos, dir_vec, next_block_pos):
            """
            Calculate new direction vector after hitting a reflective block.
            
            Args:
                current_pos (tuple): Current (x,y) position before reflection
                dir_vec (tuple): Current (dx,dy) direction before reflection
                next_block_pos (tuple): (x,y) of the block causing reflection
                
            Returns:
                tuple: New (dx,dy) direction vector after reflection
            """
            # Calculate reflection vector (normal to the block surface)
            reflection_vector = (
                next_block_pos[0] - current_pos[0],
                next_block_pos[1] - current_pos[1]
            )
            # Calculate new direction using reflection formula: r = d - 2(d·n)n
            new_direction = (
                dir_vec[0] - 2 * reflection_vector[0],
                dir_vec[1] - 2 * reflection_vector[1]
            )
            return new_direction

        # Initialize tracking of crossed blocks and path points
        crossed_blocks = []
        lazor_path = [self.start_position]  # Path always includes starting point
        
        # Continue tracing path while next position is within grid bounds
        while is_next_position_valid(current_position, direction):
            # Identify next block the laser will interact with
            next_block_pos = get_next_block(current_position, direction)
            next_block_type = game_grid[next_block_pos[1]][next_block_pos[0]]
            
            # Handle different block types
            if next_block_type == 'A':  # Reflective block
                direction = calculate_reflection(current_position, direction, next_block_pos)
            elif next_block_type == 'B':  # Opaque block (stops laser)
                return crossed_blocks, lazor_path
            elif next_block_type == 'C':  # Refractive block
                # Create new laser starting just beyond this block
                new_start = (
                    current_position[0] + direction[0],
                    current_position[1] + direction[1]
                )
                new_lazor = Lazor(new_start, direction)
                # Get path and blocks from the refracted laser
                new_lazor_blocks_path = new_lazor.get_crossed_blocks_and_path(game_grid)
                
                # Combine results from refracted path
                crossed_blocks.extend(new_lazor_blocks_path[0])
                lazor_path.extend(new_lazor_blocks_path[1])
                
                # Also reflect off the surface (like block A)
                direction = calculate_reflection(current_position, direction, next_block_pos)
                continue
            elif next_block_type == 'o':  # Target point
                crossed_blocks.append(next_block_pos)

            # Move laser to next position
            current_position = (
                current_position[0] + direction[0],
                current_position[1] + direction[1]
            )
            lazor_path.append(current_position)
        
        return crossed_blocks, lazor_path
    
    def check_goals(self, game_grid, target_points):
        """
        Check which target points are hit by this laser's path.
        
        Args:
            game_grid (2D list): The game grid with block placements
            target_points (list): List of (x,y) target positions
            
        Returns:
            list: Target points that were NOT hit by this laser
        """
        # Get all points in laser path (convert to set for fast lookup)
        lazor_path = set(self.get_crossed_blocks_and_path(game_grid)[1])
        # Return targets not found in laser path
        return [point for point in target_points if point not in lazor_path]

def is_puzzle_solved(lazor_objects, grid, target_points):
    """
    Check if all target points are hit by any of the lasers.
    
    Args:
        lazor_objects (list): List of Lazor instances
        grid (2D list): The game grid with block placements
        target_points (list): List of (x,y) target positions
        
    Returns:
        bool: True if all targets are hit, False otherwise
    """
    for lazor in lazor_objects:
        # Each laser removes the targets it hits from the list
        target_points = lazor.check_goals(grid, target_points)
    # Puzzle is solved when no targets remain unhit
    return len(target_points) == 0