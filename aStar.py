import heapq
from searchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
    def search(self):
        open_list = []
        visited = set()
        self.nodes_generated = 1

        goal = self.get_closest_goal(self.start)
        g_costs = {self.start: 0}  # Cost from start to each node
        f_cost = self.heuristic(self.start, goal)

        heapq.heappush(open_list, (f_cost, self.start, []))

        while open_list:
            _, current, path = heapq.heappop(open_list)

            if current in visited:
                continue
            self.nodes_visited += 1 # Only unique nodes are counted as visited
            visited.add(current)

            if current in self.goals:
                return current, self.nodes_generated, self.nodes_visited, path

            for dx, dy, move in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if not self.is_valid(neighbor) or neighbor in visited:
                    continue

                tentative_g = g_costs[current] + 1
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f, neighbor, path + [move]))
                    self.nodes_generated += 1

        return None, self.nodes_generated, self.nodes_visited, []

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_closest_goal(self, pos):
        return min(self.goals, key=lambda g: self.heuristic(pos, g))

    def is_valid(self, pos):
        x, y = pos
        rows, cols = self.grid
        if not (0 <= x < cols and 0 <= y < rows):
            return False
        for wx, wy, w, h in self.walls:
            if wx <= x < wx + w and wy <= y < wy + h:
                return False
        return True
