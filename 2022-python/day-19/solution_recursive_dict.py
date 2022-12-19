# --- Day 19: Not Enough Minerals ---

import timeit
import re
import math

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': True}
CTX = TEST
DEBUG = CTX['debug']

ORE, CLAY, OBSIDIAN, GEODE = 'ore', 'clay', 'obsidian', "geode"


def profiler(method):
    def wrapper_method(*arg, **kw):
        start = timeit.default_timer()
        ret = method(*arg, **kw)
        time = "{0:2.9f}".format(timeit.default_timer() - start)
        print(f'{method.__name__} took : {time} sec')
        return ret

    return wrapper_method


blueprint = []
lines = open(CTX['file']).read().splitlines()
for line in lines:
    vals = [int(n) for n in re.findall(r'\d+', line)]
    blueprint.append({
        ORE: {ORE: vals[1], CLAY: 0, OBSIDIAN: 0},
        CLAY: {ORE: vals[2], CLAY: 0, OBSIDIAN: 0},
        OBSIDIAN: {ORE: vals[3], CLAY: vals[4], OBSIDIAN: 0},
        GEODE: {ORE: vals[5], CLAY: 0, OBSIDIAN: vals[6]},
    })


def get_state(timeout, robots, materials):
    return tuple([timeout, *robots.values(), *materials.values()])


def build_robots(robots, materials, robot, recipe, wait, max_spend, remaining_timeout):
    ore = materials[ORE] + robots[ORE] * (wait + 1) - recipe[ORE]
    clay = materials[CLAY] + robots[CLAY] * (wait + 1) - recipe[CLAY]
    obsidian = materials[OBSIDIAN] + robots[OBSIDIAN] * (wait + 1) - recipe[OBSIDIAN]
    geode = materials[GEODE] + robots[GEODE] * (wait + 1)

    ore = min(ore, max_spend[ORE] * remaining_timeout)
    clay = min(clay, max_spend[CLAY] * remaining_timeout)
    obsidian = min(obsidian, max_spend[OBSIDIAN] * remaining_timeout)

    updated_materials = {ORE: ore, CLAY: clay, OBSIDIAN: obsidian, GEODE: geode}

    updated_robots = dict(robots)
    updated_robots.update({robot: updated_robots[robot] + 1})

    return updated_robots, updated_materials


def dfs(blueprint, robots, materials, cache, max_spend, timeout):
    if timeout <= 0:
        print(f'robots: {robots} - materials: {materials}')
        return

    state = get_state(timeout, robots, materials)
    if state in cache:
        return cache[state]

    _max = materials[GEODE] + robots[GEODE] * timeout

    for bp_type in blueprint:
        if bp_type != GEODE and robots[bp_type] >= max_spend[bp_type]:
            continue

        wait = 0
        recipe = blueprint[bp_type]
        for recipe_type, recipe_cost in recipe.items():
            if recipe_cost == 0:
                continue
            if robots[recipe_type] == 0:
                break
            wait = max(wait, math.ceil((recipe_cost - materials[recipe_type]) / robots[recipe_type]))
        else:
            remaining_timeout = timeout - wait - 1
            if remaining_timeout <= 0:
                continue

            updated_robots, updated_materials = build_robots(robots, materials, bp_type, recipe, wait, max_spend,
                                                             remaining_timeout)

            ret = dfs(blueprint, updated_robots, updated_materials, cache, max_spend, remaining_timeout)
            _max = max(_max, ret)

    cache[state] = _max
    return _max


@profiler
def part_1():
    robots = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    materials = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}

    total = 0
    for idx, bp in enumerate(blueprint):
        material_costs = [[v for v in recipes.values()] for recipes in bp.values()]

        cache = {}
        max_spend = {
            ORE: max([x for x, *_ in material_costs]),
            CLAY: max([y for _, y, _ in material_costs]),
            OBSIDIAN: max([z for _, _, z in material_costs])}
        max_num_geode = dfs(bp, robots, materials, cache, max_spend, 24)

        if DEBUG: print(f'largest number of geodes {max_num_geode}')
        total += (idx + 1) * max_num_geode

    print(
        f'PART 1 - What do you get if you add up the quality level of all of the blueprints? {total}')


@profiler
def part_2():
    robots = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    materials = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}

    total = 1
    for bp in blueprint[:3]:
        material_costs = [[v for v in recipes.values()] for recipes in bp.values()]

        cache = {}
        max_spend = {
            ORE: max([x for x, *_ in material_costs]),
            CLAY: max([y for _, y, _ in material_costs]),
            OBSIDIAN: max([z for _, _, z in material_costs])}

        max_num_geode = dfs(bp, robots, materials, cache, max_spend, 32)

        total *= max_num_geode
        if DEBUG: print(f'largest number of geodes {max_num_geode}')

    print(f'PART 2 - What do you get if you multiply these numbers together? {total}')


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
