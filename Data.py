from Data_Structure import *

# --- KNAPSACK ---




# --- TIME SCHEDULING ---

TEACHERS = [
    Teacher(0, "Prof. Smith"), 
    Teacher(1, "Dr. Jones"), 
    Teacher(2, "Ms. Davis")
]
ROOMS = [
    Room(0, "R101", 30), 
    Room(1, "R102", 25), 
    Room(2, "Lab A", 35)
]
COURSES = [
    Course(0, "Computer Science 101", 0), # Taught by Prof. Smith
    Course(1, "Mathematics 203", 1),      # Taught by Dr. Jones
    Course(2, "Physics 101", 0),          # Taught by Prof. Smith
    Course(3, "Chemistry Lab", 2),        # Taught by Ms. Davis
    Course(4, "Advanced Math", 1)         # Taught by Dr. Jones
]
GROUPS = [
    Group(0, "CS Year 1", 28, [0, 2, 3]), # This group takes CS, Physics, and Chem Lab
    Group(1, "Math Year 2", 20, [1, 4])   # This group takes both math courses
]
TIME_SLOTS = [
    TimeSlot(0, "Mon", "09:00"),
    TimeSlot(1, "Mon", "11:00"),
    TimeSlot(2, "Tue", "09:00"), 
    TimeSlot(3, "Tue", "11:00"),
    TimeSlot(4, "Wed", "10:00")
]