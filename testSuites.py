import os
import random
import subprocess
from openpyxl import Workbook
from testCase import TestCase

class TestSuite:
    def __init__(self, test_dir="tests", output_file="testResult.xlsx"):
        """
        Initialize a test suite with:
        - test_dir: Directory to store test files
        - output_file: Excel file to store results
        - algorithms: List of search algorithms to test
        """
        self.test_dir = test_dir
        self.output_file = output_file
        self.algorithms = ["dfs", "bfs", "gbfs", "astar", "iddfs", "beam"]
        self.tests = []

    def generate_tests(self, num_tests=15):
        """
        Generate a set of test cases with different types:
        - 50% random tests
        - 20% unreachable tests
        - 15% maze tests
        - 15% dense tests
        """
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        # Clear previous tests list
        self.tests = []
        self.test_types = {}  # Map filenames to test types
        
        # Distribution of test types
        random_tests = int(num_tests * 0.5)  # 50% random
        unreachable_tests = int(num_tests * 0.2)  # 20% unreachable
        maze_tests = int(num_tests * 0.15)  # 15% maze
        dense_tests = num_tests - random_tests - unreachable_tests - maze_tests  # 15% dense

        test_counter = 0  # Global counter for all tests
        
        # Generate random tests
        for i in range(random_tests):
            rows = random.randint(6, 15)
            cols = random.randint(6, 15)
            goals = random.randint(1, 3)
            walls = random.randint(3, int(rows * cols * 0.2))
            
            test_case = TestCase(rows, cols, goals, walls, "random")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "random"
            test_counter += 1
        
        # Generate unreachable tests
        for i in range(unreachable_tests):
            rows = random.randint(6, 12)
            cols = random.randint(6, 12)
            goals = random.randint(1, 2)
            walls = random.randint(5, 15)
            
            test_case = TestCase(rows, cols, goals, walls, "unreachable")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "unreachable"
            test_counter += 1
        
        # Generate maze tests
        for i in range(maze_tests):
            rows = random.randint(8, 15)
            cols = random.randint(8, 15)
            goals = random.randint(1, 2)
            walls = rows * cols // 3
            
            test_case = TestCase(rows, cols, goals, walls, "maze")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "maze"
            test_counter += 1
        
        # Generate dense tests
        for i in range(dense_tests):
            rows = random.randint(8, 15)
            cols = random.randint(8, 15)
            goals = random.randint(1, 2)
            walls = int(rows * cols * 0.3)
            
            test_case = TestCase(rows, cols, goals, walls, "dense")
            filename = os.path.join(self.test_dir, f"test{test_counter}.txt")
            test_case.save_to_file(filename)
            self.tests.append(filename)
            self.test_types[filename] = "dense"
            test_counter += 1

        print(f"✅ Generated {len(self.tests)} test cases")

    def algorithm_analysis(self, workbook):
        """Add sheets with deeper algorithm performance analysis"""
        analysis = workbook.create_sheet("Algorithm Analysis")
        
        # Header
        analysis['A1'] = "SEARCH ALGORITHM COMPLEXITY ANALYSIS"        
        # Calculate performance metrics by test type
        test_types = set(self.test_types.values())
        algorithms = self.algorithms
        
        # Prepare data structures for analysis
        performance_by_type = {}
        for test_type in test_types:
            performance_by_type[test_type] = {}
            for algo in algorithms:
                performance_by_type[test_type][algo.upper()] = {
                    "runs": 0, "successes": 0, "total_time": 0.0,
                    "total_nodes": 0, "total_path_length": 0
                }
        
        # Extract data from results sheet
        results_sheet = workbook["Search Results"]
        for row in list(results_sheet.rows)[1:]:  # Skip header
            test_type = row[1].value
            algo = row[2].value
            goal_reached = row[3].value == "Yes"
            
            # Get performance data
            try:
                nodes = int(row[4].value) if row[4].value not in ["N/A", None] else 0
                path_length = int(row[5].value) if row[5].value not in ["N/A", None] else 0
                
                # Fix time parsing
                time_str = row[6].value
                if time_str and isinstance(time_str, str):
                    if "ms" in time_str:
                        # Convert milliseconds to seconds
                        time_val = float(time_str.replace("ms", "")) / 1000.0
                    elif "s" in time_str:
                        time_val = float(time_str.replace("s", ""))
                    else:
                        time_val = 0.0
                else:
                    time_val = 0.0
                
                # Update statistics
                if test_type in performance_by_type and algo in performance_by_type[test_type]:
                    performance_by_type[test_type][algo]["runs"] += 1
                    if goal_reached:
                        performance_by_type[test_type][algo]["successes"] += 1
                        performance_by_type[test_type][algo]["total_time"] += time_val
                        performance_by_type[test_type][algo]["total_nodes"] += nodes
                        performance_by_type[test_type][algo]["total_path_length"] += path_length
            except Exception as e:
                print(f"Error processing row data: {e}")
                pass  # Skip problematic data
        
        # Add analysis tables to sheet
        analysis['A3'] = "PERFORMANCE BY TEST TYPE AND ALGORITHM"
        row = 4
        for test_type in sorted(test_types):
            analysis[f'A{row}'] = f"Test Type: {test_type.upper()}"
            row += 1
            
            # Add header row
            analysis.append(["Algorithm", "Success Rate", "Avg Time (ms)", "Avg Nodes", "Avg Path Length", "Memory Efficientcy*"])
            
            # Add algorithm data
            for algo in [a.upper() for a in algorithms]:
                perf = performance_by_type[test_type][algo]
                success_rate = f"{(perf['successes'] / perf['runs'] * 100):.1f}%" if perf['runs'] > 0 else "N/A"
                avg_time = f"{(perf['total_time'] / perf['successes']) * 1000:.4f}" if perf['successes'] > 0 else "N/A"
                avg_nodes = f"{(perf['total_nodes'] / perf['successes']):.1f}" if perf['successes'] > 0 else "N/A"
                avg_path = f"{(perf['total_path_length'] / perf['successes']):.1f}" if perf['successes'] > 0 else "N/A"
                
                # Memory used per node (lower is better)
                if perf['total_nodes'] > 0:
                    # Calculate memory efficiency per test run, then average
                    memory_efficiencies = []
                    test_names = set()
                    
                    # First pass: collect all test names for this algo and type
                    for test_row in list(results_sheet.rows)[1:]:
                        if test_row[1].value == test_type and test_row[2].value == algo and test_row[3].value == "Yes":
                            test_names.add(test_row[0].value)
                    
                    # Second pass: calculate efficiency for each test
                    for test_name in test_names:
                        # Find matching rows for this test
                        for test_row in list(results_sheet.rows)[1:]:
                            if (test_row[0].value == test_name and 
                                test_row[1].value == test_type and 
                                test_row[2].value == algo and
                                test_row[3].value == "Yes"):
                                try:
                                    # Get memory usage
                                    mem_str = test_row[8].value
                                    nodes_str = test_row[4].value
                                    
                                    if mem_str and "KB" in mem_str and nodes_str and nodes_str != "N/A":
                                        memory = float(mem_str.split()[0])
                                        nodes = int(nodes_str)
                                        
                                        if nodes > 0:
                                            # Calculate KB per node for this test
                                            memory_efficiencies.append(memory / nodes)
                                except Exception as e:
                                    print(f"Error calculating memory efficiency: {e}")
                    
                    # Calculate the average efficiency
                    if memory_efficiencies:
                        avg_memory_efficiency = sum(memory_efficiencies) / len(memory_efficiencies)
                        memory_efficiency_str = f"{avg_memory_efficiency:.4f} KB/node"
                    else:
                        memory_efficiency_str = "N/A"
                else:
                    memory_efficiency_str = "N/A"
                    
                analysis.append([algo, success_rate, avg_time, avg_nodes, avg_path, memory_efficiency_str])
                
            row += len(algorithms) + 2
            
        # Add explanation of memory efficiency
        analysis[f'A{row}'] = "*Memory Efficiency: Average memory usage per node visited (KB/node)."
        analysis[f'A{row+1}'] = "Lower values indicate better memory efficiency (exploring nodes using less memory)."

    def run_tests(self):
        """
        Run all tests with all algorithms and save results to Excel file.
        For beam search, test with 4 different beam widths.
        """
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Search Results"
        sheet.append(["Input File", "Test Type", "Algorithm", "Goal Reached", "Nodes Visited", 
                    "Path Length", "Execution Time", "Beam Width", "Memory Used (KB)"])

        total_tests = len(self.tests) * (len(self.algorithms) - 1 + 4)  # 4 beam widths for beam search
        current = 0

        for test_file in self.tests:
            test_type = self.test_types[test_file]
                
            # Run standard algorithms
            for algo in self.algorithms:
                if algo == "beam":
                    # Test beam search with different widths
                    beam_widths = random.sample(range(1, 6), 4)  # Randomly select 4 unique beam widths between 1 and 5
                    for beam_width in beam_widths:
                        current += 1
                        print(f"[{current}/{total_tests}] Running {algo.upper()} (width={beam_width}) on {os.path.basename(test_file)}")
                        result = self._run_algorithm(test_file, algo, beam_width)
                        sheet.append([
                            os.path.basename(test_file),
                            test_type,
                            algo.upper(),
                            result["goal_reached"],
                            result["nodes_visited"],
                            result["path_length"],
                            result["execution_time"],
                            beam_width,
                            result["memory_used"]
                        ])
                else:
                    current += 1
                    print(f"[{current}/{total_tests}] Running {algo.upper()} on {os.path.basename(test_file)}")
                    result = self._run_algorithm(test_file, algo)
                    sheet.append([
                        os.path.basename(test_file),
                        test_type,
                        algo.upper(),
                        result["goal_reached"],
                        result["nodes_visited"],
                        result["path_length"],
                        result["execution_time"],
                        "N/A",
                        result["memory_used"]
                    ])
        
        # Add algorithm complexity analysis
        self.algorithm_analysis(workbook)

        workbook.save(self.output_file)
        print(f"✅ All tests completed. Results saved to '{self.output_file}'")

    def _run_algorithm(self, test_file, algorithm, beam_width=None):
        """
        Run a single algorithm on a test file and return results:
        - goal_reached: Whether the goal was found
        - nodes_visited: Number of nodes explored
        - path_length: Length of the path found
        - execution_time: Time taken to run the algorithm
        """
        try:
            cmd = ["python", "search.py", test_file, algorithm]
            if beam_width and algorithm == "beam":
                cmd.append(str(beam_width))

            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            output = process.stdout

            # Parse output
            goal_reached = "Goal reached:" in output
            
            # Extract nodes visited
            nodes_visited = "0"
            for line in output.split('\n'):
                if "Nodes visited:" in line:
                    try:
                        nodes_visited = line.split("Nodes visited:")[1].strip()
                    except:
                        pass
            
            # Extract execution time
            execution_time = 0
            for line in output.split('\n'):
                if "Execution time:" in line:
                    try:
                        time_str = line.split("Execution time:")[1].strip()
                        execution_time = float(time_str.split()[0])
                    except:
                        pass
            
            # Extract memory used
            memory_used = 0
            for line in output.split('\n'):
                if "Memory used:" in line:
                    try:
                        memory_str = line.split("Memory used:")[1].strip()
                        memory_used = float(memory_str.split()[0])
                    except:
                        pass
            
            # Extract path length if goal reached
            path_length = 0
            if goal_reached:
                for line in output.split('\n'):
                    if "Path:" in line:
                        try:
                            path_str = line.split("Path:")[1].strip()
                            path_length = len(path_str.split())
                        except:
                            pass
            
            return {
                "goal_reached": "Yes" if goal_reached else "No",
                "nodes_visited": nodes_visited,
                "path_length": path_length,
                "execution_time": f"{execution_time:.3f}ms",
                "memory_used": f"{memory_used:.2f} KB"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "goal_reached": "Timeout",
                "nodes_visited": "N/A",
                "path_length": "N/A",
                "execution_time": "30s+",
                "memory_used": "N/A"
            }
        except Exception as e:
            return {
                "goal_reached": "Error",
                "nodes_visited": "N/A",
                "path_length": "N/A",
                "execution_time": f"Error: {str(e)[:30]}",
                "memory_used": "N/A"
            }


if __name__ == "__main__":
    # Create and run a test suite with 15 test cases
    suite = TestSuite()
    suite.generate_tests(15)
    suite.run_tests()