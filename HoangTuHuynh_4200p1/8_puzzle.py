import heapq
import random


class PuzzleState:
    def __init__(self, board, goal, moves=0, heuristic_func = None, parent= None):
        self.board = board
        self.goal = goal
        self.moves = moves  # This represents the depth
        self.heuristic_func = heuristic_func
        self.parent = parent

    def is_goal(self):
        return self.board == self.goal

    def next_states(self):
        # Generate next states
        moves = []
        zero_pos = self.board.index(0)  # Find the position of the blank tile (represented as 0)
        row, col = zero_pos // 3, zero_pos % 3

        # Directions in which the blank tile can move
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_pos = new_row * 3 + new_col
                new_board = list(self.board)
                new_board[zero_pos], new_board[new_pos] = new_board[new_pos], new_board[zero_pos]
                moves.append(PuzzleState(tuple(new_board), self.goal, self.moves + 1, parent=self))

        return moves

    def __lt__(self, other):
        return self.heuristic(self.heuristic_func) < other.heuristic(other.heuristic_func)

    def heuristic(self, func):
        return func(self.board, self.goal) + self.moves

def astar_search(start_state, heuristic_func, max_depth):
    frontier = []
    heapq.heappush(frontier, (0, start_state))
    explored = set()
    search_cost = 0  # Initialize search cost counter

    while frontier:
        _, current_state = heapq.heappop(frontier)
        search_cost += 1  # Increment search cost for each state explored

        if current_state.is_goal():
            return current_state, search_cost  # Return the solution and the search cost

        if current_state.moves > max_depth:
            continue  # Skip if the current depth exceeds the max depth

        explored.add(current_state.board)

        for state in current_state.next_states():
            if state.board not in explored:
                new_state = PuzzleState(state.board, state.goal, state.moves, heuristic_func, parent=current_state)
                total_cost = new_state.heuristic(heuristic_func)
                heapq.heappush(frontier, (total_cost, new_state))

    return None, search_cost  # No solution found, return search cost anyway

def h1(board, goal):
    return sum(b != g and b != 0 for b, g in zip(board, goal))  # Number of misplaced tiles excluding the blank one

def h2(board, goal):
    total_distance = 0
    for i in range(1, 9):
        xi, yi = board.index(i) // 3, board.index(i) % 3
        xg, yg = goal.index(i) // 3, goal.index(i) % 3
        total_distance += abs(xi - xg) + abs(yi - yg)
    return total_distance

def read_puzzle_input():
    print("Enter your 8-puzzle configuration row by row (use 0 for the empty tile):")
    puzzle = []
    for _ in range(3):
        row = input().strip().split()
        puzzle.extend([int(n) for n in row])
    return tuple(puzzle)

def generate_random_puzzle():
    puzzle = list(range(9))
    random.shuffle(puzzle)
    return tuple(puzzle)

def print_solution(solution_state):
    path = []
    while solution_state:
        path.append(solution_state)
        solution_state = solution_state.parent
    for state in reversed(path):
        print("Step:", state.moves)
        for i in range(0, 9, 3):
            print(' '.join(map(str, state.board[i:i+3])))
        print()  # Optional: for better readability
def single_test_puzzle():
    print("Select Input Method:\n[1] Random\n[2] File")
    choice = input("Enter your choice: ")
    if choice == '1':
        initial_board = generate_random_puzzle()
        print("Randomly generated puzzle:")
        for i in range(0, 9, 3):
            print(' '.join(map(str, initial_board[i:i+3])))
        print()  # Optional: for better readability
    else:
        initial_board = read_puzzle_input()
        

    

    # Choose heuristic function
    heuristic_choice = input("Select H Function: \n[1] H1\n[2] H2\n ").strip()
    heuristic_func = h1 if heuristic_choice == '1' else h2

    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    initial_state = PuzzleState(initial_board, goal_state, 0, heuristic_func)

    max_depth = int(input("Enter Solution Depth (2-20): "))
    result, search_cost = astar_search(initial_state, heuristic_func, max_depth)
    if result:
        print_solution(result)
        print("Search Cost:", search_cost)
    else:
        print("No solution found")
        print("Search Cost:", search_cost)

def multiple_test():
    test_cases = int(input("Number of test cases: "))
    while test_cases>0:
        row = input().strip().split()
        initial_board = tuple(int(num) for num in row)
        # print("Randomly generated puzzle:", initial_board)
        heuristic_choice = input("Select H Function: \n[1] H1\n[2] H2\n ").strip()
        heuristic_func = h1 if heuristic_choice == '1' else h2

        goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        initial_state = PuzzleState(initial_board, goal_state, 0, heuristic_func)

        max_depth = int(input("Enter Solution Depth (2-20): "))
        result, search_cost = astar_search(initial_state, heuristic_func, max_depth)
        if result:
            print_solution(result)
            print("Search Cost:", search_cost)
        else:
            print("No solution found")
            print("Search Cost:", search_cost)

        test_cases-=1

    
def main(): 
    while True:
        print("[1] Single Test Puzzle\n[2] Multi-Test Puzzle\n[3] Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            single_test_puzzle()
        elif choice == '2':
            multiple_test()
        elif choice == '3':
            break
    

if __name__ == "__main__":
    main()