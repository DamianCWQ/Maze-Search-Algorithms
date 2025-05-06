from searchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def search(self):
        visited = set()
        self.nodes_visited = 0

        # Start DFS from the initial position
        result = self._dfs(self.start, [], visited)
        if result: # Found a goal
            goal, path = result
            visited_grid = list(visited)
            return goal, self.nodes_visited, path, visited_grid
        else:
            return None, self.nodes_visited, [], list(visited)

    def _dfs(self, current, path, visited):
        if current in visited: # Already visited this node
            return None
        
        visited.add(current) # Mark the current node as visited
        self.nodes_visited += 1 

        if current in self.goals: # Check if current node is a goal
            return current, path

        for dx, dy, move in self.directions:  # Respect order: UP, LEFT, DOWN, RIGHT
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            # Check if the neighbor is valid and not visited
            if self.is_valid(neighbor) and neighbor not in visited:
                result = self._dfs(neighbor, path + [move], visited) # Apply DFS recursively, adding the move to the path
                if result:
                    return result  # Found goal, return early

        return None  # No path found from current

