from functools import partial

from Evolution import Genome, run_evolution
from Population import generate_matrix_population
from Selection import roulette_wheel_selection, random_selection, rank_selection
from Crossover import single_point_crossover, uniform_crossover_2d
from Mutation import random_resetting, random_resetting_2d, swap_mutation

def fitness(genome: Genome) -> int:
    score = 0

    for i in range(5):
        for j in range(5):
            if i == 0 and (j == 0 or j == 4):
                if (genome[i][0] == 'M' and genome[i][4] == 'L') or (genome[i][0] == 'L' and genome[i][4] == 'M'):
                    score += 1
                # else:
                #     return -1
            elif i == 1 and (j == 1 or j == 3):
                if genome[i][j] == 'I':
                    score += 1
                # else:
                #     return -1
            elif i == 2 and j == 2:
                if genome[i][j] == 'G':
                    score += 1
                # else:
                #     return -1
            elif i == 3 and (j == 1 or j == 3):
                if genome[i][j] == 'H':
                    score += 1
                # else:
                #     return -1
            elif i == 4 and (j == 0 or j == 4):
                if genome[i][j] == 'T':
                    score += 1
                # else:
                #     return -1
            elif genome[i][j] == 'X':
                score += 1
            # else:
            #     return -1
                
    return score



if __name__ == "__main__":
    final_matrix = [
        ['L', 'X', 'X', 'X', 'M'],
        ['X', 'I', 'X', 'I', 'X'],
        ['X', 'X', 'G', 'X', 'X'],
        ['X', 'H', 'X', 'H', 'X'],
        ['T', 'X', 'X', 'X', 'T']
    ]

    chars = ['M', 'L', 'I', 'G', 'H', 'T', 'X']

    population, generation = run_evolution(
        populate_func= partial(generate_matrix_population, size= 100, list = chars, mat_size = 5),
        selection_func= rank_selection,
        crossover_func= uniform_crossover_2d,
        mutation_func= partial(random_resetting_2d, allowed_values= chars),
        fitness_func= partial(fitness),
        fitness_limit= 25,
        generation_limit= 1000
    )

    print(generation)
    print(fitness(population[0]))
    for i in range(len(population[0])):
        print(population[0][i])
