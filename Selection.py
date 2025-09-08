from random import choices, choice
from typing import List, Dict

from Evolution import Genome, Population, FitnessFunc


# SELECTION
# Select a Pair from the Population to use as Parent for next Generation
# Genome with higher fitness has higher chance to be selected
def roulette_wheel_selection(population: Population, fitness_func: FitnessFunc) -> list[Genome]:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population], # Fitness value as weight
        k=2 # Return 2 genome as list
    )

def roulette_wheel_selection_positive(population: Population, fitness_func: FitnessFunc) -> list[Genome]:
    fitness_scores = [fitness_func(genome) for genome in population]

    min_fitness = min(fitness_scores)
    if min_fitness < 0:
        shifted_scores = [score - min_fitness + 1 for score in fitness_scores]
    else:
        shifted_scores = fitness_scores

    total_weight = sum(shifted_scores)
    if total_weight == 0:
        return choices(population=population, k=2)

    return choices(
        population=population,
        weights=shifted_scores,
        k=2
    )

# All genome are sorted based on their fitness
def rank_selection(population: Population, fitness_func: FitnessFunc) -> list[Genome]:
    new_population = sorted(population, key= lambda genome: fitness_func(genome), reverse=True)
    rank = sorted(list(range(1, len(population)+1)), reverse=True)
    # print(rank)

    return choices(
        population=new_population,
        weights=rank, # Fitness value as weight
        k=2 # Return 2 genome as list
    )


# All genome has same weight
def random_selection(population: Population, fitness_func: FitnessFunc) -> list[Genome]:
    return choices(
        population=population,
        k=2 # Return 2 genome as list
    )

# Play a tournament and select 2 genome
def tournament_selection(population: Population, fitness_func: FitnessFunc, candidates: int = 2) -> list[Genome]:
    match1 = choices(population=population, k=candidates)
    parent1 = max(match1, key= fitness_func)

    match2 = choices(population=population, k=candidates)
    parent2 = max(match2, key= fitness_func)

    return [parent1, parent2]


def nsga2_tournament_selection(population: Population, fitness_funcs: List[FitnessFunc], fronts: List[List[int]], crowding_distances: Dict[int, float]) -> List[Genome]:
    
    def is_better(p_index, q_index):
        # Find which front each individual is in
        p_front = next((i for i, front in enumerate(fronts) if p_index in front))
        q_front = next((i for i, front in enumerate(fronts) if q_index in front))
        
        # If they are in different fronts, the one in the lower front is better
        if p_front < q_front:
            return True
        elif q_front < p_front:
            return False
        
        # If they are in the same front, the one with the larger crowding distance is better
        if crowding_distances[p_index] > crowding_distances[q_index]:
            return True
        return False

    # Perform two tournaments to select two parents
    parents = []
    for _ in range(2):
        candidate1_idx, candidate2_idx = choices(range(len(population)), k=2)
        
        if is_better(candidate1_idx, candidate2_idx):
            parents.append(population[candidate1_idx])
        else:
            parents.append(population[candidate2_idx])
            
    return parents

def crowded_tournament_selection(population: Population, fronts: List[List[int]], distances: Dict[int, float]) -> Genome:
    # Get index of two random individuals
    i, j = choice(range(len(population))), choice(range(len(population)))

    # Find which front each individual is in
    # This is a bit inefficient, a reverse mapping would be faster
    i_front = next(k for k, front in enumerate(fronts) if i in front)
    j_front = next(k for k, front in enumerate(fronts) if j in front)

    # The individual in the better (lower) front wins
    if i_front < j_front:
        return population[i]
    elif j_front < i_front:
        return population[j]
    
    # If they are in the same front, the one with greater crowding distance wins
    if distances[i] > distances[j]:
        return population[i]
    else:
        return population[j]