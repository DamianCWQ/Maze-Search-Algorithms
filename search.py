import sys
from fileReader import FileReader
from grid import Grid
from dfs import DFS
from bfs import BFS
from gbfs import GBFS
from aStar import AStar
from iddfs import IDDFS
from beam import Beam

def main():
    try:
        # Check arguments - update usage message
        if len(sys.argv) < 3 or len(sys.argv) > 4:
            print("\nUsage: python search.py <filename> <method> [beam width]")
            print("Methods: dfs, bfs, gbfs, astar, iddfs, beam")
            print ("Example: python search.py input.txt astar\n")
            print("To test program: python testSuites.py\n")
            print("Note: beam width is only required when using method beam search method, 'beam'")
            sys.exit(1)

        filename = sys.argv[1]
        method = sys.argv[2].lower()

        beam_width = 3 # Default beam width
        if method == "beam":
            if len(sys.argv) == 4:
                try:
                    beam_width = int(sys.argv[3])
                    if beam_width < 1:
                        print("Beam width must be at least 1, using default (3)")
                except ValueError:
                    print("Invalid beam width value, using default (3)")
            else:
                print("Beam width not provided, using default (3)")

        # Parse the input file
        file_reader = FileReader()
        data = file_reader.parse_input_file(filename)

        # Visualize the initial grid
        grid = Grid(data)
        print("\n--- Initial Grid Map ---")
        grid.visualize_map()
        
        search_algorithms = {
            "dfs": DFS,
            "bfs": BFS,
            "gbfs": GBFS,
            "astar": AStar,
            "iddfs" : IDDFS,
            "beam" : Beam
        }

        if method not in search_algorithms:
            print(f"Invalid search method: {method}. Choose from {list(search_algorithms.keys())}.")
            sys.exit(1)

        # Initialize & run the search algorithms
        algo_class = search_algorithms[method]
        if method == "beam":
            algo = algo_class(
                grid = data["grid_size"],
                start = data["initial_position"],
                goals = data["goal_states"],
                walls = data["walls"],
                beam_width = beam_width
            )
        else:
            algo = algo_class(
                grid = data["grid_size"],
                start = data["initial_position"],
                goals = data["goal_states"],
                walls = data["walls"]
            )
        
        goal, nodes_visited, path, visited_grid = algo.search()

        # Display results
        print(f"\n--- Search Results ({method.upper()}) ---")
        print(f"File: {filename}")
        print(f"Algorithm: {method.upper()}")
        print(f"Nodes visited: {nodes_visited}")
        
        if goal:
            print(f"Goal reached: {goal}")
            print(f"Path: {' '.join(path)}")
            
            # Visualize the solution path on the grid
            print("\n--- Solution Path ---")
            grid.visualize_solution(path, visited_grid)
        else:
            print("No goal is reachable")
            grid.visualize_solution([], visited_grid)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()