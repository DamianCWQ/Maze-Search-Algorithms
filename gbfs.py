import heapq
from searchAlgorithm import SearchAlgorithm

class GBFS(SearchAlgorithm):
    def search(self):
        # Priority queue: (heuristic, position, path_so_far)
        open_list = []
        visited = set()
        self.nodes_visited = 0

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
                return current, self.nodes_visited, path, list(visited)

            for dx, dy, move in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if self.is_valid(neighbor) and neighbor not in visited:
                    h = self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (h, neighbor, path + [move]))
                
        return None, self.nodes_visited, [], list(visited)
