# --- Day 14: Regolith Reservoir ---
import math
from time import sleep
import os
import matplotlib.pyplot as plt
import numpy as np

clear = lambda: os.system('clear')

TEST = {'file': 'input.test', 'debug': True, 'draw': {'show': True, 'animation': False, 'speed': 0.01}}
INPUT = {'file': 'input', 'debug': False, 'draw': {'show': True, 'animation': True, 'speed': 1e-10}}
CTX = INPUT
DEBUG = CTX['debug']

SOURCE_START_POINT = (500, 0)

T_AIR, T_ROCK, T_SAND, T_SOURCE = ' ', '\u2591', '\u03BF', '+'
A_AIR, A_ROCK, A_SAND, A_SOURCE = 0, 1, 2, 3

blockers = [T_ROCK, T_SAND]
fig, ax = plt.subplots()


def animate(cave, falling=(500, 0)):
    rocks, start, end, floor, sands, margin = cave.values()

    start_y = start[1]
    row_num = end[0] + 1 if floor == math.inf else floor + 1
    col_num = end[1] - start_y + 1 + margin * 2

    map = np.full((row_num, col_num), A_AIR)

    sy, sx = falling
    map[sx, sy - start_y + margin] = A_SOURCE

    for ry, rx in rocks:
        map[rx, ry - start_y + margin] = A_ROCK
    for sy, sx in sands:
        map[sx, sy - start_y + margin] = A_SAND

    if floor != math.inf:
        map[-1] = A_ROCK

    ax.clear()
    ax.set_title(f"Unit of sand: {len(sands) + 1}")
    ax.imshow(map)
    plt.pause(CTX['draw']['speed'])


def terminal_draw(cave, falling=(500, 0)):
    rocks, start, end, floor, sands, margin = cave.values()

    start_y = start[1]
    row_num = end[0] + 1 if floor == math.inf else floor + 1
    col_num = end[1] - start_y + 1 + margin * 2

    map = [[T_AIR] * col_num for _ in range(row_num)]

    sy, sx = falling
    map[sx][sy - start_y + margin] = T_SOURCE

    for ry, rx in rocks:
        map[rx][ry - start_y + margin] = T_ROCK
    for sy, sx in sands:
        map[sx][sy - start_y + margin] = T_SAND

    if floor != math.inf:
        map[-1] = [T_ROCK for _ in range(col_num)]

    sleep(0.1)
    clear()
    for idx, row in enumerate(map):
        print(idx, row)


def display_map(cave, falling=(500, 0)):
    if CTX['draw']['show']:
        if CTX['draw']['animation']:
            animate(cave, falling)
        else:
            terminal_draw(cave, falling)


def get_map():
    rocks = set()
    lines = open(CTX['file']).read().splitlines()
    paths = [[eval(s) for s in line.split(" -> ")] for line in lines]

    x_min, x_max = math.inf, 0
    y_min, y_max = math.inf, 0

    # sortedBy_x = sorted(itertools.chain(*paths))
    # x_min, x_max = [x for x,_ in sortedBy_x[::len(sortedBy_x)-1]]
    # sortedBy_y = sorted(sortedBy_x, key=lambda y: y[1])
    # y_min, y_max = [y for _,y in sortedBy_y[::len(sortedBy_y)-1]]

    for path in paths:
        if DEBUG: print(f'Path: {path}')
        prev_x, prev_y = path[0]
        for curr_x, curr_y in path[1:]:
            if prev_x == curr_x:
                x_min, x_max = min(x_min, curr_x), max(x_max, curr_x)
                for y in range(min(prev_y, curr_y), max(prev_y, curr_y) + 1):
                    rocks.add((curr_x, y))
                    y_min, y_max = min(y_min, y), max(y_max, y)
                    # print(f"adding rock ({curr_x},{y})")
            else:
                y_min, y_max = min(y_min, curr_y), max(y_max, curr_y)
                for x in range(min(prev_x, curr_x), max(prev_x, curr_x) + 1):
                    rocks.add((x, curr_y))
                    x_min, x_max = min(x_min, x), max(x_max, x)

            prev_x, prev_y = curr_x, curr_y

    if DEBUG:
        print(f'x_min, x_max: {x_min}, {x_max}')
        print(f'y_min, y_max: {y_min}, {y_max}')
        print('rocks\n', rocks)

    # swap x <> y
    return {'rocks': rocks, 'start': (0, x_min), 'end': (y_max, x_max), 'floor': y_max + 2}


def candidate_neighbours(cave, falling):
    rocks, _, _, floor, sands, _ = cave.values()
    x, y = falling
    for dy, dx in [(1, 0), (1, -1), (1, 1)]:
        n = x + dx, y + dy
        if not (n in rocks or n in sands or y + dy == floor):
            return n


def is_inside(cave, x, y):
    y_min, x_min = cave['start']
    y_max, x_max = cave['end']
    return x_min <= x <= x_max and y_min <= y <= y_max


def move_down(cave, falling, stop_falling_condition):
    while stop_falling_condition(cave, falling):
        n = candidate_neighbours(cave, falling)
        if n:
            falling = n
        else:
            cave['sands'].add(falling)
            break

        # Uncomment if you want to see the sand fall
        # display_map(cave, falling)

    return falling


def release_sand(cave, sand, falling_condition, releasing_condition):
    while True:
        last = move_down(cave, sand, falling_condition)
        if not releasing_condition(cave, last):
            break
        display_map(cave)


cave = get_map()


# PART 1
def part_1():
    cave['sands'] = set()
    cave['floor'] = math.inf
    cave['print_margin'] = 0 if CTX == TEST else 10

    falling_condition = lambda c, s: is_inside(c, *s)
    releasing_condition = falling_condition

    release_sand(cave, SOURCE_START_POINT, falling_condition, releasing_condition)
    print(f'PART 1 - Units of sand:', len(cave['sands']))
    # 808


# PART 2
def part_2():
    cave['sands'] = set()
    cave['print_margin'] = 10 if CTX == TEST else 150

    falling_condition = lambda _, s: True
    releasing_condition = lambda _, s: s[1] != 0

    release_sand(cave, SOURCE_START_POINT, falling_condition, releasing_condition)
    print(f'PART 2 - Units of sand:', len(cave['sands']))
    # 26625


part_1()
part_2()
