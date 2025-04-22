class Grid:
    def __init__(self, data=None):
        self.data = data
        self.wall_cells = set()
        
        if data:
            self._calculate_wall_cells()
            
    def _calculate_wall_cells(self):
        """Pre-calculate all wall cells for faster lookups."""
        self.wall_cells = set()
        for x, y, w, h in self.data["walls"]:
            for dx in range(w):
                for dy in range(h):
                    self.wall_cells.add((x + dx, y + dy))

    def visualize_map(self):
        """Visualize the basic grid map."""
        if not self.data:
            raise ValueError("No data provided for visualization.")
            
        rows, cols = self.data["grid_size"]
        grid = [["." for _ in range(cols)] for _ in range(rows)]

        # Mark walls
        for (x, y) in self.wall_cells:
            if 0 <= y < rows and 0 <= x < cols:
                grid[y][x] = "#"

        # Mark goals
        for (gx, gy) in self.data["goal_states"]:
            if 0 <= gy < rows and 0 <= gx < cols:
                grid[gy][gx] = "G"

        # Mark initial position (after goals/walls to override)
        ix, iy = self.data["initial_position"]
        if 0 <= iy < rows and 0 <= ix < cols:
            grid[iy][ix] = "S"

        print("\nGrid Map:")
        for row in grid:
            print(" ".join(row))

    def visualize_solution(self, path, visited = None):
        """Visualize a solution path on the grid."""
        if not self.data:
            print("No grid data available.")
            return
            
        # Convert path from directions to coordinates if needed
        coords = self._path_to_coordinates(path)
        
        rows, cols = self.data["grid_size"]
        grid = [["." for _ in range(cols)] for _ in range(rows)]

        # Mark walls
        for (x, y) in self.wall_cells:
            if 0 <= y < rows and 0 <= x < cols:
                grid[y][x] = "#"

        # Mark visited nodes
        if visited:
            for (x, y) in visited:
                if 0 <= y < rows and 0 <= x < cols:
                    grid[y][x] = "+"

        reached_goals = []

        # Mark path
        for i, (x, y) in enumerate(coords):
            if 0 <= y < rows and 0 <= x < cols:
                # Use different symbols for start, end, and path steps
                if i == 0:
                    grid[y][x] = "S"  # Start position
                elif (x, y) in self.data["goal_states"]:
                    grid[y][x] = "G"  # Goal position
                else:
                    grid[y][x] = "P"  # Path step
        
        # Mark remaining goals that weren't reached
        for (gx, gy) in self.data["goal_states"]:
            if (gx, gy) not in reached_goals and 0 <= gy < rows and 0 <= gx < cols:
                grid[gy][gx] = "G"  # Unreached goal

        # Print the grid
        for row in grid:
            print(" ".join(row))
        print("\nS = Start  G = Goal  P = Path  + = Visited  # = Wall")
        
    def _path_to_coordinates(self, path):
        """Convert a path to coordinates."""
        # If path is already coordinates, return it
        if path and isinstance(path[0], tuple):
            return path
            
        # Convert direction strings to coordinates
        moves = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        x, y = self.data["initial_position"]
        coords = [(x, y)]
        
        for direction in path:
            dx, dy = moves.get(direction.lower(), (0, 0))
            x, y = x + dx, y + dy
            coords.append((x, y))
            
        return coords