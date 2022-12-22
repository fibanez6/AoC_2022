import itertools
import math
import timeit
import re

import numpy as np

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

# def profiler(method):
#     def wrapper_method(*arg, **kw):
#         start = timeit.default_timer()
#         ret = method(*arg, **kw)
#         time = "{0:2.9f}".format(timeit.default_timer() - start)
#         print(f'{method.__name__} took : {time} sec')
#         return ret
# 
#     return wrapper_method

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
DIRECTION = {'R': 1, 'L': -1}

FACING = [RIGHT, DOWN, LEFT, UP]
tiles = []
walls = []
out_map = set()

lines = open(CTX['file']).read().splitlines()

max_row = 0
max_col = 0

sq = 50

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


def move(elf, times):
    # elf = [(9, 8), 0]
    # max_col = 12
    # max_row = 16
    
    if FACING[elf[1]] == RIGHT:
        for t in range(times):
            next_facing = elf[1]
            next_block = (elf[0][0], elf[0][1] + 1)
            if next_block in out_map or next_block[1] > max_row:
                x_sq = (next_block[0] - 1) % max_col // sq
                if x_sq == 0:  # from 2 to 5 (face left)
                    x = 2 * sq + sq - (elf[0][0] - 1) % sq
                    y = 2 * sq
                    next_block = (x, y)
                    next_facing = LEFT
                elif x_sq == 1:  # from 3 to 2 (face up)
                    x = sq
                    y = 2 * sq + 1 + (elf[0][0] - 1) % sq
                    next_block = (x, y)
                    next_facing = UP
                elif x_sq == 2:  # from 5 to 2 (face left)
                    x = sq - (elf[0][0] - 1) % sq
                    y = 3 * sq
                    next_block = (x, y)
                    next_facing = LEFT
                elif x_sq == 3:  # from 6 to 5 (face up)
                    x = 3 * sq
                    y = sq + 1 + (elf[0][0] - 1) % sq
                    next_block = (x, y)
                    next_facing = UP

                if next_block not in walls:
                    elf[0] = next_block
                    elf[1] = next_facing
                    move(elf, times - (t + 1))
                    break

            if next_block not in walls:
                elf[0] = next_block
                elf[1] = next_facing
            else:
                break
    elif FACING[elf[1]] == LEFT:
        for t in range(times):
            next_facing = elf[1]
            next_block = (elf[0][0], elf[0][1] - 1)
            if next_block in out_map or next_block[1] < 1:
                x_sq = (next_block[0] - 1) % max_col // sq
                if x_sq == 0:  # from 1 to 4 (face right)
                    x = 2 * sq + sq - (elf[0][0] - 1) % sq
                    y = 1
                    next_block = (x, y)
                    next_facing = RIGHT
                elif x_sq == 1:  # from 3 to 4 (face down)
                    x = 2 * sq + 1
                    y = 1 + (elf[0][0] - 1) % sq
                    next_block = (x, y)
                    next_facing = DOWN
                elif x_sq == 2:  # from 4 to 1 (face right)
                    x = sq - (elf[0][0] - 1) % sq
                    y = sq + 1
                    next_block = (x, y)
                    next_facing = UP
                elif x_sq == 3:  # from 6 to 1 (face down)
                    x = 1
                    y = sq + 1 + (elf[0][0] - 1) % sq
                    next_block = (x, y)
                    next_facing = DOWN

                if next_block not in walls:
                    elf[0] = next_block
                    elf[1] = next_facing
                    move(elf, times - (t + 1))
                    break

            if next_block not in walls:
                elf[0] = next_block
                elf[1] = next_facing
            else:
                break
    elif FACING[elf[1]] == DOWN:
        for t in range(times):
            next_facing = elf[1]
            next_block = (elf[0][0] + 1, elf[0][1])
            if next_block in out_map or next_block[0] > max_col:
                y_sq = (next_block[1] - 1) % max_row // sq
                if y_sq == 0:  # from 6 to 2 (face Down)
                    x = 1
                    y = sq + 1 + (elf[0][1] - 1) % sq
                    next_block = (x, y)
                    next_facing = DOWN
                elif y_sq == 1:  # from 5 to 6 (face left)
                    x = 3 * sq + 1 + (elf[0][1] - 1) % sq
                    y = sq
                    next_block = (x, y)
                    next_facing = LEFT
                elif y_sq == 2:  # from 2 to 3 (face left)
                    x = sq + 1 + (elf[0][1] - 1) % sq
                    y = 2 * sq
                    next_block = (x, y)
                    next_facing = LEFT
                

                if next_block not in walls:
                    elf[0] = next_block
                    elf[1] = next_facing
                    move(elf, times - (t + 1))
                    break

            if next_block not in walls:
                elf[0] = next_block
                elf[1] = next_facing
            else:
                break
    elif FACING[elf[1]] == UP:
        for t in range(times):
            next_facing = elf[1]
            next_block = (elf[0][0] - 1, elf[0][1])
            if next_block in out_map or next_block[0] < 1:
                y_sq = (next_block[1] - 1) % max_row // sq
                if y_sq == 0:  # from 4 to 3 (face right)
                    x = sq + 1 + (elf[0][1] - 1) % sq
                    y = sq + 1
                    next_block = (x, y)
                    next_facing = RIGHT
                elif y_sq == 1:  # from 1 to 6 (face right)
                    x = 3 * sq + 1 + (elf[0][1] - 1) % sq
                    y = 1
                    next_block = (x, y)
                    next_facing = RIGHT
                elif y_sq == 2:  # from 2 to 6 (face up)
                    x = 4 * sq
                    y = 1 + (elf[0][1] - 1) % sq
                    next_block = (x, y)
                    next_facing = UP
                

                if next_block not in walls:
                    elf[0] = next_block
                    elf[1] = next_facing
                    move(elf, times - (t + 1))
                    break

            if next_block not in walls:
                elf[0] = next_block
                elf[1] = next_facing
            else:
                break


def turn(elf, direccion):
    if direccion == 'R':
        elf[1] = (elf[1] + 1) % 4
    else:
        elf[1] = (elf[1] - 1) % 4


elf = [tiles[0], 0]
for p in re.split(r'(\d+)', lines[-1]):
    print_map(elf)
    print(elf)

    # if elf[0][0] == 107 and elf[0][1] == 43:
    # if elf[0][0] == 107 and elf[0][1] :
    #     print()

    if len(p) == 0:
        continue
    if p.isdigit():
        move(elf, int(p))
    else:
        turn(elf, p)

print(f' elf {elf}  key = ', 1000 * elf[0][0] + 4 * elf[0][1] + elf[1])


# @profiler
def part_1():
    print(f'PART 1 - ?')
    # 11037 - 0.060878667 sec


# @profiler
def part_2():
    print(f'PART 2 - ?')
    # 3033720253914 - 0.909982583 sec


print(f'Running PART 1')
part_1()

# print(f'Running PART 2')
# part_2()
