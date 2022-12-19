# --- Day 19: Not Enough Minerals ---

import timeit
import re
import math

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': True}
CTX = TEST
DEBUG = CTX['debug']

ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3


def profiler(method):
    def wrapper_method(*arg, **kw):
        start = timeit.default_timer()
        ret = method(*arg, **kw)
        time = "{0:2.9f}".format(timeit.default_timer() - start)
        print(f'{method.__name__} took : {time} sec')
        return ret

    return wrapper_method


def get_state(timeout, robots, materials):
    return tuple([timeout, *robots, *materials])


def dfs(blueprint, robots, materials, cache, max_spend, timeout):
    if timeout <= 0:
        print(f'robots: {robots} - materials: {materials}')
        return

    state = get_state(timeout, robots, materials)
    if state in cache:
        return cache[state]

    _max = materials[GEODE] + robots[GEODE] * timeout

    for bp_type, recipe in enumerate(blueprint):
        if bp_type != GEODE and robots[bp_type] >= max_spend[bp_type]:
            continue

        wait = 0
        for r_type, r_cost in (r for r in enumerate(recipe) if r[1] != 0):
            if robots[r_type] == 0:
                break
            wait = max(wait, math.ceil((r_cost - materials[r_type]) / robots[r_type]))
        else:
            remaining_timeout = timeout - wait - 1
            if remaining_timeout <= 0:
                continue

            updated_materials = [m + r * (wait + 1) - rp for r, m, rp in
                                 zip(robots, materials, recipe + [0])]
            updated_materials = [min(curr, m * remaining_timeout) for curr, m in
                                 zip(updated_materials, max_spend + [updated_materials[GEODE]])]

            updated_robots = robots[:]  # copy
            updated_robots[bp_type] += 1

            ret = dfs(blueprint, updated_robots, updated_materials, cache, max_spend, remaining_timeout)
            _max = max(_max, ret)

    cache[state] = _max
    return _max


blueprint = []
lines = open(CTX['file']).read().splitlines()
for line in lines:
    vals = [int(n) for n in re.findall(r'\d+', line)]
    blueprint.append([[vals[1], 0, 0],  # robot ore recipe
                      [vals[2], 0, 0],  # robot clay recipe
                      [vals[3], vals[4], 0],  # robot obsidian recipe
                      [vals[5], 0, vals[6]]  # robot geode recipe
                      ])


@profiler
def part_1():
    robots_init = [1, 0, 0, 0]
    materials_init = [0, 0, 0, 0]

    total = 0
    for idx, bp in enumerate(blueprint):
        cache = {}
        max_spend = [max([ore for ore, *_ in bp]),  # max ore
                     max([clay for _, clay, _ in bp]),  # max clay
                     max([obsidian for _, _, obsidian in bp])  # max obsidian
                     ]
        max_num_geode = dfs(bp, robots_init, materials_init, cache, max_spend, 24)

        if DEBUG: print(f'largest number of geodes {max_num_geode}')
        total += (idx + 1) * max_num_geode

    print(f'PART 1 - What is the add up the quality level of all of the blueprints? {total}')


@profiler
def part_2():
    robots_init = [1, 0, 0, 0]
    materials_init = [0, 0, 0, 0]

    total = 1
    for bp in blueprint[:3]:
        cache = {}
        max_spend = [max([ore for ore, *_ in bp]),  # max ore
                     max([clay for _, clay, _ in bp]),  # max clay
                     max([obsidian for _, _, obsidian in bp])  # max obsidian
                     ]

        max_num_geode = dfs(bp, robots_init, materials_init, cache, max_spend, 32)
        if DEBUG: print(f'largest number of geodes {max_num_geode}')
        total *= max_num_geode

    print(f'PART 2 - What is the multiply these numbers together? {total}')


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
