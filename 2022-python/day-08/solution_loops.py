# --- Day 8: Treetop Tree House ---
"""
    @Author: Christian Salway
    @Links: https://github.com/ccsalway/AdventOfCode/tree/main/2022/day8
"""

TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT

with open(CTX['file']) as f:
    input = f.read().splitlines()

gh = [[int(x) for x in list(line)] for line in input]
gv = list(zip(*gh))
gx, gy = len(gh[0]), len(gh)


def part_1():
    v = 0
    for row in range(gy):
        for col in range(gx):
            t = gh[row][col]  # tree
            r = gh[row][col + 1:]  # right
            d = gv[col][row + 1:]  # down
            f = gh[row][:col][::-1]  # left
            u = gv[col][:row][::-1]  # up
            for n in [r, d, f, u]:
                # visible from at least one side
                if not n or max(n) < t:
                    v += 1
                    break
    return v


def part_2():
    vs = []

    for row in range(gy):
        for col in range(gx):
            t = gh[row][col]  # tree
            r = gh[row][col + 1:]  # right
            d = gv[col][row + 1:]  # down
            f = gh[row][:col][::-1]  # left
            u = gv[col][:row][::-1]  # up
            ts = 1
            for n in [r, d, f, u]:
                # visual space
                s = 0
                for x in n:
                    s += 1
                    if x >= t:
                        break
                ts *= s
            vs.append(ts)

    return max(vs)


print(f'PART 1 - How many trees are visible from outside the grid?", {part_1()}')
# 1698

print(f'PART 2 - What is the highest scenic score possible for any tree?" {part_2()}')
# 672280
