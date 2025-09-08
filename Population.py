from random import choices, choice, randrange, sample

from Evolution import Genome, Population
from Data_Structure import ScheduledClass

# Creates a genome as a list of binary integers of length 'k'
# def <func_name>(<param_name>: <param_type>) -> <return_type> :
def generate_binary_genome(length: int) -> Genome: 
    return choices([0, 1], k=length)

# Create genome for given list of numbers
def generate_listed_genome(list: list, length: int) -> Genome:
    return choices(list, k=length)



# A List of Binary Genome
def generate_binary_population(size: int, genome_length: int) -> Population: 
    return [generate_binary_genome(genome_length) for _ in range(size)]

# A List of Genome for given list of acceptable gene value
def generate_listed_population(size: int, list: list, genome_length: int) -> Population:
    return [generate_listed_genome(list, genome_length) for _ in range(size)]

def generate_listed_permutation_population(size: int, list: list, genome_length: int) -> Population:
    return [sample(list, genome_length) for _ in range(size)]

# A List of 2D Binary Genome 
def generate_2d_population(size: int, rows: int, cols: int) -> Population:
    population = []
    for _ in range(size):
        # A genome is now a list of lists (a matrix)
        genome = [[choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        population.append(genome)
    return population



# --- TIME SCHEDULING ---
def generate_timetable_population(classes_to_schedule: list, rooms: list, time_slots: list, size: int) -> Population:
    """
    Generates an initial population of random timetables.
    """
    population = []
    for _ in range(size):
        genome = []
        for class_info in classes_to_schedule:
            # For each class, assign a random room and timeslot
            scheduled_class = ScheduledClass(
                course=class_info['course'],
                group=class_info['group'],
                room=choice(rooms),
                timeslot=choice(time_slots)
            )
            genome.append(scheduled_class)
        population.append(genome)
    return population

# --- Might Light ---
def generate_matrix(list: list, mat_size: int = 5) -> Genome:
    genome = []
    for _ in range(mat_size):
        genome.append(choices(list, k=mat_size))
    return genome

def generate_matrix_population(size: int, list: list, mat_size: int) -> Population:
    return [generate_matrix(list, mat_size) for _ in range(size)]


# --- N Queen ---
def generate_nqueen_board(size: int, rows: int, cols: int) -> Population:
    population = []
    for _ in range(size):
        genome = []
        for _ in range(rows):
            temp = []
            for _ in range(cols):
                temp.append(0)
            index = randrange(cols)
            temp[index] = 1
            genome.append(temp)
        population.append(genome)
    return population



if __name__ == "__main__":
    # population = generate_matrix_population(10, ['M', 'L', 'I', 'G', 'H', 'T', 'X'], 5)
    population = generate_nqueen_board(2, 8, 8)
    
    for i in range(len(population)):
        for j in range(len(population[i])):
            print(population[i][j])
        print("\n")

    