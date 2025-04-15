import heapq
from searchAlgorithm import SearchAlgorithm

class GBFS(SearchAlgorithm):
    def search(self):
        # Priority queue: (heuristic, position, path_so_far)
        open_list = []
        visited = set()
        self.nodes_generated = 1

        # Pick the closest goal to guide the heuristic
        goal = self.get_closest_goal(self.start)
        heapq.heappush(open_list, (self.heuristic(self.start, goal), self.start, []))

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

                if self.is_valid(neighbor) and neighbor not in visited:
                    h = self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (h, neighbor, path + [move]))
                    self.nodes_generated += 1

        return None, self.nodes_generated, self.nodes_visited, []

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_closest_goal(self, pos):
        # Return the goal with the smallest heuristic value from pos
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
