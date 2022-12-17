# --- Day 17: Pyroclastic Flow ---

import collections
import dataclasses
import itertools
import os
import timeit

clear = lambda: os.system('clear')

TEST = {'file': 'input.test', 'debug': True, 'iter-part1': 2022, 'iter-part2': 1_000_000_000_000}
INPUT = {'file': 'input', 'debug': False, 'iter-part1': 2022, 'iter-part2': 1_000_000_000_000}
CTX = INPUT
DEBUG = CTX['debug']

DIRECTION = {'>': [0, 1], '<': [0, -1], 'D': [-1, 0], 'U': [1, 0]}

valves = {}
pattern = open(CTX['file']).read()

UNITS_ABOVE = 3


@dataclasses.dataclass
class Shape:
    name: str
    points: list
    height: int


ROCKS = [
    Shape(
        name='H',
        points=[(0, 2), (0, 3), (0, 4), (0, 5)],
        height=1,
    ),
    Shape(
        name='CR',
        points=[(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)],
        height=3,
    ),
    Shape(
        name='L',
        points=[(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
        height=3,
    ),
    Shape(
        name='V',
        points=[(0, 2), (1, 2), (2, 2), (3, 2)],
        height=4,
    ),
    Shape(
        name='SQ',
        points=[(0, 2), (0, 3), (1, 2), (1, 3)],
        height=2,
    )
]


class Rock:
    def __init__(self, shape, init_height):
        self.name = shape.name
        self.points = [(x + init_height, y) for (x, y) in shape.points]
        self.height_reached = shape.height + init_height

    def move(self, direction, tetris):
        dx, dy = direction
        next_points = [(x + dx, y + dy) for x, y in self.points]

        if any(tetris.check_collision(point) for point in next_points):
            return False

        if DEBUG: print(f'Move to: {next_points}')
        self.points = next_points
        self.height_reached += dx
        return True


@dataclasses.dataclass
class Tetris:
    rocks: set = dataclasses.field(default_factory=set)
    height: int = 0
    wide: int = 7

    # collision with wall, the floor or other rocks
    def check_collision(self, point):
        x, y = point
        if x < 0 or \
                y > self.wide - 1 or \
                y < 0 or \
                point in self.rocks:
            return True

        return False

    def add_rock(self, rock):
        self.rocks.update(rock.points)
        self.height = max(self.height, rock.height_reached)


@dataclasses.dataclass
class CycleDetector:
    history: dict = dataclasses.field(default_factory=dict)
    diff_heights: list = dataclasses.field(default_factory=list)
    cache: collections.deque = dataclasses.field(default_factory=collections.deque)
    cache_size: int = 10
    found: bool = False
    cycle_length: int = None

    def check(self, ite, state):
        _, _, diff_height = state

        if self.found:
            return

        if state in self.history:
            cycle_length = ite - self.history[state]
            if DEBUG: print(f'State {state} found at iter {self.history[state]} - cycle_length {cycle_length}')

            if list(self.cache) == self.diff_heights[-cycle_length - self.cache_size:-cycle_length]:
                self.found = True
                self.cycle_length = cycle_length
                return

        self.history[state] = ite
        self.diff_heights.append(diff_height)

        if len(self.cache) >= self.cache_size:
            self.cache.popleft()

        self.cache.append(diff_height)
        return

    def get_height_at(self, ite):
        cycle_start_at = len(self.diff_heights) - self.cycle_length
        cycle = self.diff_heights[cycle_start_at:]
        cycles = (ite - cycle_start_at) // self.cycle_length
        remaining = ite - cycles * self.cycle_length - cycle_start_at

        sum_firsts = sum(self.diff_heights[:cycle_start_at])
        sum_cycles = sum(cycle) * cycles
        sum_lasts = sum(cycle[:remaining])

        return sum_firsts + sum_cycles + sum_lasts


def add_rock(tetris, num_rocks):
    shapes = itertools.cycle(ROCKS)
    jets = itertools.cycle(enumerate(pattern))
    detector = CycleDetector()

    for ite in range(num_rocks):
        prev_height = tetris.height
        rock = Rock(next(shapes), tetris.height + UNITS_ABOVE)

        while True:
            jet_idx, jet = next(jets)
            if DEBUG: print(f'Rocks {ite + 1} - Tower height {tetris.height} - move {jet}')

            dir = DIRECTION[jet]
            rock.move(dir, tetris)
            success = rock.move(DIRECTION['D'], tetris)

            if not success:
                tetris.add_rock(rock)
                state = (rock.name, jet_idx, tetris.height - prev_height)
                detector.check(ite, state)
                break

        if detector.found:
            break

    if detector.found:
        print(f'-------- Cycle found with length {detector.cycle_length} - total iter {ite}')
        return detector.get_height_at(num_rocks)
    else:
        return tetris.height


#  PART 1
start = timeit.default_timer()
height = add_rock(Tetris(), CTX['iter-part1'])
print(f'PART 1 - Tower height is {height}')
print(f'       - Time: {timeit.default_timer() - start} secs')
# 3069

#  PART 2
start = timeit.default_timer()
height = add_rock(Tetris(), CTX['iter-part2'])
print(f'PART 2 - Tower height is {height}')
print(f'       - Time: {timeit.default_timer() - start} secs')
# 1523167155404
