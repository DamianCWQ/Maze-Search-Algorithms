import re

class FileReader:
    def __init__(self, filename = None):
        self.filename = filename
        self.data = None
        
    def _parse_list(self, text):
        # Extract a list of integers from text.
        return list(map(int, re.findall(r'\d+', text)))
        
    def _parse_tuple(self, text):
        # Extract a tuple of integers from text.
        return tuple(map(int, re.findall(r'\d+', text)))
        
    def parse_input_file(self, filename=None):
        # Parse the input file and store the data.
        if filename:
            self.filename = filename
            
        if not self.filename:
            raise ValueError("No filename provided")
            
        with open(self.filename, 'r') as f:
            # Skip empty lines and comment lines starting with //
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("//")]

        try:
            # Parse grid size [N, M]
            grid_size = self._parse_list(lines[0])
            if len(grid_size) < 2:
                raise ValueError("Grid size needs two values")
            
            # Parse initial position (x1, y1)
            initial_position = self._parse_tuple(lines[1])
            if len(initial_position) < 2:
                raise ValueError("Initial position needs two values")
            
            # Parse goal states
            goal_states = []
            goal_parts = lines[2].split('|')
            for goal_str in goal_parts:
                coords = self._parse_tuple(goal_str)
                if len(coords) >= 2:
                    goal_states.append((coords[0], coords[1]))
                else:
                    raise ValueError(f"Invalid goal state: {goal_str}")
            
            # Parse walls
            walls = []
            for wall_line in lines[3:]:
                wall = self._parse_tuple(wall_line)
                if len(wall) >= 4:
                    walls.append((wall[0], wall[1], wall[2], wall[3]))
                else:
                    raise ValueError(f"Invalid wall: {wall_line} (needs 4 values)")
            
            self.data = {
                "grid_size": (grid_size[0], grid_size[1]),
                "initial_position": (initial_position[0], initial_position[1]),
                "goal_states": goal_states,
                "walls": walls
            }
            
            return self.data
            
        except Exception as e:
            raise ValueError(f"Error parsing file: {e}")