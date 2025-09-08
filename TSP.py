from math import sqrt
from functools import partial

from Evolution import Genome, Population, run_evolution
from Population import generate_listed_permutation_population
from Selection import roulette_wheel_selection_positive, tournament_selection, rank_selection
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


def dynamic_crossover_probability(a: Genome, b: Genome, population: Population , fitness: fitness) -> float:
    fitness_max = fitness(population[0])
    fitness_min = fitness(population[-1])
    if fitness_max == fitness_min:
        return 0.0
    
    fitness_a = fitness(a)
    fitness_b = fitness(b)

    probability = abs(fitness_a - fitness_b) / (fitness_max - fitness_min)

    return probability

def dynamic_mutation_probabilty(a: Genome, population: Population, fitness: fitness, k: float = 0.5) -> float:
    fitness_max = fitness(population[0])
    if fitness_max == 0:
        return 0.0
    probabilty = k*((fitness(a)/fitness_max)**2)
    return probabilty

cities = {
    "A": (0, 0),
    "B": (1, 5),
    "C": (3, 2),
    "D": (7, 4),
    "E": (10, 1),
    "F": (6, 8),
    "G": (8, 10)
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
    tour = ['A', 'C', 'B', 'F', 'G', 'D', 'E']
    # print(fitness(tour))

    population, generation = run_evolution(
        populate_func=partial(generate_listed_permutation_population, size=100, list=city_names, genome_length=7),
        selection_func=roulette_wheel_selection_positive,
        crossover_func=davis_order_crossover,
        mutation_func=swap_mutation,
        fitness_func=fitness,
        fitness_limit=1,
        generation_limit=1000,
        dynamic_crossover_probability= dynamic_crossover_probability,
        dynamic_mutation_probability= partial(dynamic_mutation_probabilty, k=0.1)
    )

    print(generation)
    # for i in range(len(population[0])):
    print(population[0])
    print(fitness(population[0]))
