# Knapsack Problem

from collections import namedtuple
from functools import partial
from random import choices, randint, random, randrange
import time
from typing import Callable, List, Tuple

# Genome == Chromosome
Genome  = List[int]
Population = List[Genome]
Thing = namedtuple('Thing', ['name', 'value', 'weight']) # See namedtuple documentation for syntax

# typing.Callable create a user defined callable type like function, method etc.
# Callable[[<param_types>], <ret_type>]
# We will partially implement the function with rest of the parameters except 'Genome'. Then just call the FitnessFunc with appropriate genome param to get the result.
FitnessFunc = Callable[[Genome], int] 
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], List[Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome, int, float], Genome]


# Creates a genome as a list of binary integers of length 'k'
# def <func_name>(<param_name>: <param_type>) -> <return_type> :
def generate_genome(length: int) -> Genome: 
    return choices([0, 1], k=length)


# A List of Chromosome
def generate_population(size: int, genome_length: int) -> Population: 
    return [generate_genome(genome_length) for _ in range(size)]

# FITNESS
# Calculate Fitness for given weight limit
def fitness(genome: Genome, things: list[Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("Genome and Things must have the same length.")

    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value

# SELECTION
# Select a Pair from the Population to use as Parent for next Generation
def selection_pair(population: Population, fitness_fuc: FitnessFunc) -> list[Genome]:
    return choices(
        population=population,
        weights=[fitness_fuc(genome) for genome in population], # Fitness value as weight
        k=2 # Return 2 genome as list
    )

# CROSSOVER
# Selects a single random point from both parent genome, cuts the genomes, swaps the portions and return the new childs as a tuple 
def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomees of Both Parents must have same length.")
    
    length = len(a)
    if length < 2:
        return a, b # Returns a Tuple of Tuple[a, b]

    p = randint(1, length-1) # Single Random Point

    # 1st-> a(0 to p-1)+b(p to rest) , 2nd-> b(0 to p-1)+a(p to rest)
    return a[0:p] + b[p:], b[0:p] + a[p:]

# MUTATION
# Flipping a bit with a probability
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
                    # <value_if_true> if (<condition>) else <value_if_false>
        genome[index] = genome[index] if random() > probability else (genome[index] ^ 1)

    return genome

def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100
                                    ) -> Tuple[Population, int]:
    
    population = populate_func() # Calls the partial function with no param as all params are already in it

    for generation in range(generation_limit):
        population = sorted(population, key= lambda genome: fitness_func(genome), reverse=True) # Sorts population based on fitness in descending order

        if fitness_func(population[0]) >= fitness_limit: # Here, fitness_func is a partial function that is working like Currying in Ruby
            break

        next_generation = population[0:2]

        for _ in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(population, key= lambda genome: fitness_func(genome), reverse=True)

    return population, generation

# Decodes a genome into a list of names of the selected things.
def genome_to_things(genome: Genome, things: list[Thing]) -> list[Thing]:
    result = []

    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]

    return result




things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70),
    Thing('Mint', 5, 25),
    Thing('Socks', 10, 38)
]

# print(things[0])

start_time = time.time()
population, generation = run_evolution(
    populate_func= partial(generate_population, size = 10, genome_length= len(things)),
    selection_func= selection_pair,
    # crossover_func= single_point_crossover,
    # mutation_func= partial(mutation, num= 10, probability= 0.7),
    fitness_func= partial(fitness, things= things, weight_limit= 3000),
    fitness_limit= 1310, # The target value for the solution. The evolution will stop if this fitness is reached.
    generation_limit= 100
)
end_time = time.time()

print(f"Number of generations: {generation}")
print(f"Time : {end_time - start_time}")
print(f"Best Solution: {genome_to_things(genome=population[0], things= things)}")