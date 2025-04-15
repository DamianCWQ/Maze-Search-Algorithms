from collections import deque
from searchAlgorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    def search(self):
        queue = deque([(self.start, [])])  # Each element: (position, path_so_far)
        visited = set()
        self.nodes_generated = 1

        while queue:
            current, path = queue.popleft()

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            if current in self.goals:
                return current, self.nodes_generated, self.nodes_visited, path

            for dx, dy, move in self.directions:  # No reversal for BFS
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if self.is_valid(neighbor) and neighbor not in visited:
                    queue.append((neighbor, path + [move]))
                    self.nodes_generated += 1

        return None, self.nodes_generated, self.nodes_visited, []

    def is_valid(self, pos):
        x, y = pos
        rows, cols = self.grid
        if not (0 <= x < cols and 0 <= y < rows):
            return False
        for wx, wy, w, h in self.walls:
            if wx <= x < wx + w and wy <= y < wy + h:
                return False
        return True