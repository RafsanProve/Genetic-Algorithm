# evolution.py
# This file contains the core, problem-agnostic genetic algorithm engine.

from typing import List, Callable, Tuple, TypeVar

# Generic type variables to make the functions more flexible.
# Now, a Genome can be a list of anything, not just ints.
Genome = TypeVar('Genome')
Population = List[Genome]

# Redefining the function signatures with the generic Genome type.
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc,
        crossover_func: CrossoverFunc,
        mutation_func: MutationFunc,
        generation_limit: int = 100
) -> Tuple[Population, int]:
    """
    Runs the genetic algorithm.

    Args:
        populate_func: Function to generate the initial population.
        fitness_func: Function to calculate the fitness of a genome.
        fitness_limit: The target fitness value to stop evolution.
        selection_func: Function to select two parents from the population.
        crossover_func: Function to perform crossover on two parents.
        mutation_func: Function to mutate a genome.
        generation_limit: The maximum number of generations to run.

    Returns:
        A tuple containing the final population sorted by fitness and the
        number of generations it took.
    """
    population = populate_func()

    for generation in range(generation_limit):
        # Sort the population by fitness in descending order.
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        # If the best solution has reached the fitness limit, stop.
        if fitness_func(population[0]) >= fitness_limit:
            break

        # Keep the top 2 solutions for the next generation (elitism).
        next_generation = population[0:2]

        # Generate the rest of the new population through breeding.
        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    # Final sort of the last generation.
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, generation
