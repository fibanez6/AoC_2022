# --- Day 20: Grove Positioning System ---

import timeit

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': True}
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


def swap(numbers, indices, index, n):
    value = numbers[index]
    location_of_index = [i for i, x in enumerate(indices) if x == index][0]
    indices.pop(location_of_index)
    insert_at = (location_of_index + value) % (n - 1)
    indices.insert(insert_at, index)
    return value


def decrypt(numbers, times=1):
    indices = [i for i in range(len(numbers))]
    for k in range(times):
        for i, number in enumerate(numbers):
            swap(numbers, indices, i, len(numbers))

    _numbers = [numbers[i] for i in indices]
    idx_zero = indices.index(numbers.index(0))

    return sum(_numbers[(idx_zero + p * 1000) % len(numbers)] for p in [1, 2, 3])


@profiler
def part_1():
    numbers = [int(x) for x in open(CTX['file'])]

    ret = decrypt(numbers)
    print(f'PART 1 - What is the sum of the 1000th, 2000th and 3000th numbers? {ret}')
    # 11037 - 1.143206125 sec


@profiler
def part_2():
    decryption_key = 811_589_153
    numbers = [int(x) * decryption_key for x in open(CTX['file'])]

    ret = decrypt(numbers, 10)
    print(f'PART 2 - What is the sum of the 1000th, 2000th and 3000th numbers? {ret}')
    # 3033720253914 - 11.386642208 sec


print(f'Running PART 1')
part_1()

print(f'Running PART 2')
part_2()
