from typing import Callable, List, Optional, Tuple, TypeVar


# Genome == Chromosome
# Genome = List[int]
# This allows a Genome to be a list of ints, a 2D list, a list of objects, etc.
Genome = TypeVar('Genome')
Population = List[Genome]

# typing.Callable create a user defined callable type like function, method etc.
# Callable[[<param_types>], <ret_type>]
# We will partially implement the function with rest of the parameters except 'Genome'. Then just call the FitnessFunc with appropriate genome param to get the result.
FitnessFunc = Callable[[Genome], float] 
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], List[Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome, int, float], Genome]
DynamicCrossoverRate = Callable[[Genome, Genome, Population, FitnessFunc], float]
DynamicMutationRate = Callable[[Genome, Population, FitnessFunc], float]


def expansion_replacement(old_population: Population, offspring_population: Population, fitness_func: FitnessFunc) -> Population:
    # Combines old and new generatios, then returns the top N fittest individuals.
    combined = old_population + offspring_population
    combined = sorted(combined, key=fitness_func, reverse=True)
    return combined[:len(old_population)]

def steady_state_replacement(sorted_population: Population, offspring_population: Population) -> Population:
    # Replaces the worst genome from the old generation with the new offspring
    num_to_replace = len(offspring_population)
    # The best individuals from the old generation survive
    survivors = sorted_population[:-num_to_replace]
    
    return survivors + offspring_population


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: float,
        selection_func: SelectionFunc,
        crossover_func: CrossoverFunc,
        mutation_func: MutationFunc,
        generation_limit: int = 100,
        dynamic_crossover_probability: Optional[DynamicCrossoverRate] = None,
        dynamic_mutation_probability: Optional[DynamicMutationRate] = None,
        replacement_strategy: str = 'elitism',
        steady_state_offspring: int = 2 
) -> Tuple[Population, int]:
    
    population = populate_func() # Calls the partial function with no param as all params are already in it

    for generation in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if fitness_func(population[0]) >= fitness_limit:
            break
        
        # Number of offspring pairs for Replacement Strategy
        if replacement_strategy == 'elitism':
            num_offspring_pairs = int(len(population) / 2) - 1
        elif replacement_strategy in ['expansion', 'full_generational']:
            num_offspring_pairs = int(len(population) / 2)
        elif replacement_strategy == 'steady_state':
            # Ensure an even number of offspring for steady state
            if steady_state_offspring % 2 != 0:
                raise ValueError("steady_state_offspring must be an even number.")
            num_offspring_pairs = int(steady_state_offspring / 2)
        else:
            raise ValueError(f"Unknown replacement strategy: {replacement_strategy}")

        # Offspring
        offspring_population = []
        for _ in range(num_offspring_pairs):
            parents = selection_func(population, fitness_func)

            if dynamic_crossover_probability:
                crossover_prob = dynamic_crossover_probability(parents[0], parents[1], population, fitness_func)
                offspring_a, offspring_b = crossover_func(parents[0], parents[1], crossover_prob)
            else:
                offspring_a, offspring_b = crossover_func(parents[0], parents[1])

            if dynamic_mutation_probability:
                mutation_prob_a = dynamic_mutation_probability(offspring_a, population, fitness_func)
                mutation_prob_b = dynamic_mutation_probability(offspring_b, population, fitness_func)
                offspring_a = mutation_func(offspring_a, probability=mutation_prob_a)
                offspring_b = mutation_func(offspring_b, probability=mutation_prob_b)
            else:
                offspring_a = mutation_func(offspring_a)
                offspring_b = mutation_func(offspring_b)

            offspring_population += [offspring_a, offspring_b]

        # Replacment Strategy to create the next generation
        if replacement_strategy == 'elitism':
            population = population[0:2] + offspring_population
        elif replacement_strategy == 'expansion':
            population = expansion_replacement(population, offspring_population, fitness_func)
        elif replacement_strategy == 'full_generational':
            population = offspring_population
        elif replacement_strategy == 'steady_state':
            population = steady_state_replacement(population, offspring_population)
    
    population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

    return population, generation # generation is the number of iteration that executed