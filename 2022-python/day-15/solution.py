# --- Day 15: Beacon Exclusion Zone ---

import math
import os
import re
import timeit
from z3 import If, Int, Solver, And

start = timeit.default_timer()

clear = lambda: os.system('clear')

TEST = {'file': 'input.test', 'debug': True, 'Y': 10, 'limit': 20}
INPUT = {'file': 'input', 'debug': False, 'Y': 2_000_000, 'limit': 4_000_000}
CTX = INPUT
DEBUG = CTX['debug']

################### 
# PRINT MAP HELPERS
###################
BEACON, SENSOR, EMPTY, MARK = 'B', 'S', ' ', '#'
min_x, max_x = math.inf, -math.inf
min_y, max_y = math.inf, -math.inf
max_md = -math.inf


def print_map(map):
    for idx, row in enumerate(map):
        print(idx, row)


def fill_map(signals):
    for (sx, sy), (bx, by) in signals:
        map[sy][sx + margin_x] = SENSOR
        map[by][bx + margin_x] = BEACON


def highlight_map(x, y, margin_x):
    if (el := map[y][x + margin_x]) in [BEACON, SENSOR]:
        map[y][x + margin_x] = "[" + el + "]"


def add_mark_map(mx, my, margin_x):
    if map[my][mx + margin_x] == EMPTY:
        map[my][mx + margin_x] = MARK
    else:
        highlight_map(mx, my, margin_x)


###################
# SOLUTION
###################

# manhattan_distance = |x2 - x1| + |y2 - y1|
def distance(a, b):
    return sum(abs(v1 - v2) for v1, v2 in zip(a, b))


signals = []
lines = open(CTX['file']).read().splitlines()
for line in lines:
    vals = [int(n) for n in re.findall(r'-?\d+', line)]
    sensor = (vals[0], vals[1])
    beacon = (vals[2], vals[3])
    signals.append([sensor, beacon])

    # TO PRINT MAP
    max_md = max(max_md, distance(beacon, sensor))
    min_x = min(min_x, min(sensor[0], beacon[0]))
    max_x = max(max_x, max(sensor[0], beacon[0]))
    min_y = min(min_y, min(sensor[1], beacon[1]))
    max_y = max(max_y, max(sensor[1], beacon[1]))

map = []
if DEBUG:
    map = [[EMPTY] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    margin_x = 0 if min_x >= 0 else -min_x
    fill_map(signals)


# PART 1
def part_1():
    """
    Coverage of all sensors near the row (y)
    """
    beacons = set()
    marks = set()
    for sensor, beacon in signals:
        radio = distance(sensor, beacon)

        beacons.add(beacon)

        y = CTX['Y']
        # Height/vertical points within the circumference (radio == distance) as sensor as its center
        for x in range(sensor[0] - radio, sensor[0] + radio + 1):
            if distance(sensor, (x, y)) <= radio:
                # Inside the search area
                marks.add((x, y))
                if DEBUG:
                    add_mark_map(x, y, margin_x)
                    highlight_map(*sensor, margin_x)

    if DEBUG: print_map(map)
    print(f'PART 1 - how many positions cannot contain a beacon?', len(marks - beacons))
    # 6124805


# PART 2
def z3abs(x):
    return If(x >= 0, x, -x)


def part_2():
    min_limit = 0
    max_limit = CTX['limit']

    s = Solver()
    x = Int("x")
    y = Int("y")
    s.add(And(min_limit <= x, x <= max_limit))
    s.add(And(min_limit <= y, y <= max_limit))

    for sensor, beacon in signals:
        dist = distance(sensor, beacon)
        s.add(z3abs(x - sensor[0]) + z3abs(y - sensor[1]) > dist)

    s.check()
    m = s.model()
    print(f'Beacon found at ({m[x].as_long()},{m[y].as_long()})')
    print('PART 2 - What is its tuning frequency?', m[x].as_long() * 4_000_000 + m[y].as_long())
    # 12555527364986


part_1()
part_2()

stop = timeit.default_timer()
print(f'Time: {stop - start} secs')

"""
PART 1 Sample solution:
7 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '[S]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '[S]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
8 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
9 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
10 ['#', '#', '#', '#', '[B]', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ']
11 [' ', ' ', '[S]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
12 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
13 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
14 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '[S]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '[S]', ' ', ' ', ' ', ' ', ' ']
"""
