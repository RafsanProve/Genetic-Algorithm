from collections import namedtuple
from functools import partial
import time

from Evolution import Genome, run_evolution
from Population import generate_binary_population
from Selection import roulette_wheel_selection
from Crossover import single_point_crossover
from Mutation import bit_flip_mutation


Thing = namedtuple('Thing', ['name', 'value', 'weight']) # See namedtuple documentation for syntax


# FITNESS
# Calculate Fitness for given weight limit
def fitness(genome: Genome, things: list[Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("Genome and Things must have the same length.")

    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value

# Decodes a genome into a list of names of the selected things.
def genome_to_things(genome: Genome, things: list[Thing]) -> list[Thing]:
    result = []

    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing]

    return result



if __name__ == "__main__":
    things = [
        Thing('Laptop', 500, 2200),
        Thing('Headphones', 150, 160),
        Thing('Coffee Mug', 60, 350),
        Thing('Notepad', 40, 333),
        Thing('Water Bottle', 30, 192),
        Thing('Phone', 500, 200),
        Thing('Baseball Cap', 100, 70),
        Thing('Mint', 5, 25),
        Thing('Socks', 10, 38)
    ]

    # print(things[0])

    start_time = time.time()
    population, generation = run_evolution(
        populate_func= partial(generate_binary_population, size = 10, genome_length= len(things)),
        selection_func= roulette_wheel_selection,
        crossover_func= single_point_crossover,
        mutation_func= partial(bit_flip_mutation, num= 10, probability= 0.7),
        fitness_func= partial(fitness, things= things, weight_limit= 3000),
        fitness_limit= 1310, # The target value for the solution. The evolution will stop if this fitness is reached.
        generation_limit= 100
    )
    end_time = time.time()

    best_genome = population[0]

    best_solution = genome_to_things(best_genome, things)
    best_fitness = fitness(best_genome, things, 3000)
    total_weight = sum([thing.weight for thing in best_solution])

    print(f"\nGenerations: {generation}")
    print(f"Time: {end_time - start_time}s")
    print(f"Best solution fitness: {best_fitness}")
    print(f"Best solution weight: {total_weight}/{3000}")
    print("Items in knapsack:")
    for item in best_solution:
        print(f"- {item.name} (Value: {item.value}, Weight: {item.weight})")