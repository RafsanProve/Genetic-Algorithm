import math
import time
from functools import partial

from Evolution import run_evolution
from Population import generate_binary_population
from Crossover import single_point_crossover
from Mutation import bit_flip_mutation
from Selection import roulette_wheel_selection, roulette_wheel_selection_positive

GENOME_LENGTH = 20
RANGE_MIN = -10.0
RANGE_MAX = 31.0

def func1(x: float) -> float:
    return math.sin(10 * math.pi * x) * x + 2.0

def func2(x: float) -> float:
    # x=2, y= 10
    return -(x - 2)**2 + 10

def func3(x: float) -> float:
    return x*x


def decode_genome(genome: list[int]) -> float:
    binary_string = "".join(map(str, genome))
    decimal_value = int(binary_string, 2)

    max_decimal = 2**len(genome) - 1

    scaled_value = RANGE_MIN + (decimal_value / max_decimal) * (RANGE_MAX - RANGE_MIN)
    return scaled_value

def calculate_fitness(genome: list[int]) -> float:
    x = decode_genome(genome)
    return func2(x)


if __name__ == "__main__":

    start_time = time.time()

    population, generations = run_evolution(
        populate_func=partial(generate_binary_population, size=50, genome_length=GENOME_LENGTH),
        fitness_func=calculate_fitness,
        selection_func=roulette_wheel_selection_positive,
        crossover_func=single_point_crossover,
        mutation_func=partial(bit_flip_mutation, probability=0.05),
        fitness_limit=1000.0,
        generation_limit=200
    )

    end_time = time.time()

    best_genome = population[0]

    best_x = decode_genome(best_genome)
    max_y = calculate_fitness(best_genome)

    print(f"\nEvolution finished in {generations} generations.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Best solution found:")
    print(f"  - x value: {best_x:.6f}")
    print(f"  - Max y value: {max_y:.6f}")