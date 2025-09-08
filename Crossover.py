from random import randint, random, sample
from typing import Tuple

from Evolution import Genome


# CROSSOVER
# Selects a single random point from both parent genome, cuts the genomes, swaps the portions and return the new childs as a tuple 
def single_point_crossover(a: Genome, b: Genome, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomees of Both Parents must have same length.")
    
    length = len(a)
    if length < 2:
        return a, b # Returns a Tuple of Tuple[a, b]

    if random() <= probability:
        p = randint(1, length-1) # Single Random Point

        # 1st-> a(0 to p-1)+b(p to rest) , 2nd-> b(0 to p-1)+a(p to rest)
        return a[0:p] + b[p:], b[0:p] + a[p:]
    else:
        return a, b

def multi_point_crossover(a: Genome, b: Genome, points: int, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomes of Both Parents must have same length.")
    
    length = len(a)
    if length < 2:
        return a, b
    
    if points >= length:
        raise ValueError("Number of crossover points must be less than genome length.")

    if random() <= probability:
        p = random.sample(range(1, length), points)
        p.append(length)
        p.sort()

        # print(p)

        child_a = []
        child_b = []
        flag = True
        i = 0
        for j in p:
            if flag:
                child_a += a[i:j]
                child_b += b[i:j]
                i = j
                flag = False
            else:
                child_a += b[i:j]
                child_b += a[i:j]
                i = j
                flag = True
        
        return child_a, child_b
    else:
        return a, b

def uniform_crossover(a: Genome, b: Genome, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomees of Both Parents must have same length.")
    
    length = len(a)
    if length < 2:
        return a, b # Returns a Tuple of Tuple[a, b]

    if random() <= probability:
        child_a = []
        child_b = []
    
        for i in range(length):
            flag = randint(0,1)
            if flag:
                child_a.append(a[i])
                child_b.append(b[i])
            else:
                child_a.append(b[i])
                child_b.append(a[i])
        
        return child_a, child_b
    else:
        return a, b

def uniform_crossover_2d(a: Genome, b: Genome, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Genomes must have the same dimensions.")

    if random() <= probability:
        rows, cols = len(a), len(a[0])
        child_a = [([0] * cols) for _ in range(rows)]
        child_b = [([0] * cols) for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                flag = randint(0,1)
                if flag:
                    child_a[i][j] = a[i][j]
                    child_b[i][j] = b[i][j]
                else:
                    child_a[i][j] = b[i][j]
                    child_b[i][j] = a[i][j]

        return child_a, child_b
    else:
        return a, b

def whole_arithmetic_recombination(a: Genome, b: Genome, alpha: float, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomees of Both Parents must have same length.")
    
    if not (0 <= alpha <= 1):
        raise ValueError("Alpha must be between 0 and 1.")

    
    length = len(a)
    if length < 2:
        return a, b # Returns a Tuple of Tuple[a, b]
    
    if random() <= probability:
        child_a = []
        child_b = []
        
        for i in range(length):
            child_a.append( (alpha * a[i]) + ((1-alpha) * b[i]) )
            child_b.append( (alpha * b[i]) + ((1-alpha) * a[i]) )

        return child_a, child_b
    else:
        return a, b


def is_permutation(a: Genome, b: Genome) -> bool:
    return sorted(a) == sorted(b) and len(set(a)) == len(a) == len(b)


def davis_order_crossover(a: Genome, b: Genome, probability: float = 0.5) -> Tuple[Genome, Genome]:
    if len(a)!=len(b):
        raise ValueError("Genomees of Both Parents must have same length.")
    
    length = len(a)
    if length < 2:
        return a, b # Returns a Tuple of Tuple[a, b]
    
    if not is_permutation(a, b):
        raise ValueError("Genomes must be valid permutations with unique and identical elements.")
    
    if random() <= probability:
        child_a = []
        child_b = []

        p = sample(range(1, length), 2)
        p.sort()
        # print(p)

        # Copy the slice from each parent
        swap_seg_a = a[p[0]:p[1]+1]
        swap_seg_b = b[p[0]:p[1]+1]

        # Remaining items not in the copied segments
        remaining_seg_a = [i for i in b if i not in swap_seg_a]
        remaining_seg_b = [i for i in a if i not in swap_seg_b]

        # Construct children
        child_a = remaining_seg_a[:p[0]] + swap_seg_a + remaining_seg_a[p[0]:]
        child_b = remaining_seg_b[:p[0]] + swap_seg_b + remaining_seg_b[p[0]:]

        return child_a, child_b
    else:
        return a, b


if __name__ == "__main__":
    # from Population import generate_binary_genome, generate_listed_genome

    # test1 = generate_binary_genome(10)
    # test2 = generate_binary_genome(10)

    # test1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # test2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    test1 = [1, 2, 3, 4, 5, 6, 7, 8]
    test2 = [8, 6, 4, 2, 7, 5, 3, 1]

    # test1 = generate_listed_genome(list= list(range(1, 20)), length=20)
    # test2 = generate_listed_genome(list= list(range(1, 20)), length=20)


    # child_a, child_b = single_point_crossover(test1, test2)
    # child_a, child_b = multi_point_crossover(test1, test2, 4)
    # child_a, child_b = uniform_crossover(test1, test2)
    # child_a, child_b = whole_arithmetic_recombination(test1, test2, 0.3)
    child_a, child_b = davis_order_crossover(test1, test2)


    print(test1, test2)
    print(child_a, child_b)