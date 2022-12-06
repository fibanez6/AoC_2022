#  --- Day 5: Supply Stacks ---

# Load cargo data by figure out how many stacks and cranes there are
# NOTE: Your IDE may trim trailing whitespace in the data

import re

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def print_cargo(cargo):
    if DEBUG:
        print("\nCargo:")
        for stack in cargo:
            print(stack)
        print("")


def read_file():
    data = open(CTX['file'], 'r', encoding='utf-8').read().splitlines()
    cargo = read_cargo(data)
    max_num_cranes = max([len(x) for x in cargo])
    moves = read_moves(data, max_num_cranes + 2)
    return cargo, moves


def read_cargo(data):
    cranes_pos = []
    for line in data:
        positions = [
            [match.start(), match.group()] for match in re.finditer(r"[A-Z]", line)
        ]
        cranes_pos.append(positions)

        if not positions:
            break

    # [          [5, 'D'], 
    # [[1, 'N'], [5, 'C']], 
    # [[1, 'Z'], [5, 'M'], [9, 'P']]
    if DEBUG: print(cranes_pos)

    num_stacks = max([len(x) for x in cranes_pos])
    cargo = [[] for _ in range(num_stacks)]

    for row in cranes_pos:
        for crane_pos, crane in row:
            stack = int(crane_pos) // 4
            # if DEBUG: print("stack = ", stack, " crane = ", crane)
            cargo[stack].append(crane)

    print_cargo(cargo)
    return cargo


def read_moves(data, cargo_size):
    moves = data[cargo_size:]
    for move in moves:
        yield list(map(int, re.findall(r'\b\d+\b', move)))


def crateMover_9000(cargo, moves):
    print_cargo(cargo)
    for count, stack_from, stack_to in moves:
        for _ in range(count):
            crate = cargo[stack_from - 1].pop(0)
            if DEBUG: print("move", crate, "from", stack_from, "to", stack_to)
            cargo[stack_to - 1].insert(0, crate)
            print_cargo(cargo)


def crateMover_9001(cargo, moves):
    print_cargo(cargo)
    for count, stack_from, stack_to in moves:
        for i in reversed(range(count)):
            if DEBUG: print("move", cargo[stack_from - 1][i], "from", stack_from, "to", stack_to)
            cargo[stack_to - 1].insert(0, cargo[stack_from - 1].pop(i))
        print_cargo(cargo)


def part_1():
    cargo, moves = read_file()
    crateMover_9000(cargo, moves)
    top_each_stack = [stack[0] for stack in cargo]
    return ''.join(top_each_stack)


def part_2():
    cargo, moves = read_file()
    crateMover_9001(cargo, moves)
    top_each_stack = [stack[0] for stack in cargo]
    return ''.join(top_each_stack)


# PART 1
print("PART 1 - Top of each stack: ", part_1())
# SBPQRSCDF

# PART 2
print("PART 2 - Top of each stack: ", part_2())
# RGLVRCQSB
