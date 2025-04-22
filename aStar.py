import heapq
from searchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
    def search(self):
        open_list = []
        visited = set()
        self.nodes_visited = 0

        goal = self.get_closest_goal(self.start)
        g_costs = {self.start: 0}  # Cost from start to each node
        f_cost = self.heuristic(self.start, goal)

        # Used to p
        heapq.heappush(open_list, (f_cost, 0, self.start, []))

        while open_list:
            _, _, current, path = heapq.heappop(open_list)

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            if current in self.goals:
                return current, self.nodes_visited, path, list(visited)

            for dx, dy, move in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if not self.is_valid(neighbor) or neighbor in visited:
                    continue

                tentative_g = g_costs[current] + 1
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)

                    path_length = len(path) + 1
                    heapq.heappush(open_list, (f, path_length, neighbor, path + [move]))
            
        return None, self.nodes_visited, [], list(visited)
