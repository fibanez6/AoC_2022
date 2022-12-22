# --- Day 22: Monkey Map ---
# CUBE

import re

TEST = {'file': 'input.test', 'debug': True, 'size': 4}
INPUT = {'file': 'input', 'debug': False, 'size': 50}
CTX = INPUT
DEBUG = CTX['debug']

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

board = {}
row_ends = {}
col_ends = {}
sections = set()
elf = None
facing = 0
sq = CTX['size']


def turn(facing, dir="R", times=1):
    return (0, 1, 2, 3)[(facing + times * (-1, 1)[dir == "R"]) % 4]


data = open(CTX['file']).read().split("\n\n")
x = 0
for row in data[0].splitlines():
    row_section = x // sq + 1
    x += 1
    for y, el in enumerate(row, 1):
        col_section = (y - 1) // sq + 1
        if el != " ":
            sections.add((row_section, col_section))

            if el == ".":
                board[x, y] = (True, (row_section, col_section))
            elif el == '#':
                board[x, y] = (False, (row_section, col_section))

            if board.get((x - 1, y)) == None:
                col_ends[y] = (x, None)
            else:
                col_ends[y] = (col_ends[y][0], x)
            if not elf and x == 1:
                elf = (1, y)
            row_ends[x] = (row_ends.get(x, (y,))[0], y)


def turn(facing, dir="R", times=1):
    _dir = (facing + times) % 4 if dir == 'R' else (facing + times * -1) % 4
    return (RIGHT, DOWN, LEFT, UP)[_dir]


def move(steps):
    global elf
    global facing

    for _ in range(steps):
        dp, di = not facing in (1, 3), (1, -1)[facing in (2, 3)]
        new = elf[dp] + di
        s1, s2 = board.get(elf)[1][:: -1 if dp else 1]
        ends = (col_ends, row_ends)[dp][elf[~dp]]
        if new < ends[0] or new > ends[1]:
            changed_sec_pos = 1 if di == -1 else sq
            const_sec_pos = elf[~dp] - sq * (s2 - 1)
            for sec, value in (
                    (
                            (s1 - 3 * di, s2),
                            (facing, (sq + 1) - changed_sec_pos, const_sec_pos),
                    ),
                    (
                            (s1 - 3 * di, s2 + 2 * di),
                            (facing, (sq + 1) - changed_sec_pos, const_sec_pos),
                    ),
                    (
                            (s1 - 3 * di, s2 + 2 * di),
                            (facing, (sq + 1) - changed_sec_pos, const_sec_pos),
                    ),
                    (
                            (s1 + di, s2 - di),
                            (turn(facing, ("R", "L")[dp]), const_sec_pos, changed_sec_pos),
                    ),
                    (
                            (s1 + di, s2 + di),
                            (
                                    turn(facing, ("L", "R")[dp]),
                                    (sq + 1) - const_sec_pos,
                                    (sq + 1) - changed_sec_pos,
                            ),
                    ),
                    (
                            (s1 - 3 * di, s2 - di),
                            (
                                    turn(facing, ("L", "R")[dp]),
                                    (sq + 1) - changed_sec_pos,
                                    (sq + 1) - const_sec_pos,
                            ),
                    ),
                    (
                            (s1 - 3 * di, s2 + di),
                            (turn(facing, ("R", "L")[dp]), const_sec_pos, changed_sec_pos),
                    ),
                    (
                            (s1 - di, s2 - 3 * di),
                            (
                                    turn(facing, ("L", "R")[dp]),
                                    (sq + 1) - changed_sec_pos,
                                    const_sec_pos,
                            ),
                    ),
                    (
                            (s1 - di, s2 + 3 * di),
                            (turn(facing, ("R", "L")[dp]), const_sec_pos, changed_sec_pos),
                    ),
                    (
                            (s1 - di, s2 + 2 * di),
                            (
                                    turn(facing, times=2),
                                    changed_sec_pos,
                                    (sq + 1) - const_sec_pos,
                            ),
                    ),
                    (
                            (s1 - di, s2 - 2 * di),
                            (
                                    turn(facing, times=2),
                                    changed_sec_pos,
                                    (sq + 1) - const_sec_pos,
                            ),
                    ),
                    (
                            (s1 + di, s2 + 2 * di),
                            (
                                    turn(facing, times=2),
                                    changed_sec_pos,
                                    (sq + 1) - const_sec_pos,
                            ),
                    ),
                    (
                            (s1 + di, s2 - 2 * di),
                            (
                                    turn(facing, times=2),
                                    changed_sec_pos,
                                    (sq + 1) - const_sec_pos,
                            ),
                    ),
            ):
                s = sec[:: -1 if dp else 1]
                if s in sections:
                    new_facing = value[0]
                    new_pos = (
                        value[1] + sq * (sec[0] - 1),
                        value[2] + sq * (sec[1] - 1),
                    )
                    new_pos = new_pos[:: -1 if dp else 1]
                    break
        else:
            new_pos = (elf[~dp], new) if dp else (new, elf[~dp])
            new_facing = facing
        if not board[new_pos][0]:
            break
        elf = new_pos
        facing = new_facing


for p in re.findall('\d+|[LR]', data[1]):
    if p.isdigit():
        steps = int(p)
        move(steps)
    else:
        facing = turn(facing, p)

print(f'PART 2 - What is the final password?', 1000 * elf[0] + 4 * elf[1] + facing)
# 55343
