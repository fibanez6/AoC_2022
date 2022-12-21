# --- Day 21: Monkey Math ---

# Using Python 3.10

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


def add_equation(s, z3term, equation):
    match (equation):
        case [const]:
            s.add(z3term == int(const))
        case [t1, "+", t2]:
            z3t1, z3t2 = Int(t1), Int(t2)
            s.add(z3term == z3t1 + z3t2)
        case [t1, "-", t2]:
            z3t1, z3t2 = Int(t1), Int(t2)
            s.add(z3term == z3t1 - z3t2)
        case [t1, "/", t2]:
            z3t1, z3t2 = Int(t1), Int(t2)
            s.add(z3term == z3t1 / z3t2)
        case [t1, "*", t2]:
            z3t1, z3t2 = Int(t1), Int(t2)
            s.add(z3term == z3t1 * z3t2)
        case [t1, "=", t2]:
            z3t1, z3t2 = Int(t1), Int(t2)
            s.add(z3t1 == z3t2)


lines = open(CTX['file']).read().splitlines()

@profiler
def part_1():
    s = z3.Optimize()
    target = 'root'
    z3target = None

    for line in lines:
        term = line[:4]
        z3term = Int(term)
        add_equation(s, z3term, line[6:].split(' '))
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
        z3term = Int(term)

        if term == target:
            z3target = Int(term)
            continue

        eq = line[6:].split(' ')
        if term == 'root':
            eq[1] = '='
        add_equation(s, z3term, eq)

    s.check()
    m = s.model()

    print(f'PART 2 - What number do you yell to pass root\'s equality test? {m[z3target]}')
    # 3916936880448 - 0.538418083 sec


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
