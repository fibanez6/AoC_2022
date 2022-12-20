# --- Day 20: Grove Positioning System ---

import timeit

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


def print_numbers(numbers, indices):
    cp = [numbers[i] for i in indices]
    print(cp)


def decrypt(numbers, times=1):
    indices = list(range(len(numbers)))

    for i in indices * times:
        indices.pop(j := indices.index(i))
        indices.insert((j + numbers[i]) % len(indices), i)

    if DEBUG:
        print_numbers(numbers, indices)

    zero = indices.index(numbers.index(0))
    # The number list after (x000 % len(numbers)) times
    return sum(numbers[indices[(zero + p * 1000) % len(numbers)]] for p in [1, 2, 3])


@profiler
def part_1():
    numbers = [int(x) for x in open(CTX['file'])]

    ret = decrypt(numbers)
    print(f'PART 1 - What is the sum of the 1000th, 2000th and 3000th numbers? {ret}')
    # 11037 - 0.060878667 sec


@profiler
def part_2():
    decryption_key = 811_589_153
    numbers = [int(x) * decryption_key for x in open(CTX['file'])]

    ret = decrypt(numbers, 10)
    print(f'PART 2 - What is the sum of the 1000th, 2000th and 3000th numbers? {ret}')
    # 3033720253914 - 0.909982583 sec


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
