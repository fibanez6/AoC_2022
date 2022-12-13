# --- Day 13: Distress Signal ---

import ast
import functools

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

NO_FOUND = (0, 0)


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return sign(a - b)
    if isinstance(a, int):
        return compare([a], b)
    if isinstance(b, int):
        return compare(a, [b])

    # To find the first element in a sequence seq that matches a predicate
    ai, bi = next(filter(lambda x: compare(x[0], x[1]) != 0, zip(a, b)), NO_FOUND)
    return compare(ai, bi) or sign(len(a) - len(b))


def get_packets():
    packets = open(CTX['file']).read().split('\n\n')
    for idx, pair_packet in enumerate(packets, start=1):
        a, b = pair_packet.splitlines()
        a = ast.literal_eval(a)
        b = ast.literal_eval(b)
        if DEBUG:
            print(f'== Pair {idx} ==')
            print(f'A; {a}\nB: {b}')
        yield a, b


# PART 1
def part_1():
    total = sum(i
                for i, (a, b) in enumerate(get_packets(), start=1)
                if compare(a, b) < 0)
    print(f'PART 1 - What is the sum of the indices of those pairs? {total}')
    # 5208


# PART 2
def part_2():
    packets = [[[2]], [[6]]]
    for a, b in get_packets():
        packets.append(a), packets.append(b)

    sorted_pks = sorted(packets, key=functools.cmp_to_key(compare))

    if DEBUG:
        for p in sorted_pks: print(p)

    idx2 = sorted_pks.index([[2]]) + 1
    idx6 = sorted_pks.index([[6]]) + 1

    print(f'PART 2 - What is the decoder key for the distress signal? '
          f'idx2= {idx2} x idx6= {idx6} = {idx2 * idx6}')
    # 25792


part_1()
part_2()
