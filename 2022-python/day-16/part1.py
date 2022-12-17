# --- Day 16: Proboscidea Volcanium PART 1 ---

import math
import os
import timeit
from collections import deque

start = timeit.default_timer()

clear = lambda: os.system('clear')

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = TEST
DEBUG = CTX['debug']

valves = {}
lines = open(CTX['file']).read().splitlines()
for line in lines:
    val, tun = line.split(';')
    valves[val[6:8]] = {
        'flow': int(val[23:]),
        'tunnels': [v.strip() for v in tun[23:].split(',')],
        'paths': {}
    }


def bfs(root, end):
    queue = deque()
    queue.append(root)
    visited = set()
    visited.add(root['state'])

    while queue:
        state, depth = queue.popleft().values()
        if end in valves[state]['tunnels']:
            return depth + 1
        for t in valves[state]['tunnels']:
            if t not in visited:
                visited.add(t)
                queue.append({'state': t, 'depth': depth + 1})

    return math.inf


# Use BFS to determine the distance between meaningful valves (AA, and all valves with non-zero flow rate)
valves_keys = [v for v in list(valves.keys()) if valves[v]['flow'] != 0]
for a in ['AA'] + valves_keys:
    for b in valves_keys:
        if a != b:
            valves[a]['paths'][b] = bfs({'state': a, 'depth': 0}, b)

if DEBUG:
    for k in valves.keys():
        print(f'Valve {k}', valves[k])
    print()


def dfs(opened, curr_val, p_released, timeout):
    global pressure_max
    pressure_max = max(pressure_max, p_released)

    if DEBUG:
        print(f'Current valve {curr_val} - pressure released = {p_released} - timeout = {timeout - 1}')

    if timeout <= 0:
        return

    if curr_val not in opened:
        # Open valve.
        new_opened = opened.union([curr_val])
        new_p_released = p_released + valves[curr_val]['flow'] * timeout
        if DEBUG: print(f'Open val {curr_val}')
        dfs(new_opened, curr_val, new_p_released, timeout - 1)
    else:
        # Move to the next unopened valve and reduce the timer with the cost of movement
        for next_val in valves[curr_val]['paths']:
            if next_val not in opened:
                timeout_updated = timeout - valves[curr_val]['paths'][next_val]
                if DEBUG: print(f'Move to {next_val} - cost = {valves[curr_val]["paths"][next_val]}')
                dfs(opened, next_val, p_released, timeout_updated)


# DFS on this new graph, to find the path with max value, where the path's length is <= 30
pressure_max = 0
opened = set(['AA'])
dfs(opened, 'AA', 0, 29)
print(f'PART 1 - What is the most pressure you can release? {pressure_max}')
# 1707

stop = timeit.default_timer()
print(f'Time: {stop - start} secs')
