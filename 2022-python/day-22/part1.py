# --- Day 22: Monkey Map ---

import re
import numpy as np

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']


RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
DIRECTION = {'R': 1, 'L': -1}

FACING = [RIGHT, DOWN, LEFT, UP]
tiles = []
walls = []
out_map = set()

lines = open(CTX['file']).read().splitlines()

max_row = 0
max_col = 0

elf_path = set()


def print_map(elf):
    a = np.array([[' '] * (max_row + 1) for _ in range(max_col + 1)])

    for t in tiles:
        a[t[0] - 1, t[1] - 1] = '.'
    for w in walls:
        a[w[0] - 1, w[1] - 1] = '#'

    elf_path.add((elf[0], elf[1]))
    for e in elf_path:
        a[e[0][0] - 1, e[0][1] - 1] = str(e[1])

    np.savetxt("map.txt", a, fmt='%s')

    return a


for x, row in enumerate(lines, start=1):
    if len(row) == 0:
        max_col = x - 1
        break
    max_row = max(max_row, len(row))
    for y, el in enumerate(row, start=1):
        if el == '.':
            tiles.append((x, y))
        elif el == '#':
            walls.append((x, y))
        else:
            out_map.add((x, y))


def find_left(x, y):
    for yi in range(1, max_row):
        if (x, yi) not in out_map:
            return (x, yi)
    return (x, y)


def find_right(x, y):
    for yi in range(max_row, 1, -1):
        if (x, yi) not in out_map:
            return (x, yi)
    return (x, y)


def find_up(x, y):
    for xi in range(1, max_col):
        if (xi, y) not in out_map:
            return (xi, y)
    return (x, y)


def find_down(x, y):
    for xi in range(max_col, 1, -1):
        if (xi, y) not in out_map:
            return (xi, y)
    return (x, y)


def move(elf, times):
    if FACING[elf[1]] == RIGHT:
        for _ in range(times):
            next_block = (elf[0][0], elf[0][1] + 1)
            if next_block in out_map:
                next_block = find_left(*elf[0])
            if next_block[1] > max_row:
                next_block = find_left(*elf[0])
            if next_block not in walls:
                elf[0] = next_block
            else:
                break
    elif FACING[elf[1]] == LEFT:
        for _ in range(times):
            next_block = (elf[0][0], elf[0][1] - 1)
            if next_block in out_map:
                next_block = find_right(*elf[0])
            if next_block[1] < 1:
                next_block = find_right(*elf[0])
            if next_block not in walls:
                elf[0] = next_block
            else:
                break
    elif FACING[elf[1]] == DOWN:
        for _ in range(times):
            next_block = (elf[0][0] + 1, elf[0][1])
            if next_block in out_map:
                next_block = find_up(*elf[0])
            if next_block[0] > max_col:
                next_block = find_up(*elf[0])
            if next_block not in walls:
                elf[0] = next_block
            else:
                break
    elif FACING[elf[1]] == UP:
        for _ in range(times):
            next_block = (elf[0][0] - 1, elf[0][1])
            if next_block in out_map:
                next_block = find_down(*elf[0])
            if next_block[0] < 1:
                next_block = find_down(*elf[0])
            if next_block not in walls:
                elf[0] = next_block
            else:
                break


def turn(elf, dir):
    if dir == 'R':
        elf[1] = (elf[1] + 1) % 4
    else:
        elf[1] = (elf[1] - 1) % 4


elf = [tiles[0], 0]
for p in re.findall('\d+|[LR]', lines[-1]):
    if DEBUG: print_map(elf)
    if p.isdigit():
        move(elf, int(p))
    else:
        turn(elf, p)

print(f'PART 1 - What is the final password?', 1000 * elf[0][0] + 4 * elf[0][1] + elf[1])
# 20494
