#  --- Day 5: Supply Stacks ---

import re

DEBUG = False
TEST = {'file': 'input.test', 'num_stacks': 3, 'max_cranes': 3}
INPUT = {'file': 'input', 'num_stacks': 9, 'max_cranes': 8}
DOMAIN = INPUT


def print_cargo(cargo):
    if DEBUG:
        print("\nCargo:")
        for stack in cargo:
            print(stack)
        print("")


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


def execute_moves(cargo, moves):
    print_cargo(cargo)
    for count, stack_from, stack_to in moves:
        for _ in range(count):
            crate = cargo[stack_from - 1].pop(0)
            if DEBUG: print("move", crate, "from", stack_from, "to", stack_to)
            cargo[stack_to - 1].insert(0, crate)
            print_cargo(cargo)


data = open(DOMAIN['file'], 'r', encoding='utf-8').read().splitlines()

cargo = read_cargo(data, DOMAIN['num_stacks'], DOMAIN['max_cranes'])
moves = read_moves(data, DOMAIN['max_cranes'] + 2)

execute_moves(cargo, moves)
top_each_stack = [stack[0] for stack in cargo]

print("Top of each stack: ", ''.join(top_each_stack))
# SBPQRSCDF
