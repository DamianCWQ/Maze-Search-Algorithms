from searchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def search(self):
        stack = [(self.start, [])]  # Each element: (starting position, path so far)
        visited = set()
        self.nodes_visited = 0

        while stack:
            current, path = stack.pop()

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            if current in self.goals:  # Check if the current node is a goal
                return current, self.nodes_visited, path, list(visited)

            # Iterate through all possible moves
            for dx, dy, move in reversed(self.directions): # Directions are reversed to maintain the order of moves
                nx, ny = current[0] + dx, current[1] + dy # Calculate neighbor position
                neighbor = (nx, ny)
                if self.is_valid(neighbor) and neighbor not in visited:
                    stack.append((neighbor, path + [move]))

        return None, self.nodes_visited, [], list(visited)  # Return empty path if no goal is found
