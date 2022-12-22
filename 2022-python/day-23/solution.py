# --- Day 23: Unstable Diffusion ---

import math
import timeit

import numpy as np

TEST = {'file': 'input.test2', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

NW, N, NE = (-1, -1), (-1, 0), (-1, 1)
SW, S, SE = (1, -1), (1, 0), (1, 1)
W, E = (0, -1), (0, 1)

N_NE_NW = [N, NW, NE]
S_SE_SW = [S, SW, SE]
W_NW_SW = [W, NW, SW]
E_NE_SE = [E, NE, SE]

ADJACENTS = [NW, N, NE, SW, S, SE, W, E]
DIRECTIONS = [N_NE_NW, S_SE_SW, W_NW_SW, E_NE_SE]

elfs = set()

lines = open(CTX['file']).read().splitlines()
for xi, row in enumerate(lines):
    for yi, el in enumerate(row):
        if el == '#':
            elfs.add((xi, yi))


def print_map(elfs):
    min_x, max_x, min_y, max_y = get_min_max(elfs)

    map = np.array([['.'] * (max_y - min_y) for _ in range(max_x - min_x)])
    for x, y in elfs:
        map[x, y] = '#'
    np.savetxt("map.txt", map, fmt='%s')


def get_min_max(elfs):
    min_x, max_x = math.inf, -math.inf
    min_y, max_y = math.inf, -math.inf

    for x, y in elfs:
        min_x, max_x = min(min_x, x), max(max_x, x + 1)
        min_y, max_y = min(min_y, y), max(max_y, y + 1)

    return min_x, max_x, min_y, max_y


def get_positions(x, y, n):
    return [(x + nx, y + ny) for nx, ny in n]


start = timeit.default_timer()

round = 0
while True:
    round += 1
    proposals = {}
    if DEBUG: print_map(elfs)

    #  1st round
    for elf_idx, elf in enumerate(elfs):
        if not any(x in elfs for x in get_positions(*elf, ADJACENTS)):
            continue

        for i in range(4):
            d = DIRECTIONS[(round - 1 + i) % 4]
            if not any(x in elfs for x in get_positions(*elf, d)):
                p = (elf[0] + d[0][0], elf[1] + d[0][1])
                proposals[p] = elf if p not in proposals else None
                break

    #  2nd round
    if not proposals:
        break

    for prop, elf in proposals.items():
        if elf:
            elfs.remove(elf)
            elfs.add(prop)

    if round == 10:
        min_x, max_x, min_y, max_y = get_min_max(elfs)
        tiles = (max_x - min_x) * (max_y - min_y) - len(elfs)
        print(f'PART 1 - How many empty ground tiles does that rectangle contain? {tiles}')
        # 3940
        time = "{0:2.9f}".format(timeit.default_timer() - start)
        print(f'Took : {time} sec')

print(f'PART 2 - What is the number of the first round where no Elf moves? {round}')
# 990
time = "{0:2.9f}".format(timeit.default_timer() - start)
print(f'Took : {time} sec')
