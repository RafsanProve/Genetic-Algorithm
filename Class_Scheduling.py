import time
from functools import partial

# Import the core evolution engine and necessary operators
from Evolution import run_evolution
from Population import generate_timetable_population # We will create this
from Selection import roulette_wheel_selection
from Crossover import uniform_crossover # This is perfect for our needs
from Mutation import timetable_mutation # We will create this

# --- 1. DEFINE THE DATA STRUCTURES ---
from Data_Structure import ScheduledClass

# --- 2. DEFINE THE PROBLEM DATASET ---
from Data import TEACHERS, ROOMS, COURSES, GROUPS, TIME_SLOTS



# --- 3. THE FITNESS FUNCTION ---

def calculate_fitness(genome: list[ScheduledClass]) -> float:
    """
    Calculates the fitness of a timetable genome using a penalty system.
    The lower the penalty, the higher the fitness.
    """
    penalty = 0

    # --- Hard Constraint Penalties (High Value) ---
    HARD_PENALTY = 1000

    # Group classes by timeslot for efficient clash detection
    schedule_by_slot = {}
    for scheduled_class in genome:
        slot_id = scheduled_class.timeslot.id
        if slot_id not in schedule_by_slot:
            schedule_by_slot[slot_id] = []
        schedule_by_slot[slot_id].append(scheduled_class)

    for slot_id, classes_in_slot in schedule_by_slot.items():
        # Check for clashes within each timeslot
        teachers_in_slot = [c.course.teacher_id for c in classes_in_slot]
        rooms_in_slot = [c.room.id for c in classes_in_slot]
        groups_in_slot = [c.group.id for c in classes_in_slot]

        # Teacher clash: more than one unique teacher means a clash
        if len(set(teachers_in_slot)) != len(teachers_in_slot):
            penalty += HARD_PENALTY

        # Room clash
        if len(set(rooms_in_slot)) != len(rooms_in_slot):
            penalty += HARD_PENALTY

        # Student Group clash
        if len(set(groups_in_slot)) != len(groups_in_slot):
            penalty += HARD_PENALTY

    # Check for room capacity issues
    for scheduled_class in genome:
        if scheduled_class.room.capacity < scheduled_class.group.size:
            penalty += HARD_PENALTY

    # --- Soft Constraint Penalties (Lower Value) ---
    SOFT_PENALTY = 10

    # Example: Penalize classes on Wednesday (maybe it's a sports day)
    for scheduled_class in genome:
        if scheduled_class.timeslot.day == "Wed":
            penalty += SOFT_PENALTY

    # The goal is to evolve a solution where penalty is 0, or as low as possible.
    # We invert the score because the evolution engine maximizes fitness.
    # The '+1' avoids division by zero if the penalty is 0.
    return 1.0 / (1.0 + penalty)


def print_timetable(genome: list[ScheduledClass]):
    """Helper function to print the timetable in a readable format."""
    print("\n--- Generated Timetable ---")
    sorted_genome = sorted(genome, key=lambda c: (c.timeslot.day, c.timeslot.time, c.room.name))
    for s_class in sorted_genome:
        print(
            f"[{s_class.timeslot.day} {s_class.timeslot.time}] "
            f"Room: {s_class.room.name} | "
            f"Course: {s_class.course.name} | "
            f"Group: {s_class.group.name} | "
            f"Teacher: {TEACHERS[s_class.course.teacher_id].name}"
        )
    print(f"Fitness Score: {calculate_fitness(genome):.4f}")


# --- 4. MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    # First, determine all class assignments that need to be scheduled
    classes_to_schedule = []
    for group in GROUPS:
        for course_id in group.course_ids:
            course = next(c for c in COURSES if c.id == course_id)
            classes_to_schedule.append({'course': course, 'group': group})

    start_time = time.time()

    # Run the evolution!
    population, generations = run_evolution(
        populate_func=partial(generate_timetable_population, classes_to_schedule=classes_to_schedule, rooms=ROOMS, time_slots=TIME_SLOTS, size=50), # Larger population for a complex problem 
        fitness_func=calculate_fitness,
        fitness_limit=1.0, # Aim for a perfect score (0 penalty)
        selection_func=roulette_wheel_selection, # From your existing selection.py
        crossover_func=uniform_crossover, # From your existing crossover.py
        mutation_func=partial(timetable_mutation, rooms=ROOMS, time_slots=TIME_SLOTS,probability=0.2), # Higher mutation probability can be good here
        generation_limit=500
    )

    end_time = time.time()

    print(f"\nEvolution finished in {generations} generations.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    # Print the best solution found
    best_timetable = population[0]
    print_timetable(best_timetable)
