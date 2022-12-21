# --- Day 21: Monkey Math ---

import timeit
from z3 import *

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']


def profiler(method):
    def wrapper_method(*arg, **kw):
        start = timeit.default_timer()
        ret = method(*arg, **kw)
        time = "{0:2.9f}".format(timeit.default_timer() - start)
        print(f'{method.__name__} took : {time} sec')
        return ret

    return wrapper_method


def add_equation(s, z3term, z3t1, op, z3t2):
    if op == '+':
        s.add(z3term == z3t1 + z3t2)
    elif op == '-':
        s.add(z3term == z3t1 - z3t2)
    elif op == '/':
        s.add(z3term == z3t1 / z3t2)
    elif op == '*':
        s.add(z3term == z3t1 * z3t2)
    elif op == '=':
        s.add(z3t1 == z3t2)


def add_constant(s, z3term, const):
    s.add(z3term == const)


lines = open(CTX['file']).read().splitlines()


@profiler
def part_1():
    s = z3.Optimize()
    target = 'root'
    z3target = None

    for line in lines:
        term = line[:4]
        if len(line) > 12:
            z3term, z3t1, op, z3t2 = Int(term), Int(line[6:10]), line[11], Int(line[13:])
            add_equation(s, z3term, z3t1, op, z3t2)
        else:
            z3term, const = Int(term), int(line[6:])
            add_constant(s, z3term, const)
        if term == target:
            z3target = z3term

    s.check()
    m = s.model()

    print(f'PART 1 - What number do you yell to pass root\'s equality test? {m[z3target]}')
    # 41857219607906 - 0.543951375 sec


@profiler
def part_2():
    s = z3.Optimize()
    target = 'humn'
    z3target = None

    for line in lines:
        term = line[:4]
        if term == target:
            z3target = Int(term)
        elif len(line) > 12:
            z3term, z3t1, z3t2 = Int(term), Int(line[6:10]), Int(line[13:])
            op = '=' if term == 'root' else line[11]
            add_equation(s, z3term, z3t1, op, z3t2)
        else:
            z3term, const = Int(term), int(line[6:])
            add_constant(s, z3term, const)

    s.check()
    m = s.model()

    print(f'PART 1 - What number do you yell to pass root\'s equality test? {m[z3target]}')
    # 3916936880448 - 0.538418083 sec


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
