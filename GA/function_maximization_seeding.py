import json
import math
import time
from functools import partial

# Import the core evolution engine and REUSE operators from the knapsack problem
from evolution import run_evolution
from population_seeding import generate_binary_population
from crossover import single_point_crossover
from mutation import bit_flip_mutation
from selection import roulette_wheel_selection

# --- 1. PROBLEM DEFINITION ---

# Define the search space and precision
# A longer genome gives higher precision
GENOME_LENGTH = 40
RANGE_MIN = -5.0
RANGE_MAX = 5.0

SEED_FILE = "Function_Maximization_best_genome.json"

def func(x: float) -> float:
    return math.sin(10 * math.pi * x) * x + 2.0

# --- 2. DECODING AND FITNESS FUNCTIONS ---

def decode_genome(genome: list[int]) -> float:
    """Decodes a binary genome into a decimal number within our defined range."""
    # Convert binary list to an integer
    binary_string = "".join(map(str, genome))
    decimal_value = int(binary_string, 2)

    # Calculate the maximum possible decimal value for the given genome length
    max_decimal = 2**len(genome) - 1

    # Scale the decimal value to our desired range
    scaled_value = RANGE_MIN + (decimal_value / max_decimal) * (RANGE_MAX - RANGE_MIN)
    return scaled_value

def calculate_fitness(genome: list[int]) -> float:
    x = decode_genome(genome)
    return func(x)

# --- 3. MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    
    #Load Seed Genome
    loaded_seed_genomes = None
    try:
        with open(SEED_FILE, 'r') as file:
            # We load the genome and wrap it in a list
            loaded_seed_genomes = [json.load(file)]
        print(f"Successfully loaded seed genome from {SEED_FILE}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid seed file found. Starting with a random population.")


    start_time = time.time()

    # Run the evolution!
    population, generations = run_evolution(
        populate_func=partial(generate_binary_population, size=50, genome_length=GENOME_LENGTH, seed_genomes= loaded_seed_genomes),
        fitness_func=calculate_fitness,
        fitness_limit=7.0, # A theoretical high value to aim for
        selection_func=roulette_wheel_selection,
        crossover_func=single_point_crossover,
        mutation_func=partial(bit_flip_mutation, probability=0.05),
        generation_limit=200
    )

    end_time = time.time()

    best_genome = population[0]

    # Save the Best Genome for the Next Run 
    with open(SEED_FILE, 'w') as f:
        json.dump(best_genome, f)
    print(f"Saved best genome to {SEED_FILE} for future runs.")
    

    best_x = decode_genome(best_genome)
    max_y = calculate_fitness(best_genome)

    print(f"\nEvolution finished in {generations} generations.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Best solution found:")
    print(f"  - x value: {best_x:.6f}")
    print(f"  - Max y value: {max_y:.6f}")
