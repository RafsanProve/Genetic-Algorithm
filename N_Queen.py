from functools import partial

from typing import Tuple
from Evolution import Genome, run_evolution
from Population import generate_2d_population, generate_nqueen_board
from Selection import roulette_wheel_selection, rank_selection
from Crossover import single_point_crossover, uniform_crossover_2d
from Mutation import bit_flip_mutation_2d,swap_mutation_2d

def fitness(genome: Genome) -> int:
    N = len(genome)
    score = (N * (N - 1)) // 2  
    queens = []

    for i in range(len(genome)):
        for j in range(len(genome[i])):
            if genome[i][j] == 1:
                queens.append((i, j))

    # Ensure there are exactly N queens for a valid calculation
    if len(queens) != N:
        return 0 # Or handle as an invalid genome

    clashes = 0
    # Iterate through all unique pairs of queens
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            q1 = queens[i]
            q2 = queens[j]

            check_row = q1[0] == q2[0]
            check_col = q1[1] == q2[1]
            check_dia = abs(q1[0] - q2[0]) == abs(q1[1] - q2[1])

            # Check for attacks
            if check_row or check_col or check_dia:
                clashes += 1
    
    return score - clashes



if __name__ == "__main__":

    final_board = [
        [0,0,0,0,0,1,0,0],
        [0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,1,0],
        [1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0],
        [0,0,1,0,0,0,0,0],
    ]

    # print(fitness(final_board))

    population, generation = run_evolution(
        populate_func= partial(generate_nqueen_board, size= 100, rows= 8, cols= 8),
        selection_func= roulette_wheel_selection,
        crossover_func= uniform_crossover_2d,
        mutation_func= partial(swap_mutation_2d, num= 20, probability= 0.7),
        fitness_func= fitness,
        fitness_limit= 28,
        generation_limit= 1000
    )

    print(generation)
    print(fitness(population[0]))
    for i in range(len(population[0])):
        print(population[0][i], ',')