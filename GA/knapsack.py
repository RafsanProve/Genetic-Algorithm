# knapsack.py
# This is the main executable file for solving the Knapsack problem.
# It imports the required components from the other modules.

from collections import namedtuple
from functools import partial
import time

# Import the core evolution engine
from evolution import run_evolution

# Import your desired methods from the modular files
from population import generate_binary_population
from selection import roulette_wheel_selection
from crossover import single_point_crossover
from mutation import bit_flip_mutation

# --- 1. Problem Definition ---

# Define a 'Thing' for the items we can put in the knapsack
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

# List of things to choose from
things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70),
    Thing('Mint', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Book', 300, 1000),
    Thing('Charger', 25, 150)
]

WEIGHT_LIMIT = 3000

# --- 2. Problem-Specific Functions ---

def fitness(genome: list[int], things: list[Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("Genome and things must be of the same length.")

    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0  # Penalize solutions that are too heavy

    return value


def genome_to_things(genome: list[int], things: list[Thing]) -> list[Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result.append(thing)
    return result


# --- 3. Main Execution Block ---

if __name__ == "__main__":
    start_time = time.time()

    # Run the evolution!
    # We use functools.partial to pre-fill the arguments of our functions.
    population, generations = run_evolution(
        populate_func=partial(generate_binary_population, size=10, genome_length=len(things)),
        fitness_func=partial(fitness, things=things, weight_limit=WEIGHT_LIMIT),
        fitness_limit=1310,  # Target value for the solution
        selection_func=roulette_wheel_selection,
        crossover_func=single_point_crossover,
        mutation_func=partial(bit_flip_mutation, num=1, probability=0.5),
        generation_limit=100
    )

    end_time = time.time()

    # Print the results
    best_genome = population[0]
    best_solution = genome_to_things(best_genome, things)
    best_fitness = fitness(best_genome, things, WEIGHT_LIMIT)
    total_weight = sum([thing.weight for thing in best_solution])

    print(f"Generations: {generations}")
    print(f"Time: {end_time - start_time}s")
    print(f"Best solution fitness: {best_fitness}")
    print(f"Best solution weight: {total_weight}/{WEIGHT_LIMIT}")
    print("Items in knapsack:")
    for item in best_solution:
        print(f"- {item.name} (Value: {item.value}, Weight: {item.weight})")

