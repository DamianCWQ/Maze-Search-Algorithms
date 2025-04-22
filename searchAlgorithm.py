from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    def __init__(self, grid, start, goals, walls):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.walls = walls
        self.nodes_visited = 0
        self.directions = [(0, -1, "UP"), (-1, 0, "LEFT"), (0, 1, "DOWN"), (1, 0, "RIGHT")]

    def is_valid(self, pos):
        """Check if a position is valid (within grid bounds and not a wall)"""
        x, y = pos
        rows, cols = self.grid
        if not (0 <= x < cols and 0 <= y < rows):
            return False
        for wx, wy, w, h in self.walls:
            if wx <= x < wx + w and wy <= y < wy + h:
                return False
        return True
    
    def heuristic(self, a, b):
        """Calculate Manhattan distance heuristic (Absolute distance between two points)"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_closest_goal(self, pos):
        """Find the closest goal from a position using the heuristic"""
        # Handle edge case
        if not self.goals:
            return None
            
        # Initialize with the first goal
        closest_goal = self.goals[0]
        min_distance = self.heuristic(pos, closest_goal)
        
        # Check each goal to find the closest one
        for goal in self.goals:
            # Calculate Manhattan distance
            current_distance = self.heuristic(pos, goal)

            # Update if we found a closer goal
            if current_distance < min_distance:
                min_distance = current_distance
                closest_goal = goal
                
        return closest_goal

    @abstractmethod
    def search(self):
        pass