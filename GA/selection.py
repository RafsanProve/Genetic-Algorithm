from random import choices
from typing import List, Tuple
from evolution import Genome, Population, FitnessFunc

def roulette_wheel_selection(population: Population, fitness_func: FitnessFunc) -> Tuple[Genome, Genome]:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )