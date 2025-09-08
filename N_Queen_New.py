from functools import partial

from Evolution import Genome, run_evolution
from Population import generate_listed_population, generate_listed_permutation_population
from Selection import roulette_wheel_selection, tournament_selection
from Crossover import single_point_crossover, multi_point_crossover, davis_order_crossover, uniform_crossover
from Mutation import random_resetting, swap_mutation

def fitness(genome: Genome) -> int:
    n = len(genome)
    score = (n*(n-1)) // 2

    for i in range(n):
        for j in range(i+1, n):
            if genome[i] == genome[j]:
                score -= 1
            if abs(i-j) == abs(genome[i]-genome[j]):
                score -= 1
    return score

if __name__ == "__main__":

    final_board = [5,3,6,0,7,1,4,2]

    # print(fitness(final_board))

    population, generation = run_evolution(
        populate_func= partial(generate_listed_permutation_population, list= list(range(0, 8)), size= 100, genome_length= 8),
        selection_func= tournament_selection,
        crossover_func= davis_order_crossover,
        # crossover_func= partial(multi_point_crossover, points= 3),
        mutation_func= swap_mutation,
        # mutation_func= partial(random_resetting, allowed_values= list(range(1, 8))),
        fitness_func= fitness,
        fitness_limit= 28,
        generation_limit= 2000
    )

    print(generation)
    print(fitness(population[0]))
    print(population[0])