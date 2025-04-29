from searchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def search(self):
        self.nodes_visited = 0
        self.visited = set()
        
        # Start the recursive search from the initial position
        goal_pos, path, found = self._dfs(self.start, [])
        
        return (goal_pos, self.nodes_visited, path, list(self.visited)) if found else (None, self.nodes_visited, [], list(self.visited))
    
    def _dfs(self, current, path_so_far):
        """
        Recursive DFS helper function.
        Returns: (goal_position, path, found_goal)
        """
        # Check if the node was already visited
        if current in self.visited:
            return None, path_so_far, False
        
        # Mark as visited and increment counter
        self.visited.add(current)
        self.nodes_visited += 1
        
        # Check if we've found a goal
        if current in self.goals:
            return current, path_so_far, True
        
        # Try each possible direction
        for dx, dy, move in self.directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            
            # Skip invalid or already visited positions
            if not self.is_valid(neighbor):
                continue
                
            # Recursively explore from neighbor
            goal_pos, new_path, found = self._dfs(neighbor, path_so_far + [move])
            
            # If we found a goal from this neighbor, propagate the result back
            if found:
                return goal_pos, new_path, True
        
        # If we get here, no goal was found from this position
        return None, path_so_far, False