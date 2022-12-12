# --- Day 12: Hill Climbing Algorithm ---

from collections import deque
import math

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

lines = open(CTX['file']).read().splitlines()

left = lambda x, y: (x, y - 1)
right = lambda x, y: (x, y + 1)
up = lambda x, y: (x - 1, y)
down = lambda x, y: (x + 1, y)


def get_neighbour(x, y, reverse=False):
    diff_elevation = lambda a, b: b - a if reverse else a - b
    curr_elevation = ord(heightmap[x][y])
    neighbours = [l(x, y) for l in [left, right, up, down]]
    for nx, ny in neighbours:
        if 0 <= nx < len(heightmap) \
                and 0 <= ny < len(heightmap[0]) \
                and diff_elevation(ord(heightmap[nx][ny]), curr_elevation) <= 1:
            yield (nx, ny)


# Breadth-First Search
def BFS(root, end, reverse=False):
    # Create a queue for BFS
    queue = deque()
    queue.append(root)

    # Mark the root node as visited and enqueue it
    visited = set()
    visited.add(root['state'])

    while queue:
        n = queue.popleft()
        state, steps = (lambda state, steps: (state, steps))(**n)

        if DEBUG: print("state:", state, "--- steps:", steps)

        if heightmap[state[0]][state[1]] == end:
            return steps

        # Get all neighbour of the dequeued node
        for n in get_neighbour(*state, reverse):
            if not n in visited:
                visited.add(n)
                queue.append({"state": n, "steps": steps + 1})
                if DEBUG: print("queueing neighbour", n)

    return math.inf


heightmap = []
for ri, row in enumerate(lines):
    heightmap.append(list(row))
    for ci, e in enumerate(row):
        if e == 'S':
            start = (ri, ci)
            heightmap[ri][ci] = 'a'
        if e == 'E':
            end = (ri, ci)
            heightmap[ri][ci] = 'z'

# PART 1
print(f'\nPART 1 - From {start} ---> to \'z\'')
part1 = BFS({"state": start, "steps": 0}, 'z')
print(f'PART 1 - What is the fewest steps required from S to E? {part1}')
# 504

# PART 2
print(f'\nPART 2 - From: {end} ---> to first \'a\'')
part2 = BFS({"state": end, "steps": 0}, 'a', True)
print(f'PART 2 - What is the fewest steps required from E to a? {part2}')
# 500
