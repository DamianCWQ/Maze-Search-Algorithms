import heapq
from searchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
    def search(self):
        open_list = []
        visited = set()
        self.nodes_visited = 0

        # Initialize the starting node and its f-cost
        goal = self.get_closest_goal(self.start)
        g_costs = {self.start: 0}  # Cost from start to each node
        f_cost = self.heuristic(self.start, goal) # Heuristic cost from start to goal

        # Push the starting node into the open list with its f-cost and path
        heapq.heappush(open_list, (f_cost, 0, self.start, []))

        while open_list:
            _, _, current, path = heapq.heappop(open_list) # Get the node with the lowest f-cost

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            # Check if the current node is a goal
            if current in self.goals:
                return current, self.nodes_visited, path, list(visited)

            # Iterate through possible moves (UP, LEFT, DOWN, RIGHT)
            for dx, dy, move in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                # Check if the neighbor is valid and not already visited
                if not self.is_valid(neighbor) or neighbor in visited:
                    continue
                
                # Calculate the cost to reach the neighbor
                tentative_g = g_costs[current] + 1
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal) # f(n) = g(n) + h(n)

                    # Add the neighbor to the open list with its f-cost and path
                    path_length = len(path) + 1
                    heapq.heappush(open_list, (f, path_length, neighbor, path + [move]))
            
        return None, self.nodes_visited, [], list(visited)

