# --- Day 9: Rope Bridge ---

import numpy as np

TEST = {'file': 'input.test', 'debug': True, 'map_size': (6, 6)}
INPUT = {'file': 'input', 'debug': False, 'map_size': (500, 500)}
CTX = TEST
DEBUG = CTX['debug']

offsets = {'L': (-1, 0), 'U': (0, 1), 'R': (1, 0), 'D': (0, -1)}


def print_map(segments):
    if DEBUG:
        row_size, col_size = CTX['map_size']
        map = np.array([['.'] * row_size] * col_size)
        head = segments[0]
        tail = segments[-1]

        for i in range(1, len(segments) - 1):
            map[tuple(segments[i])] = str(i)

        map[tuple(tail)] = 'T'
        map[tuple(head)] = 'H'

        print()
        print(map)


def print_tail_visited_map(tail_visits):
    if DEBUG:
        row_size, col_size = CTX['map_size']
        map = np.array([['.'] * row_size] * col_size)

        for visit in tail_visits:
            map[tuple(visit)] = '#'

        print("\n-------\nVisits")
        print(map)


def if_touching(head, tail):
    return max(abs(head[0] - tail[0]), abs(head[1] - tail[1])) > 1


def move(segments, direction):
    dx, dy = offsets[direction]
    segments[0][0] += dx
    segments[0][1] += dy

    if DEBUG: print("\nsegments:", segments)

    for segment_index in range(1, len(segments)):
        head = segments[segment_index - 1]
        tail = segments[segment_index]
        # print_map(segments)

        if if_touching(head, tail):
            if head[0] != tail[0]:
                tail[0] += 1 if head[0] > tail[0] else -1
            if head[1] != tail[1]:
                tail[1] += 1 if head[1] > tail[1] else -1


def simulate(moves, segment_count):
    segments = [[0, 0] for _ in range(segment_count)]
    tail_visits = {tuple(segments[-1])}  # Set

    for idx, mov in enumerate(moves):
        direction, steps = mov
        if DEBUG: print(f'\n-------\n idx: {idx} move: {direction} steps: {steps}\n-------')
        for _ in range(steps):
            move(segments, direction)
            print_map(segments)
            tail_visits.add(tuple(segments[-1]))

    print_tail_visited_map(tail_visits)
    return len(tail_visits)


moves = open(CTX['file']).read().splitlines()
moves = [(move.split()[0], int(move.split()[1])) for move in moves]

# PART 1
print(f'Part 1: {simulate(moves, 2)})')
# 6332

# PART 2
print(f'Part 2: {simulate(moves, 10)}')
# 2511
