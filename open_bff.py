class LazorGame:
    def __init__(self, file_path):
        self.grid = []       # 2D List for the grid
        self.blocks = {}     # Dictionary of available blocks
        self.lasers = []     # List of (x, y, vx, vy)
        self.targets = []    # List of (x, y) points
        self.read_file(file_path)  # Call the method to parse the file

    def read_file(self, file_path):
        """Reads and parses the .bff file, storing data into attributes."""
        with open(file_path, "r") as file:
            raw_lines = file.readlines()  # Read all lines from the file
        
        # Process lines: Remove comments (#) and blank lines
        lines = []
        for line in raw_lines:
            line = line.strip()  # Remove extra spaces/newline characters
            if not line or line.startswith("#"):  # Ignore empty lines and comments
                continue
            lines.append(line)  # Add valid lines to the list

        # Read the structured data
        grid_mode = False
        for i, line in enumerate(lines):
            if line == "GRID START":
                grid_mode = True
                continue
            elif line == "GRID STOP":
                grid_mode = False
                continue

            if grid_mode:
                self.grid.append(line.split())  # Store grid as a list of lists
            
            elif line[0] in {"A", "B", "C"}:  # Blocks (Reflect, Opaque, Refract)
                block_type, count = line.split()
                self.blocks[block_type] = int(count)
            
            elif line[0] == "L":  # Lasers
                _, x, y, vx, vy = line.split()
                self.lasers.append((int(x), int(y), int(vx), int(vy)))
            
            elif line[0] == "P":  # Targets
                _, x, y = line.split()
                self.targets.append((int(x), int(y)))

# define the display information function
    def display_info(self):
        print("Grid:")
        for row in self.grid:
            print(" ".join(row))
        print("\nBlocks:", self.blocks)
        print("\nLasers:", self.lasers)
        print("\nTargets:", self.targets)
        print('\n')



# Example Usage
lazor_game = LazorGame("mad_1.bff")
lazor_game.display_info()
