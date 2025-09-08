from collections import namedtuple

# --- KNAPSACK ---



# --- TIME SCHEDULING ---

# Basic entities for our university
Room = namedtuple('Room', ['id', 'name', 'capacity'])
Teacher = namedtuple('Teacher', ['id', 'name'])
Course = namedtuple('Course', ['id', 'name', 'teacher_id'])
Group = namedtuple('Group', ['id', 'name', 'size', 'course_ids'])
TimeSlot = namedtuple('TimeSlot', ['id', 'day', 'time'])

# A single scheduled class, which will be our "Gene"
ScheduledClass = namedtuple('ScheduledClass', ['course', 'group', 'room', 'timeslot'])