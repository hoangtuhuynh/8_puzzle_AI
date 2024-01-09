import random
import time
import numpy as np


def print_board(board):
    """ Display the board in a readable format. """
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print("\n")

def random_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def compute_heuristic(board):
    h = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                h += 1
    return h

def get_neighbors(board):
    neighbors = []
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i] != j:
                new_board = list(board)
                new_board[i] = j
                neighbors.append(new_board)
    return neighbors

def steepest_ascent_hill_climbing(board):
    current_board = board
    search_cost = 0
    while True:
        current_heuristic = compute_heuristic(current_board)
        neighbors = get_neighbors(current_board)
        search_cost += len(neighbors)
        next_board = None
        next_heuristic = float('inf')

        for neighbor in neighbors:
            h = compute_heuristic(neighbor)
            if h < next_heuristic:
                next_board = neighbor
                next_heuristic = h

        if next_heuristic >= current_heuristic:
            break

        current_board = next_board

    return current_board, search_cost

# Genetic Algorithm Functions
def initialize_population(pop_size, n):
    return [random_board(n) for _ in range(pop_size)]

def fitness(board, max_heuristic):
    return max_heuristic - compute_heuristic(board)

def random_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    return population[np.random.choice(len(population), p=selection_probs)]

def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[:c] + y[c:]

def mutate(board):
    n = len(board)
    i = random.randint(0, n - 1)
    board[i] = random.randint(0, n - 1)
    return board

def genetic_algorithm(pop_size, n, generations):
    population = initialize_population(pop_size, n)
    max_heuristic = (n * (n - 1)) // 2
    search_cost = 0

    for generation in range(generations):
        new_population = []
        fitnesses = [fitness(individual, max_heuristic) for individual in population]
        search_cost += len(population)

        for _ in range(len(population)):
            x = random_selection(population, fitnesses)
            y = random_selection(population, fitnesses)
            child = reproduce(x, y)
            if random.random() < 0.1:
                child = mutate(child)
            new_population.append(child)

        population = new_population

        best_individual = max(population, key=lambda ind: fitness(ind, max_heuristic))
        if compute_heuristic(best_individual) == 0:
            return best_individual, search_cost

    return max(population, key=lambda ind: fitness(ind, max_heuristic)), search_cost

# Running the algorithm on one instance 
def run_single_instance_experiment(n, pop_size, generations):
    initial_board = random_board(n)
    print("Initial Board:")
    print_board(initial_board)

    # Steepest-Ascent Hill Climbing
    start_time = time.time()
    final_board_hc, search_cost_hc = steepest_ascent_hill_climbing(initial_board)
    hc_time = time.time() - start_time
    print("Final Board (Steepest-Ascent Hill Climbing):")
    print_board(final_board_hc)
    print(f"Time Taken: {hc_time} seconds")
    print(f"Search Cost: {search_cost_hc}\n")

     # Genetic Algorithm
    start_time = time.time()
    final_board_ga, search_cost_ga = genetic_algorithm(pop_size, n, generations)
    ga_time = time.time() - start_time
    final_heuristic_ga = compute_heuristic(final_board_ga)

    print("Final Board (Genetic Algorithm):")
    print_board(final_board_ga)
    print(f"Time Taken: {ga_time} seconds")
    print(f"Search Cost: {search_cost_ga}")

    if final_heuristic_ga == 0:
        print("The GA final board is a solution.")
    else:
        print("The GA final board is not a solution.")
    print("\n")

# Running the algorithms on multiple instances
def run_experiments(n, num_instances, pop_size, generations):
    hill_climbing_success = 0
    ga_success = 0
    hc_search_costs = 0
    ga_search_costs = 0
    hc_time = 0
    ga_time = 0

    for _ in range(num_instances):
        initial_board = random_board(n)

        # Hill Climbing
        start_time = time.time()
        final_board_hc, search_cost_hc = steepest_ascent_hill_climbing(initial_board)
        hc_time += time.time() - start_time
        hc_search_costs += search_cost_hc
        if compute_heuristic(final_board_hc) == 0:
            hill_climbing_success += 1

        # Genetic Algorithm
        start_time = time.time()
        final_board_ga, search_cost_ga = genetic_algorithm(pop_size, n, generations)
        ga_time += time.time() - start_time
        ga_search_costs += search_cost_ga
        if compute_heuristic(final_board_ga) == 0:
            ga_success += 1

    return {
        'HC_Success_Rate': hill_climbing_success / num_instances * 100,
        'GA_Success_Rate': ga_success / num_instances * 100,
        'HC_Avg_Search_Cost': hc_search_costs / num_instances,
        'GA_Avg_Search_Cost': ga_search_costs / num_instances,
        'HC_Avg_Time': hc_time / num_instances,
        'GA_Avg_Time': ga_time / num_instances
    }

def main():
    # Parameters
    n = 8  # Size of the board (8x8) 
    pop_size = 100  # Population size for GA
    generations = 100  # Number of generations for GA

    print("Welcome to N-Queen Problem")
    choose = int(input("[1] To run one instance\n[2] to run multiple instances\n"))
    if choose == 1:
        # Run single instance experiment
        run_single_instance_experiment(n, pop_size, generations)
    # Run experiments
    else:
        num_instances = int(input("Number of instances: ")) # Number of instances to run
        results = run_experiments(n, num_instances, pop_size, generations)
        print("Experiment Results:", results)

if __name__ == '__main__':
    main()

