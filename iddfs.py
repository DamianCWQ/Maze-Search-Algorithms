from searchAlgorithm import SearchAlgorithm

class IDDFS(SearchAlgorithm):
    def search(self):
        depth = 0 
        self.nodes_visited = 0
        max_depth = self.grid[0] * self.grid[1] # Limit according to row * cols to prevent infinite loops
        all_visited = set() # Track all visited nodes across iterations

        while depth <= max_depth:
            # Create fresh visited set for each depth iteration
            visited = set([self.start])
            self.nodes_visited += 1
            all_visited.add(self.start)
            
            # Call recursive depth-limited search
            result = self.depth_limited_search(self.start, [], depth, visited, all_visited)
            if result:
                goal, path = result
                return goal, self.nodes_visited, path, list(all_visited)
            depth += 1
        
        print(f"No path found within the maximum depth limit. (Depth = {max_depth})")
        return None, self.nodes_visited, [], list(all_visited)

    def depth_limited_search(self, current, path_so_far, limit, visited, all_visited):
        """
        Recursive depth-limited search implementation.
        Returns: (goal_position, path) or None if not found
        """
        # Check if current is a goal
        if current in self.goals:
            return current, path_so_far
        
        # Stop if depth limit reached
        if limit <= 0:
            return None
        
        # Try each direction
        for dx, dy, move in self.directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            
            # Only explore valid unvisited positions
            if self.is_valid(neighbor) and neighbor not in visited:
                # Mark as visited immediately when discovered
                self.nodes_visited += 1
                visited.add(neighbor)
                all_visited.add(neighbor)
                
                # Explore recursively with reduced depth limit
                result = self.depth_limited_search(neighbor, path_so_far + [move], limit - 1, visited, all_visited)
                
                # If goal found, propagate result back up the call stack
                if result:
                    return result
        
        # No path found within this branch
        return None