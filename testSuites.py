import os
import random
import subprocess
import time
from openpyxl import Workbook

class TestCase:
    def __init__(self, rows, cols, num_goals, num_walls, test_type="random"):
        self.rows = rows
        self.cols = cols
        self.num_goals = num_goals
        self.num_walls = num_walls
        self.test_type = test_type
        self.start = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        self.goals = self._generate_goals()
        
        if test_type == "unreachable":
            self.walls = self._generate_unreachable_walls()
        elif test_type == "maze":
            self.walls = self._generate_maze_walls()
        elif test_type == "dense":
            self.walls = self._generate_dense_walls()
        else:
            self.walls = self._generate_walls()

    def _is_goal_reachable(self, start, goal, walls):
        """Check if a specific goal is reachable from start position"""
        # Convert walls to blocked cells for efficient checking
        blocked_cells = set()
        for wx, wy, w, h in walls:
            for dx in range(w):
                for dy in range(h):
                    blocked_cells.add((wx + dx, wy + dy))
        
        # BFS to check reachability
        from collections import deque
        queue = deque([start])
        visited = {start}
        
        while queue:
            x, y = queue.popleft()
            
            # Check if we reached the goal
            if (x, y) == goal:
                return True
            
            # Try all four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                # Check if move is valid
                if (0 <= nx < self.cols and 
                    0 <= ny < self.rows and 
                    (nx, ny) not in blocked_cells and 
                    (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        return False

    def _are_all_goals_reachable(self, walls):
        """Check if ALL goals are reachable"""
        return all(self._is_goal_reachable(self.start, goal, walls) for goal in self.goals)

    def _are_all_goals_unreachable(self, walls):
        """Check if ALL goals are unreachable"""
        return all(not self._is_goal_reachable(self.start, goal, walls) for goal in self.goals)

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
        goals = set()
        min_distance = max(self.rows, self.cols) // 3  # At least 1/3 of the grid size away
        
        # Adjust min_distance if the grid is too small
        if min_distance < 5:
            min_distance = 5
        
        attempts = 100  # Prevent infinite loop
        while len(goals) < self.num_goals and attempts > 0:
            gx = random.randint(0, self.cols - 1)
            gy = random.randint(0, self.rows - 1)
            
            # Calculate Manhattan distance from start
            distance = abs(gx - self.start[0]) + abs(gy - self.start[1])
            
            # Add goal if it's far enough and not already added
            if (gx, gy) != self.start and distance >= min_distance:
                goals.add((gx, gy))
            
            attempts -= 1
        
        # If we couldn't find enough distant goals, add some closer ones
        # (This ensures we don't get stuck with fewer goals than requested)
        if len(goals) < self.num_goals:
            print(f"Warning: Could not place all goals far from start. Using closer positions.")
            while len(goals) < self.num_goals:
                gx = random.randint(0, self.cols - 1)
                gy = random.randint(0, self.rows - 1)
                if (gx, gy) != self.start and (gx, gy) not in goals:
                    goals.add((gx, gy))
        
        return list(goals)

    def _generate_walls(self):
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
        else:
            self._generate_walls()  # Regenerate if not all goals are reachable
            return walls

    def _generate_unreachable_walls(self):
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
        else:
            self._generate_unreachable_walls()  # Regenerate if not all goals are unreachable
            return walls

    def _generate_maze_walls(self):
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
        else:
            print("Regenerating maze walls...")
            self._generate_maze_walls()
            return walls

    def _generate_dense_walls(self):
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
        else:
            self._generate_dense_walls()  # Regenerate if not all goals are reachable
            return walls

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(f"[{self.rows},{self.cols}]\n")
            f.write(f"({self.start[0]},{self.start[1]})\n")
            goal_line = " | ".join(f"({gx},{gy})" for gx, gy in self.goals)
            f.write(goal_line + "\n")
            for wx, wy, w, h in self.walls:
                f.write(f"({wx},{wy},{w},{h})\n")


class TestSuite:
    def __init__(self, test_dir="tests", output_file="testResult.xlsx"):
        self.test_dir = test_dir
        self.output_file = output_file
        self.algorithms = ["dfs", "bfs", "gbfs", "astar", "iddfs", "beam"]
        self.tests = []

    def generate_tests(self, num_tests=15):
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        # Clear previous tests list
        self.tests = []
        self.test_types = {}  # Map filenames to test types
        
        # Distribution of test types
        random_tests = int(num_tests * 0.5)  # 50% random
        unreachable_tests = int(num_tests * 0.2)  # 20% unreachable
        maze_tests = int(num_tests * 0.15)  # 15% maze
        dense_tests = num_tests - random_tests - unreachable_tests - maze_tests  # 15% dense

        test_counter = 0  # Global counter for all tests
        
        # Generate random tests
        for i in range(random_tests):
            rows = random.randint(6, 15)
            cols = random.randint(6, 15)
            goals = random.randint(1, 3)
            walls = random.randint(3, int(rows * cols * 0.2))
            
            test_case = TestCase(rows, cols, goals, walls, "random")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "random"  # Store the test type
            test_counter += 1
        
        # Generate unreachable tests
        for i in range(unreachable_tests):
            rows = random.randint(6, 12)
            cols = random.randint(6, 12)
            goals = random.randint(1, 2)
            walls = random.randint(5, 15)
            
            test_case = TestCase(rows, cols, goals, walls, "unreachable")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "unreachable"  # Store the test type
            test_counter += 1
        
        # Generate maze tests
        for i in range(maze_tests):
            rows = random.randint(8, 15)
            cols = random.randint(8, 15)
            goals = random.randint(1, 2)
            walls = rows * cols // 3
            
            test_case = TestCase(rows, cols, goals, walls, "maze")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "maze"  # Store the test type
            test_counter += 1
        
        # Generate dense tests
        for i in range(dense_tests):
            rows = random.randint(8, 15)
            cols = random.randint(8, 15)
            goals = random.randint(1, 2)
            walls = int(rows * cols * 0.3)
            
            test_case = TestCase(rows, cols, goals, walls, "dense")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "dense"  # Store the test type
            test_counter += 1

        print(f"✅ Generated {len(self.tests)} test cases")

    def run_tests(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Search Results"
        sheet.append(["Input File", "Test Type", "Algorithm", "Goal Reached", "Nodes Visited", 
                    "Path Length", "Execution Time", "Beam Width"])

        total_tests = len(self.tests) * (len(self.algorithms) - 1 + 4)  # 4 beam widths for beam search
        current = 0

        for test_file in self.tests:
            test_type = self.test_types[test_file]
                
            # Run standard algorithms
            for algo in self.algorithms:
                if algo == "beam":
                    # Test beam search with different widths
                    beam_widths = random.sample(range(1, 11), 4)  # Randomly select 4 unique beam widths between 1 and 10
                    for beam_width in beam_widths:
                        current += 1
                        print(f"[{current}/{total_tests}] Running {algo.upper()} (width={beam_width}) on {os.path.basename(test_file)}")
                        result = self._run_algorithm(test_file, algo, beam_width)
                        sheet.append([
                            os.path.basename(test_file),
                            test_type,
                            algo.upper(),
                            result["goal_reached"],
                            result["nodes_visited"],
                            result["path_length"],
                            result["execution_time"],
                            beam_width
                        ])
                else:
                    current += 1
                    print(f"[{current}/{total_tests}] Running {algo.upper()} on {os.path.basename(test_file)}")
                    result = self._run_algorithm(test_file, algo)
                    sheet.append([
                        os.path.basename(test_file),
                        test_type,
                        algo.upper(),
                        result["goal_reached"],
                        result["nodes_visited"],
                        result["path_length"],
                        result["execution_time"],
                        "N/A"
                    ])
        
        # Auto-adjust column widths
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = max_length + 2
            sheet.column_dimensions[column_letter].width = adjusted_width

        workbook.save(self.output_file)
        print(f"✅ All tests completed. Results saved to '{self.output_file}'")

    def _run_algorithm(self, test_file, algorithm, beam_width=None):
        try:
            cmd = ["python", "search.py", test_file, algorithm]
            if beam_width and algorithm == "beam":
                cmd.append(str(beam_width))

            start_time = time.time()
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            execution_time = time.time() - start_time
            
            output = process.stdout
            
            # Parse results
            goal_reached = "Goal reached:" in output
            
            # Extract nodes visited
            nodes_visited = "0"
            for line in output.split('\n'):
                if "Nodes visited:" in line:
                    try:
                        nodes_visited = line.split("Nodes visited:")[1].strip()
                    except:
                        pass
            
            # Extract path length if goal reached
            path_length = 0
            if goal_reached:
                for line in output.split('\n'):
                    if "Path:" in line:
                        try:
                            path_str = line.split("Path:")[1].strip()
                            path_length = len(path_str.split())
                        except:
                            pass
            
            return {
                "goal_reached": "Yes" if goal_reached else "No",
                "nodes_visited": nodes_visited,
                "path_length": path_length,
                "execution_time": f"{execution_time:.3f}s"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "goal_reached": "Timeout",
                "nodes_visited": "N/A",
                "path_length": "N/A",
                "execution_time": "30s+"
            }
        except Exception as e:
            return {
                "goal_reached": "Error",
                "nodes_visited": "N/A",
                "path_length": "N/A",
                "execution_time": f"Error: {str(e)[:30]}"
            }


if __name__ == "__main__":
    suite = TestSuite()
    suite.generate_tests(15)  # Generate 15 test cases by default
    suite.run_tests()