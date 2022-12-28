#  --- Day 5: Supply Stacks ---

import re

DEBUG = False
TEST = {'file': 'input.test', 'num_stacks': 3, 'max_cranes': 3}
INPUT = {'file': 'input', 'num_stacks': 9, 'max_cranes': 8}
CTX = INPUT


def print_cargo(cargo):
    if DEBUG:
        print("\nCargo:")
        for stack in cargo:
            print(stack)
        print("")


def read_file():
    data = open(CTX['file'], 'r', encoding='utf-8').read().splitlines()
    cargo = read_cargo(data, CTX['num_stacks'], CTX['max_cranes'])
    moves = read_moves(data, CTX['max_cranes'] + 2)
    return cargo, moves


def read_cargo(data, num_stacks, max_cranes):
    cargo = [[] for i in range(num_stacks)]

    for stack in range(num_stacks):
        for i in range(max_cranes):
            crate = data[i][stack * 4 + 1]
            if not crate == ' ':
                if DEBUG: print("stack =", stack, "crate idx =", i, "crate =", crate)
                cargo[stack].append(crate)

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
print(f'PART 1 - Top of each stack: {part_1()}')
# SBPQRSCDF

# PART 2
print(f'PART 2 - Top of each stack: {part_2()}')
# RGLVRCQSB
