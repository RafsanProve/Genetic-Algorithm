# population.py
# Contains functions for generating genomes and populations.
# Now supports seeding the population with known good genomes.

from random import choices
from typing import List, Optional
from evolution import Genome, Population

def generate_binary_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_binary_population(size: int, genome_length: int, seed_genomes: Optional[List[Genome]] = None) -> Population:
    """
    Generates a population of binary genomes.

    If seed_genomes is provided, they will be included in the initial
    population, giving the algorithm a head start.
    """
    population = []
    if seed_genomes:
        population += seed_genomes

    # Fill the rest of the population with random genomes
    remaining_size = size - len(population)
    for _ in range(remaining_size):
        population.append(generate_binary_genome(genome_length))

    return population
