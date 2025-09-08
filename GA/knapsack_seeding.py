from collections import namedtuple
from functools import partial
import time
import json  

from evolution import run_evolution
from population_seeding import generate_binary_population
from selection import roulette_wheel_selection
from crossover import single_point_crossover
from mutation import bit_flip_mutation

# --- 1. Problem Definition ---

Thing = namedtuple('Thing', ['name', 'value', 'weight'])
SEED_FILE = "Knapsack_best_genome.json"

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70),
    Thing('Mint', 5, 25),
    Thing('Tissues', 15, 80),
    Thing('Socks', 10, 38),
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
                return 0
    return value


def genome_to_things(genome: list[int], things: list[Thing]) -> list[Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result.append(thing)
    return result


# --- 3. Main Execution Block ---

if __name__ == "__main__":
    #Load Seed Genome
    loaded_seed_genomes = None
    try:
        with open(SEED_FILE, 'r') as f:
            # We load the genome and wrap it in a list
            loaded_seed_genomes = [json.load(f)]
        print(f"Successfully loaded seed genome from {SEED_FILE}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid seed file found. Starting with a random population.")

    start_time = time.time()
    
    population, generations = run_evolution(
        populate_func=partial(generate_binary_population, size=10, genome_length=len(things), seed_genomes=loaded_seed_genomes),  # Pass the loaded seed here!
        fitness_func=partial(fitness, things=things, weight_limit=WEIGHT_LIMIT),
        fitness_limit=1310,
        selection_func=roulette_wheel_selection,
        crossover_func=single_point_crossover,
        mutation_func=partial(bit_flip_mutation, num=1, probability=0.5),
        generation_limit=100
    )

    end_time = time.time()

    # Best Solution
    best_genome = population[0]

    # Save the Best Genome for the Next Run 
    with open(SEED_FILE, 'w') as f:
        json.dump(best_genome, f)
    print(f"Saved best genome to {SEED_FILE} for future runs.")

    best_solution = genome_to_things(best_genome, things)
    best_fitness = fitness(best_genome, things, WEIGHT_LIMIT)
    total_weight = sum([thing.weight for thing in best_solution])

    print(f"\nGenerations: {generations}")
    print(f"Time: {end_time - start_time}s")
    print(f"Best solution fitness: {best_fitness}")
    print(f"Best solution weight: {total_weight}/{WEIGHT_LIMIT}")
    print("Items in knapsack:")
    for item in best_solution:
        print(f"- {item.name} (Value: {item.value}, Weight: {item.weight})")
