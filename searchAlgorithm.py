from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    def __init__(self, grid, start, goals, walls):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.walls = walls
        self.nodes_generated = 0
        self.nodes_visited = 0
        self.directions = [(0, -1, "UP"), (-1, 0, "LEFT"), (0, 1, "DOWN"), (1, 0, "RIGHT")]
        
    @abstractmethod
    def search(self):
        pass