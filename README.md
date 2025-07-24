# Robot Navigation Search Algorithms
## Overview
This project implements and compares six different search algorithms for pathfinding in grid-based environments. The algorithms are designed to find a path from a start position to one of several possible goal positions while avoiding wall obstacles.

## Features
### Six search algorithm implementations:
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Greedy Best-First Search (GBFS)
- A* Search (A-Star)
- Iterative Deepening Depth-First Search (IDDFS)
- Beam Search with configurable beam width

### Comprehensive testing framework:
- Automatic test case generation
- Four grid types (Random, Maze, Dense, Unreachable)
- Performance metrics (time, memory, nodes explored, path length)
- Results export to Excel and Word documents

### Visualization:
- Text-based grid visualization
- Solution path display
- Visited nodes tracking

## Project Structure
- search.py - Main program entry point
- searchAlgorithm.py - Abstract base class for all algorithms

### Algorithm implementations:
- dfs.py - Depth-First Search
- bfs.py - Breadth-First Search
- gbfs.py - Greedy Best-First Search
- aStar.py - A* Search
- iddfs.py - Iterative Deepening DFS
- beam.py - Beam Search

### Support files:
- fileReader.py - Parses input files
- grid.py - Grid representation and visualization
- testCase.py - Test case generation
- testSuites.py - Test framework

## Usage
### Running a Single Test
To run a specific algorithm on a test file:
```python search.py <filename> <method> [beam_width]```

Where:
- <filename> is the path to a test file
- <method> is one of: dfs, bfs, gbfs, astar, iddfs, beam
- [beam_width] is optional and only used for beam search (default is 3)

#### Example:
```
python search.py input.txt astar
python search.py input.txt beam 3
```

### Input File Format
Test files use the following format:
```
[rows,cols]
(start_x,start_y)
(goal1_x,goal1_y) | (goal2_x,goal2_y) | ...
(wall1_x,wall1_y,width1,height1)
(wall2_x,wall2_y,width2,height2)
...
```

### Running the Test Suite
To generate test cases and run all algorithms on them:
```python testSuites.py```

This will:
- Generate 10 test cases across different grid types
- Run all algorithms on each test case
- Generate an Excel file with results
- Create a detailed Word report with performance analysis

#### Performance Analysis
The test suite generates a comprehensive report comparing all algorithms across different grid types. Performance metrics include:
- Success rate
- Average execution time
- Average nodes visited
- Average path length
- Memory usage
