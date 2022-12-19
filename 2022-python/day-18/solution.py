# --- Day 18: Boiling Boulders ---

import timeit
from collections import deque

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

cubes = set()
data = open(CTX['file']).read().splitlines()
for line in data:
    cubes.add(tuple(map(int, line.split(","))))


def profiler(method):
    def wrapper_method(*arg, **kw):
        start = timeit.default_timer()
        ret = method(*arg, **kw)
        time = "{0:2.9f}".format(timeit.default_timer() - start)
        print(f'{method.__name__} took : {time} sec')
        return ret

    return wrapper_method


def gen_neighbors(x, y, z):
    yield (x, y, z + 1)
    yield (x, y, z - 1)
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)


def get_surface_areas(cubes):
    """
   Generate neighbors and compare them with the collection.
   """
    exposed_areas = 0
    for c in cubes:
        for n in gen_neighbors(*c):
            if n not in cubes:
                exposed_areas += 1
    return exposed_areas


@profiler
def part_1():
    exposed_areas = get_surface_areas(cubes)
    print(f'PART 1 - What is the surface area of your scanned lava droplet? {exposed_areas}')
    # 4340


@profiler
def part_2():
    """
    A big cube that surrounds all ▨ cubes and then apply BFS. It excludes the "cube of air is trapped within the lava
    droplet" as it is unreachable. Finally, surface area of all □ cubes (the cubes in the empty space between the big
    cube and the ▨ data cubes) - surface area of the big cube
    Cuboid:
        Total Surface area = 2 (length × breadth + breadth × height + length × height)
        
                        
                      +---------------+
                     /               / |
                    /               /  |
                   /               /   |
                  +---------------+    |                ▨  trapped within the lava droplet
                  | □□□□□□□□□□□□□ |    |
        height    | □□□□□▨▨▨▨▨▨▨□ |   +
                  | □□□▨▨▨▨▨▨▨▨□□ |  /
                  | □▨▨▨▨▨▨▨▨▨□□□ | /   breadth
                  | □□□□□□□□□□□□□ |/
                  +---------------+
          bfs(x,y)     length
    """
    min_max = lambda x: (min(x) - 1, max(x) + 1)
    surface_area = lambda l, h, b: 2 * (l * b + b * h + l * h)

    x_min, x_max = min_max([x for x, _, _ in cubes])
    y_min, y_max = min_max([y for _, y, _ in cubes])
    z_min, z_max = min_max([z for _, _, z in cubes])

    length = x_max - x_min + 1
    height = y_max - y_min + 1
    breadth = z_max - z_min + 1

    def get_valid_neighbors(x, y, z):
        for n in gen_neighbors(x, y, z):
            if n not in cubes \
                    and x_min <= n[0] <= x_max \
                    and y_min <= n[1] <= y_max \
                    and z_min <= n[2] <= z_max:
                yield n

    # Breadth-First Search
    def bfs(root):
        queue = deque()
        queue.append(root)

        # Mark the root node as visited and enqueue it
        visited = set()
        visited.add(root)

        while queue:
            cube = queue.popleft()
            for n in get_valid_neighbors(*cube):
                if n not in visited:
                    visited.add(n)
                    queue.append(n)

        return visited

    visited = bfs((x_min, y_min, z_min))
    exterior_surface_area = get_surface_areas(visited) - surface_area(length, height, breadth)
    # Count all the neighbors of each data cube inside the big cube
    # exterior_surface_area = sum(n in visited for cube in cubes for n in gen_neighbors(*cube))
    print(f'PART 2 - What is the exterior surface area of your scanned lava droplet? {exterior_surface_area}')
    # 2468


part_1()
part_2()
