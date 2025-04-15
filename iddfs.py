from searchAlgorithm import SearchAlgorithm

class IDDFS(SearchAlgorithm):
    def search(self):
        depth = 0 # Start with depth 0
        self.nodes_generated = 0
        self.nodes_visited = 0
        max_depth = 500 # Limit to prevent infinite loops

        while depth <= max_depth:
            visited = set()
            result = self.depth_limited_search(self.start, [], depth, visited)
            if result is not None:
                goal, path = result
                return goal, self.nodes_generated, self.nodes_visited, path
            depth += 1
        
        # No path found within the max depth
        print (f"No path found within the maximum depth limit. (Depth = {max_depth})")
        return None, self.nodes_generated, self.nodes_visited, []

    def depth_limited_search(self, current, path, limit, visited):
        self.nodes_generated += 1
        self.nodes_visited += 1

        if current in self.goals:
            return current, path

        if limit == 0:
            return None

        visited.add(current)

        for dx, dy, move in self.directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if self.is_valid(neighbor) and neighbor not in visited:
                result = self.depth_limited_search(neighbor, path + [move], limit - 1, visited.copy())
                if result:
                    return result

        return None

    def is_valid(self, pos):
        x, y = pos
        rows, cols = self.grid
        if not (0 <= x < cols and 0 <= y < rows):
            return False
        for wx, wy, w, h in self.walls:
            if wx <= x < wx + w and wy <= y < wy + h:
                return False
        return True
