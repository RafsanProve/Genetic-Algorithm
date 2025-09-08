from math import sqrt
from functools import partial

from Evolution import Genome, Population, run_evolution
from NSGA import run_nsga2
from Population import generate_listed_permutation_population
from Selection import roulette_wheel_selection_positive, tournament_selection, rank_selection, nsga2_tournament_selection
from Crossover import davis_order_crossover
from Mutation import swap_mutation



def distance(point1: float, point2: float) -> float:
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def fitness(genome: Genome) -> float:
    total_distance = 0
    n = len(genome)
    for i in range(n):
        from_city = genome[i]
        to_city = genome[(i+1)%n]
        total_distance += distance_matrix[from_city][to_city]
    return 1 / (total_distance + 1e-6)

def fitness_turns(genome: Genome) -> float:
    turns = 0
    n = len(genome)
    for i in range(n):
        # A simple turn could be a change in direction
        p1 = cities[genome[i]]
        p2 = cities[genome[(i + 1) % n]]
        p3 = cities[genome[(i + 2) % n]]

        # This is a simplification; a more robust calculation would be needed
        if (p2[0] - p1[0]) * (p3[1] - p2[1]) != (p2[1] - p1[1]) * (p3[0] - p2[0]):
            turns += 1
    return 1 / (turns + 1e-6) # We want to maximize this (minimize turns)

# cities = {
#     "A": (0, 0),
#     "B": (1, 5),
#     "C": (3, 2),
#     "D": (7, 4),
#     "E": (10, 1),
#     "F": (6, 8),
#     "G": (8, 10)
# }

cities = {
    "A": (0, 0),  # City 0
    "B": (1, 5),  # City 1
    "C": (2, 0),  # City 2
    "D": (3, 5),  # City 3
    "E": (4, 0),  # City 4
    "F": (5, 5),  # City 5
    "G": (6, 0),  # City 6
    "H": (7, 5)   # City 7
}

# Create a list of city names
city_names = list(cities.keys())

# Create a distance matrix for easy lookup
distance_matrix = {}
for city1, coords1 in cities.items():
    distance_matrix[city1] = {}
    for city2, coords2 in cities.items():
        if city1 == city2:
            distance_matrix[city1][city2] = 0
        else:
            distance_matrix[city1][city2] = distance(coords1, coords2)

if __name__ == "__main__":
    final_solutions, generations = run_nsga2(
        populate_func=partial(generate_listed_permutation_population, size=10, list=city_names, genome_length=len(city_names)),
        fitness_funcs=[fitness, fitness_turns], # Pass both fitness functions
        selection_func=nsga2_tournament_selection, # Use the new selection function
        crossover_func=davis_order_crossover,
        mutation_func=swap_mutation,
        generation_limit=500,
    )

    print(f"Found {len(final_solutions)} non-dominated solutions:")
    print(f"{generations} Genetations:")
    for solution in final_solutions:
        print(f"Tour: {solution}, Distance: {1/fitness(solution)}, Turns: {1/fitness_turns(solution)}")

# if __name__ == "__main__":
#     tour = ['A', 'C', 'B', 'F', 'G', 'D', 'E']
#     # print(fitness(tour))

#     population, generation = run_evolution(
#         populate_func=partial(generate_listed_permutation_population, size=100, list=city_names, genome_length=7),
#         selection_func=roulette_wheel_selection_positive,
#         crossover_func=davis_order_crossover,
#         mutation_func=swap_mutation,
#         fitness_func=fitness,
#         fitness_limit=1,
#         generation_limit=1000,
#         dynamic_crossover_probability= dynamic_crossover_probability,
#         dynamic_mutation_probability= partial(dynamic_mutation_probabilty, k=0.1)
#     )

#     print(generation)
#     # for i in range(len(population[0])):
#     print(population[0])
#     print(fitness(population[0]))
