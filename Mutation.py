from random import random, randrange, choice, shuffle

from Evolution import Genome


# MUTATION
# Flipping a bit with a probability
def bit_flip_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index = randrange(len(genome))
                        # <value_if_true> if (<condition>) else <value_if_false>
            # genome[index] = genome[index] if random() > probability else (genome[index] ^ 1)
            genome[index] ^= 1

    return genome

def bit_flip_mutation_2d(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index1 = randrange(len(genome))
            index2 = randrange(len(genome))
                        # <value_if_true> if (<condition>) else <value_if_false>
            # genome[index] = genome[index] if random() > probability else (genome[index] ^ 1)
            genome[index1][index2] ^= 1

    return genome

# Randomly assign value from an acceptable list
def random_resetting(genome: Genome, allowed_values: list, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index = randrange(len(genome))
            # print(index)
                        # <value_if_true> if (<condition>) else <value_if_false>
            # genome[index] = genome[index] if random() > probability else (genome[index] ^ 1)
            genome[index] = allowed_values[randrange(len(allowed_values))]

    return genome

def random_resetting_2d(genome: Genome, allowed_values: list, num: int = 1, probability: float = 0.05) -> Genome:
    rows, cols = len(genome), len(genome[0])
    for _ in range(num):
        for i in range(rows):
            for j in range(cols):
                if random() < probability:
                    genome[i][j] = choice(allowed_values)
    return genome

# Swap 2 random element from a Genome
def swap_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index1 = randrange(len(genome))
            index2 = randrange(len(genome))

            genome[index1], genome[index2] = genome[index2], genome[index1]

    return genome

def swap_mutation_2d(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index11 = randrange(len(genome))
            index12 = randrange(len(genome))
            index21 = randrange(len(genome))
            index22 = randrange(len(genome))

            genome[index11][index12], genome[index21][index22] = genome[index21][index22], genome[index11][index12]

    return genome

def scramble_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index1 = randrange(len(genome))
            index2 = randrange(len(genome))
            
            if(index1>index2):
                index1, index2 = index2, index1

            print(index1, index2)
            sub_genome = genome[index1:index2+1]
            shuffle(sub_genome)
            genome[index1:index2+1] = sub_genome
            print(genome)

    return genome

# Inverse a sub section and set it in the genome
def inverse_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        if random() <= probability:
            index1 = randrange(len(genome))
            index2 = randrange(len(genome))
            
            if(index1>index2):
                index1, index2 = index2, index1

            print(index1, index2)
            reversed_sublist = genome[index1:index2+1][::-1]
            genome[index1:index2+1] = reversed_sublist

    return genome


            




def timetable_mutation(genome: Genome, rooms: list, time_slots: list, probability: float = 0.1) -> Genome:
    """
    Mutates a timetable by randomly re-assigning a class's room or timeslot.
    """
    if random() > probability:
        return genome # No mutation

    # Select a random class in the timetable to mutate
    index = randrange(len(genome))
    scheduled_class = genome[index]

    # Flip a coin to decide whether to change the room or the timeslot
    if random() < 0.5:
        # Change the room
        new_room = choice(rooms)
        genome[index] = scheduled_class._replace(room=new_room)
    else:
        # Change the timeslot
        new_timeslot = choice(time_slots)
        genome[index] = scheduled_class._replace(timeslot=new_timeslot)

    return genome 

if __name__ == "__main__":
    # from Population import generate_binary_genome, generate_listed_genome

    # test1 = generate_binary_genome(10)
    # test2 = generate_binary_genome(10)

    test1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # test2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    # test1 = [1, 2, 3, 4, 5, 6, 7, 8]
    test2 = [8, 6, 4, 2, 7, 5, 3, 1]

    # test1 = generate_listed_genome(list= list(range(1, 20)), length=20)
    # test2 = generate_listed_genome(list= list(range(1, 20)), length=20)

    print(random_resetting(test1, test2))