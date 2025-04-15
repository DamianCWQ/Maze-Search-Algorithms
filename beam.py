from searchAlgorithm import SearchAlgorithm
import heapq

class Beam(SearchAlgorithm):
    # Initialize the Beam Search algorithm with grid, start position, goal positions, walls, and beam width
    def __init__(self, grid, start, goals, walls, beam_width=2):
        super().__init__(grid, start, goals, walls)
        self.beam_width = beam_width

    def search(self):
        current_level = [(self.heuristic(self.start, self.get_closest_goal(self.start)), self.start, [])]
        visited = set()
        self.nodes_generated = 1
        self.nodes_visited = 0

        while current_level:
            # Sort by heuristic and select top-k
            current_level = heapq.nsmallest(self.beam_width, current_level)
            next_level = []

            for _, current, path in current_level:
                self.nodes_visited += 1

                if current in visited:
                    continue
                visited.add(current)

                if current in self.goals:
                    return current, self.nodes_generated, self.nodes_visited, path

                for dx, dy, move in self.directions:
                    nx, ny = current[0] + dx, current[1] + dy
                    neighbor = (nx, ny)
                    if self.is_valid(neighbor) and neighbor not in visited:
                        h = self.heuristic(neighbor, self.get_closest_goal(neighbor))
                        next_level.append((h, neighbor, path + [move]))
                        self.nodes_generated += 1

            current_level = next_level

        return None, self.nodes_generated,self.nodes_visited, []

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_closest_goal(self, pos):
        return min(self.goals, key=lambda g: self.heuristic(pos, g))

    def is_valid(self, pos):
        x, y = pos
        rows, cols = self.grid
        if not (0 <= x < cols and 0 <= y < rows):
            return False
        for wx, wy, w, h in self.walls:
            if wx <= x < wx + w and wy <= y < wy + h:
                return False
        return True
