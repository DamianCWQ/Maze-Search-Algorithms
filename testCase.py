from collections import deque
import random

class TestCase:
    def __init__(self, rows, cols, num_goals, num_walls, test_type="random"):
        """
        Initialize a test case with the following parameters:
        - rows: Number of rows in the grid
        - cols: Number of columns in the grid
        - num_goals: Number of goal positions to place
        - num_walls: Number of walls to place
        - test_type: Type of test case ("random", "unreachable", "maze", "dense")
        """
        self.rows = rows
        self.cols = cols
        self.num_goals = num_goals
        self.num_walls = num_walls
        self.test_type = test_type

        # Place the start position in one of the quadrants
        quadrant = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])
        
        if quadrant == "top_left":
            x = random.randint(0, self.cols // 2 - 1)
            y = random.randint(0, self.rows // 2 - 1)
        elif quadrant == "top_right":
            x = random.randint(self.cols // 2, self.cols - 1)
            y = random.randint(0, self.rows // 2 - 1)
        elif quadrant == "bottom_left":
            x = random.randint(0, self.cols // 2 - 1)
            y = random.randint(self.rows // 2, self.rows - 1)
        else:  # bottom_right
            x = random.randint(self.cols // 2, self.cols - 1)
            y = random.randint(self.rows // 2, self.rows - 1)
        
        self.start = (x, y)
        self.start_quadrant = quadrant
        
        # Generate goal positions
        self.goals = self._generate_goals()
        
        # Generate walls based on test type
        if test_type == "unreachable":
            self.walls = self._generate_unreachable_walls()
        elif test_type == "maze":
            self.walls = self._generate_maze_walls()
        elif test_type == "dense":
            self.walls = self._generate_dense_walls()
        else:
            self.walls = self._generate_walls()

    def _is_goal_reachable(self, walls):
        """
        Use flood fill algorithm to check if ALL goals are reachable in a single pass.
        This is a BFS-based implementation that:
        1. Converts walls to blocked cells
        2. Uses a queue to explore all reachable cells
        3. Tracks visited cells to avoid revisiting
        4. Returns True if all goals are found, False otherwise
        """
        # Convert walls to blocked cells for efficient checking
        blocked_cells = set()
        for wx, wy, w, h in walls:
            for dx in range(w):
                for dy in range(h):
                    blocked_cells.add((wx + dx, wy + dy))
        
        # Create a copy of goals as a set for O(1) lookup and removal
        remaining_goals = set(self.goals)
        
        # BFS/Flood fill from start position
        queue = deque([self.start])
        visited = {self.start}
        
        while queue and remaining_goals:  # Continue until queue is empty or all goals found
            x, y = queue.popleft()
            
            # Check if current cell is a goal
            if (x, y) in remaining_goals:
                remaining_goals.remove((x, y))
                
                # Early termination if all goals found
                if not remaining_goals:
                    return True
            
            # Explore all four directions (up, right, down, left)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                # Check if move is valid (within bounds, not blocked, not visited)
                if (0 <= nx < self.cols and 
                    0 <= ny < self.rows and 
                    (nx, ny) not in blocked_cells and 
                    (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        # If we've exhausted the queue and haven't found all goals, they're not all reachable
        return len(remaining_goals) == 0

    def _are_all_goals_reachable(self, walls):
        """Check if ALL goals are reachable"""
        return self._is_goal_reachable(walls)

    def _are_all_goals_unreachable(self, walls):
        """Check if ALL goals are unreachable"""
        return not self._is_goal_reachable(walls)

    def _is_in_buffer_zone(self, x, y):
        """Check if a cell is in the buffer zone (1 cell around the start)"""
        # Check if near the start position
        if abs(x - self.start[0]) <= 1 and abs(y - self.start[1]) <= 1:
            return True
        
        # Check if near any goal position
        for gx, gy in self.goals:
            if abs(x - gx) <= 1 and abs(y - gy) <= 1:
                return True
        
        return False

    def _generate_goals(self):
        """
        Generate goal positions on the edges of the grid with the following constraints:
        1. Goals should be placed only on the perimeter of the grid
        2. No two goals should be at the same position
        3. Goals should not be at the start position
        """
        goals = set()
    
        # Collect all edge positions
        edge_positions = []
        
        # Opposite quadrant edges
        if self.start_quadrant == "top_left":
            # Use bottom and right edges
            for x in range(self.cols // 2, self.cols):
                edge_positions.append((x, self.rows - 1))  # Bottom edge (right half)
            for y in range(self.rows // 2, self.rows - 1):
                edge_positions.append((self.cols - 1, y))  # Right edge (bottom half)
        
        elif self.start_quadrant == "top_right":
            # Use bottom and left edges
            for x in range(0, self.cols // 2):
                edge_positions.append((x, self.rows - 1))  # Bottom edge (left half)
            for y in range(self.rows // 2, self.rows - 1):
                edge_positions.append((0, y))  # Left edge (bottom half)
        
        elif self.start_quadrant == "bottom_left":
            # Use top and right edges
            for x in range(self.cols // 2, self.cols):
                edge_positions.append((x, 0))  # Top edge (right half)
            for y in range(0, self.rows // 2):
                edge_positions.append((self.cols - 1, y))  # Right edge (top half)
        
        else:  # "bottom_right"
            # Use top and left edges
            for x in range(0, self.cols // 2):
                edge_positions.append((x, 0))  # Top edge (left half)
            for y in range(0, self.rows // 2):
                edge_positions.append((0, y))  # Left edge (top half)

        # If we have more goals than available edge positions, adjust
        if self.num_goals > len(edge_positions):
            print(f"Warning: Requested {self.num_goals} goals, but only {len(edge_positions)} edge positions available.")
            self.num_goals = min(self.num_goals, len(edge_positions))
        
        # Randomly select from available edge positions
        selected_positions = random.sample(edge_positions, self.num_goals)
        goals = set(selected_positions)
        
        return list(goals)
    

    def _generate_walls(self):
        """
        Generate random walls with the following constraints:
        1. Walls should not be in buffer zones
        2. Walls should not block all goals
        3. Walls should be within grid bounds
        """
        max_attempts = 100  # Prevent infinite loop
        for attempt in range(max_attempts):
            walls = []
            for _ in range(self.num_walls):
                wx = random.randint(0, self.cols - 2)
                wy = random.randint(0, self.rows - 2)
                w = random.randint(1, min(3, self.cols - wx))
                h = random.randint(1, min(3, self.rows - wy))
                    
                # Check if any part of the wall is in buffer zones
                wall_in_buffer = False
                for dx in range(w):
                    for dy in range(h):
                        if self._is_in_buffer_zone(wx + dx, wy + dy):
                            wall_in_buffer = True
                            break
                    if wall_in_buffer:
                        break
                if (wx + dx, wy + dy) == self.start or (wx + dx, wy + dy) in self.goals:
                    wall_in_buffer = True

                # Only add wall if it doesn't overlap with buffer zones
                if not wall_in_buffer:
                    walls.append((wx, wy, w, h))
                
            # Verify all goals are reachable
            if self._are_all_goals_reachable(walls):
                return walls
        
        return []  # Return empty list if no valid walls found

    def _generate_unreachable_walls(self):
        """
        Generate walls that make goals unreachable by:
        1. Creating a complete enclosure around each goal
        2. Adding additional random walls
        """
        max_attempts = 100
        for attempt in range(max_attempts):
            walls = []
            # Create walls to make goals unreachable
            for gx, gy in self.goals:
                # Create complete enclosure around the goal
                for dx in range(-1, 2): # 3x3 area around the goal
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:  # Skip the goal itself
                            continue
                            
                        wx = gx + dx
                        wy = gy + dy
                        
                        # Ensure wall is within grid bounds
                        if 0 <= wx < self.cols and 0 <= wy < self.rows:
                            # Don't place wall on start
                            if (wx, wy) != self.start:
                                walls.append((wx, wy, 1, 1))
            
            # Add some random walls
            for _ in range(self.num_walls // 2):
                wx = random.randint(0, self.cols - 2)
                wy = random.randint(0, self.rows - 2)
                w = random.randint(1, min(3, self.cols - wx))
                h = random.randint(1, min(3, self.rows - wy))
                
                # Don't block start position
                blocks_start = wx <= self.start[0] < wx + w and wy <= self.start[1] < wy + h
                
                if not blocks_start:
                    walls.append((wx, wy, w, h))
                    
            # Verify all goals are unreachable
            if self._are_all_goals_unreachable(walls):
                return walls
            
        return []  # Return empty list if no valid walls found

    def _generate_maze_walls(self):
        """
        Generate maze-like wall patterns with:
        1. Alternating rows and columns of walls
        2. Random gaps in the walls
        3. Ensuring goals remain reachable
        """
        max_attempts = 100
        for attempt in range(max_attempts):
            walls = []
            # Create maze pattern walls
            for i in range(0, self.rows, 2):
                for j in range(0, self.cols):
                    # Only add wall if not in buffer zone
                    if not self._is_in_buffer_zone(j, i) and random.random() < 0.7:
                        walls.append((j, i, 1, 1))
                
            for i in range(0, self.rows):
                for j in range(0, self.cols, 2):
                    # Only add wall if not in buffer zone
                    if not self._is_in_buffer_zone(j, i) and random.random() < 0.7:
                        walls.append((j, i, 1, 1))
                
            # Verify all goals are reachable
            if self._are_all_goals_reachable(walls):
                return walls
            
        return []  # Return empty list if no valid walls found

    def _generate_dense_walls(self):
        """
        Generate dense wall patterns with:
        1. Approximately 30% of grid filled with walls
        2. Smaller wall sizes (1x1 or 2x2)
        3. Ensuring goals remain reachable
        """
        max_attempts = 100
        for attempt in range(max_attempts): 
            walls = []
            # Fill roughly 30% of grid with walls
            wall_count = int(self.rows * self.cols * 0.3)
            attempts = 0
                
            while len(walls) < wall_count and attempts < 100:
                wx = random.randint(0, self.cols - 2) # Random wall position
                wy = random.randint(0, self.rows - 2)
                w = random.randint(1, 2)  # Smaller walls
                h = random.randint(1, 2)
                    
                # Check if any part of the wall is in buffer zones
                wall_in_buffer = False
                for dx in range(w):
                    for dy in range(h):
                        if self._is_in_buffer_zone(wx + dx, wy + dy):
                            wall_in_buffer = True
                            break
                    if wall_in_buffer:
                        break
                    
                # Only add wall if it doesn't overlap with buffer zones
                if not wall_in_buffer:
                    walls.append((wx, wy, w, h))
                    
                attempts += 1
                
            # Verify all goals are reachable
            if self._are_all_goals_reachable(walls):
                return walls
            
        return []  # Return empty list if no valid walls found

    def save_to_file(self, filename):
        """
        Save the test case to a file with the following format:
        1. Grid dimensions [rows,cols]
        2. Start position (x,y)
        3. Goal positions (x1,y1) | (x2,y2) | ...
        4. Wall positions (x,y,width,height)
        """
        with open(filename, 'w') as f:
            f.write(f"[{self.rows},{self.cols}]\n")
            f.write(f"({self.start[0]},{self.start[1]})\n")
            goal_line = " | ".join(f"({gx},{gy})" for gx, gy in self.goals)
            f.write(goal_line + "\n")
            for wx, wy, w, h in self.walls:
                f.write(f"({wx},{wy},{w},{h})\n")
