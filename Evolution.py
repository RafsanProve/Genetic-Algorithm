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


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: float,
        selection_func: SelectionFunc,
        crossover_func: CrossoverFunc,
        mutation_func: MutationFunc,
        generation_limit: int = 100,
        dynamic_crossover_probability: Optional[DynamicCrossoverRate] = None,
        dynamic_mutation_probability: Optional[DynamicMutationRate] = None
) -> Tuple[Population, int]:
    
    population = populate_func() # Calls the partial function with no param as all params are already in it

    for generation in range(generation_limit):
        population = sorted(population, key= lambda genome: fitness_func(genome), reverse=True) # Sorts population based on fitness in descending order

        # If the fitness is above the limit, No further iteration needed
        if fitness_func(population[0]) >= fitness_limit: # Here, fitness_func is a partial function that is working like Currying in Ruby
            break

        # Elitism
        next_generation = population[0:2]

        # Here, in each iteration we are creating 2 child. So in order to keep the population size same, we iterate half of the length of the population
        # As we are implementing Elitism, we are keeping 2 best genome from previous generation. So, to keep the population size same, we will generate 2 less children.
        # So, we will iterate one lesser time
        for _ in range(int(len(population) / 2) - 1): 
            parents = selection_func(population, fitness_func)

            # Static Crossover Probability
            # offspring_a, offspring_b = crossover_func(parents[0], parents[1])

            # Dynamic Crossover Probability
            if dynamic_crossover_probability:
                crossover_prob = dynamic_crossover_probability(parents[0], parents[1], population, fitness_func)
                offspring_a, offspring_b = crossover_func(parents[0], parents[1], crossover_prob)
            else:
                offspring_a, offspring_b = crossover_func(parents[0], parents[1])

            # Static Mutation Probability
            # offspring_a = mutation_func(offspring_a)
            # offspring_b = mutation_func(offspring_b)

            # Dynamic Mutation Probability
            if dynamic_mutation_probability:
                mutation_prob_a = dynamic_mutation_probability(offspring_a, population, fitness_func)
                mutation_prob_b = dynamic_mutation_probability(offspring_b, population, fitness_func)
                offspring_a = mutation_func(offspring_a, probability= mutation_prob_a)
                offspring_b = mutation_func(offspring_b, probability= mutation_prob_b)
            else:
                offspring_a = mutation_func(offspring_a)
                offspring_b = mutation_func(offspring_b)

            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(population, key= lambda genome: fitness_func(genome), reverse=True)

    return population, generation # generation is the number of iteration that executed