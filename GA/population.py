from random import choices
from typing import List
from evolution import Genome, Population

def generate_binary_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_binary_population(size: int, genome_length: int) -> Population:
    return [generate_binary_genome(genome_length) for _ in range(size)]