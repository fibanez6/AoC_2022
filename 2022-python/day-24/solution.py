# --- Day 24: Blizzard Basin ---

import math
import queue
import itertools

import numpy as np

TEST = {'file': 'input.test2', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = TEST
DEBUG = CTX['debug']

N, S, W, E = (-1, 0), (1, 0), (0, -1), (0, 1)

# Remove borders
map = []
lines = open(CTX['file']).read().splitlines()
for row in lines[1:-1]:
    map.append(row[1:-1])

height = len(map)
width = len(map[0])

lcm = math.lcm(height, width)
print(f'height={height} width={width} lcm={lcm}')

# Cache the positions of blizzards at each point in time (they cycle after lcm(width,height) 
# then invert them to only include "open" positions
timelapse_map = {}
for i, j in itertools.product(range(height), range(width)):
    bliz_pos_time = set()

    for jt in range(width):
        bliz = map[i][jt]
        if bliz == '>':
            for k in range(lcm // width):
                bliz_pos_time.add(k * width + (j - jt) % width)
        elif bliz == '<':
            for k in range(lcm // width):
                bliz_pos_time.add(k * width + (jt - j) % width)

    for it in range(height):
        bliz = map[it][j]
        if bliz == 'v':
            for k in range(lcm // height):
                bliz_pos_time.add(k * height + (i - it) % height)
        elif bliz == '^':
            for k in range(lcm // height):
                bliz_pos_time.add(k * height + (it - i) % height)

    timelapse_map[(i, j)] = set(range(lcm)) - bliz_pos_time


def print_timelapse_map(timelapse_map, time, show_blizzards=False):
    map = np.array([['.'] * (width + 2) for _ in range(height + 2)])
    map[0:, 0] = '#'
    map[0, 0:] = '#'
    map[-1, :] = '#'
    map[:, -1] = '#'
    map[0, 1] = '.'
    map[-1, -2] = '.'

    for (x, y), times in timelapse_map.items():
        print_bliz = lambda show: time not in times if show else time in times
        if print_bliz(show_blizzards):
            map[x + 1, y + 1] = '@'

    np.savetxt("map.txt", map, fmt='%s')


def get_possible_elf_moves(elf, time):
    _time = (time + 1) % lcm

    if elf == start:
        moves = [elf, (0, 0)]
    elif elf == end:
        moves = [elf, (height - 1, width - 1)]
    else:
        moves = [elf]
        for (dx, dy) in [W, S, E, N]:
            _elf = (elf[0] + dx, elf[1] + dy)
            if 0 <= _elf[0] < height and 0 <= _elf[1] < width:
                moves.append(_elf)
        if elf == (0, 0):
            moves.append(start)
        elif elf == (height - 1, width - 1):
            moves.append(end)

    res = []
    for m in moves:
        if m in [start, end]:
            res.append((m, _time))
        elif _time in timelapse_map[m]:
            res.append((m, _time))
    return res


def bfs(start, end, start_time):
    root_node = (start, start_time)

    q = queue.Queue()
    q.put(root_node)

    cache = {root_node: 0}

    while q:
        curr_state = q.get()
        if DEBUG: print_timelapse_map(timelapse_map, curr_state[1])

        if curr_state[0] == end:
            return cache[curr_state]

        for n in get_possible_elf_moves(*curr_state):
            if n in cache:
                continue
            cache[n] = cache[curr_state] + 1
            q.put(n)


time = 0
start, end = (-1, 0), (height, width - 1)

# PART 1
print(f"From {start} to {end}")
steps = bfs(start, end, time)
time += steps
print(f"PART 1 - What is the fewest number of minutes to reach the goal? {time}")

# PART 2
print(f"From {end} to {start}")
steps = bfs(end, start, time)
time += steps
print(f"What is the fewest number of minutes required to reach the goal and go back? {time}")

print(f"From {start} to {end}")
steps = bfs(start, end, time)
time += steps
print(f"PART 2 - What is the fewest number of minutes required to reach the goal, go back, then goal again? {time}")
