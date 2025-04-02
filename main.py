import time
from file_parser import load_puzzle
from solver import smart_solution, brute_force_solution
from grid_utils import display_solution

def solve_puzzle():
    """
    Main function to solve the puzzle.
    Returns True if puzzle was solved, False otherwise.
    """
    start_time = time.time()
    
    print("Please input your file name (Full name with .bff):")
    puzzle_file = input().strip('"')
    
    try:
        # Try smart method first
        solution = smart_solution(puzzle_file)
        
        if not solution:
            # Fall back to brute force if smart fails
            solution = brute_force_solution(puzzle_file)
        
        if solution:
            end_time = time.time()
            grid, placed_blocks = solution
            display_solution(grid, placed_blocks)
            print(f"\nPuzzle solved in {end_time - start_time:.2f} seconds")
            return True
        else:
            print("\nFailed to solve the puzzle")
            return False
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        return False

if __name__ == '__main__':
    solve_puzzle()