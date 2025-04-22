from searchAlgorithm import SearchAlgorithm

class IDDFS(SearchAlgorithm):
    def search(self):
        depth = 0 
        self.nodes_visited = 0
        max_depth = 50 # Limit to prevent infinite loops
        all_visited = set() # Track all visited nodes across iterations

        while depth <= max_depth:
            result = self.depth_limited_search(self.start, depth, all_visited)
            if result is not None:
                goal, path = result
                return goal, self.nodes_visited, path, list(all_visited)
            depth += 1
        
        print(f"No path found within the maximum depth limit. (Depth = {max_depth})")
        return None, self.nodes_visited, [], list(all_visited)

    def depth_limited_search(self, start, depth_limit, all_visited):
        stack = [(start, [], depth_limit)]
        visited = set([start])  # Local visited set for this depth iteration
        
        self.nodes_visited += 1
        all_visited.add(start)
        
        while stack:
            current, path, limit = stack.pop()
            
            if current in self.goals:
                return current, path
                
            if limit <= 0:  # Skip expansion if depth limit reached
                continue
                
            # Explore neighbors (in reversed order to match recursive DFS behavior)
            for dx, dy, move in reversed(self.directions):
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                
                if self.is_valid(neighbor) and neighbor not in visited:
                    self.nodes_visited += 1
                    visited.add(neighbor)
                    all_visited.add(neighbor)
                    stack.append((neighbor, path + [move], limit - 1))
        
        # No path found at this depth
        return None