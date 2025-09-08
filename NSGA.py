from typing import Callable, List, Tuple, Dict, TypeVar
from math import inf as INFINITE

Genome = TypeVar('Genome')
Population = List[Genome]

FitnessFunc = Callable[[Genome], float] 
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], List[Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome, int, float], Genome]

def dominates(a: Genome, b: Genome, fitness_funcs: List[FitnessFunc]) -> int:
    a_fitnesses = [func(a) for func in fitness_funcs]
    b_fitnesses = [func(b) for func in fitness_funcs]

    better = worse = False

    for fitness_a, fitness_b in zip(a_fitnesses, b_fitnesses):
        if fitness_a > fitness_b : # Maximising fitness, so if fitness of a>b for all fitness funcs, bthen a dominates b
            better = True
        elif fitness_a < fitness_b :
            worse = True

    if better and not worse:
        return 1
    elif worse and not better:
        return -1
    return 0


def non_dominated_sort(population: Population, fitness_funcs: List[FitnessFunc]) -> List[List[int]]:
    population_size = len(population)
    dominated_counts = [0]*population_size
    dominating_solutions = [[] for _ in range(population_size)]
    fronts = [[]]

    for i in range(population_size):
        for j in range(i+1, population_size):
            domination_result = dominates(population[i], population[j], fitness_funcs)

            if domination_result == 1:
                dominating_solutions[i].append(j)
                dominated_counts[j] += 1
            elif domination_result == -1:
                dominating_solutions[j].append(i)
                dominated_counts[i] += 1
        
        if dominated_counts[i] == 0:
            fronts[0].append(i)

    i = 0
    while i < len(fronts):
        next_front = []
        for p_index in fronts[i]:
            for q_index in dominating_solutions[p_index]:
                dominated_counts[q_index] -= 1
                if dominated_counts[q_index] == 0:
                    next_front.append(q_index)
        
        if next_front:
            fronts.append(next_front)
        i += 1
    
    return fronts


def crowding_distance(population: Population, fitness_funcs: List[FitnessFunc], front: List[int]) -> Dict[int, float]:
    distances = {i: 0.0 for i in front}

    for i in range(len(fitness_funcs)):
        sorted_front = sorted(front, key = lambda j: fitness_funcs[i](population[j]))
        distances[sorted_front[0]] = INFINITE
        distances[sorted_front[-1]] = INFINITE

        if len(sorted_front) > 2:
            min_fitness = fitness_funcs[i](population[sorted_front[0]])
            max_fitness = fitness_funcs[i](population[sorted_front[-1]])

            if max_fitness == min_fitness:
                continue

            for k in range(1, len(sorted_front) - 1):
                next_neighbour = fitness_funcs[i](population[sorted_front[k+1]])
                prev_neighbour = fitness_funcs[i](population[sorted_front[k-1]])

                next_prev_neighbour_diff = next_neighbour - prev_neighbour
                max_min_diff = max_fitness - min_fitness

                distances[sorted_front[k]] += next_prev_neighbour_diff / max_min_diff
    return distances

def run_nsga2(
        populate_func: PopulateFunc,
        fitness_funcs: List[FitnessFunc],
        selection_func: SelectionFunc,
        crossover_func: CrossoverFunc,
        mutation_func: MutationFunc,
        generation_limit: int = 100
) -> Population :
    
    population = populate_func()

    for generation in range(generation_limit):
        parent_fronts = non_dominated_sort(population, fitness_funcs)
        parent_crowding_distances = {}
        for front in parent_fronts:
            parent_crowding_distances.update(crowding_distance(population, fitness_funcs, front))

        offspring_population = []
        for _ in range(len(population) // 2):
            parents = selection_func(population, fitness_funcs, parent_fronts, parent_crowding_distances)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a, offspring_b = mutation_func(offspring_a), mutation_func(offspring_b)
            offspring_population += [offspring_a, offspring_b]

        combined_population = population + offspring_population
        fronts = non_dominated_sort(combined_population, fitness_funcs)

        next_generation = []
        for front in fronts:
            if len(next_generation) + len(front) <= len(population):
                next_generation.extend([combined_population[i] for i in front])
            else:
                distances = crowding_distance(combined_population, fitness_funcs, front)
                sorted_front = sorted(front, key=lambda i: distances[i], reverse=True)
                remaining_space = len(population) - len(next_generation)
                next_generation.extend([combined_population[i] for i in sorted_front[:remaining_space]])
                break
        
        population = next_generation

    # Final non-dominated sort to return the best solutions
    final_fronts = non_dominated_sort(population, fitness_funcs)
    return [population[i] for i in final_fronts[0]], generation