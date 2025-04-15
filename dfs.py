from searchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def search(self):
        stack = [(self.start, [])]  # Each element: (position, path_so_far)
        visited = set()
        self.nodes_generated = 1

        while stack:
            current, path = stack.pop()

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            if current in self.goals:
                return current, self.nodes_generated, self.nodes_visited, path

            for dx, dy, move in reversed(self.directions):  
                # Reversed for correct order due to stack (LIFO)
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if self.is_valid(neighbor) and neighbor not in visited:
                    stack.append((neighbor, path + [move]))
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
