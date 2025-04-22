from searchAlgorithm import SearchAlgorithm
import heapq

class Beam(SearchAlgorithm):
    def __init__(self, grid, start, goals, walls, beam_width = 3):
        super().__init__(grid, start, goals, walls)
        self.beam_width = max(1, beam_width)  # Ensure beam width is at least 1

    def search(self):
        current_level = [(self.heuristic(self.start, self.get_closest_goal(self.start)), 0, self.start, [], None)]
        self.nodes_visited = 0
        visited_nodes = set()

        while current_level:
            # Select top-k nodes for this level
            current_level = heapq.nsmallest(self.beam_width, current_level)
            next_level = []
            
            # Process the current beam
            for _, cost, current, path, parent in current_level:
                self.nodes_visited += 1
                visited_nodes.add(current)
                
                # Check if we reached a goal
                if current in self.goals:
                    return current, self.nodes_visited, path, list(visited_nodes)
                
                # Generate all neighbors
                for dx, dy, move in self.directions:
                    nx, ny = current[0] + dx, current[1] + dy
                    neighbor = (nx, ny)
                    
                    # Cycle prevention - don't go back to parent
                    if parent == neighbor:
                        continue
                        
                    # Check if the move is valid
                    if self.is_valid(neighbor) and neighbor not in visited_nodes:
                        new_cost = cost + 1
                        h = self.heuristic(neighbor, self.get_closest_goal(neighbor))
                        next_level.append((h, new_cost, neighbor, path + [move], current))
            
            # Select unique positions for the next beam
            # This prevents multiple paths to the same state in a single level
            positions_seen = set()
            filtered_next_level = []
            
            for entry in next_level:
                position = entry[2]  # The position is the 3rd element
                if position not in positions_seen:
                    filtered_next_level.append(entry)
                    positions_seen.add(position)
            
            current_level = filtered_next_level

        # No path found
        return None, self.nodes_visited, [], list(visited_nodes)