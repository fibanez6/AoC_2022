# --- Day 25: Full of Hot Air ---

from bidict import bidict

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']

snafu_table = bidict({'=': -2, '-': -1, '0': 0, '1': 1, '2': 2})


def to_decimal(snafu):
    return sum((5 ** e) * snafu_table[s] for e, s in enumerate(reversed(snafu)))


def to_snafu(n):
    weights = []
    limit = 0

    # [1,5,25,125,...]
    while limit < n:
        w = 5 ** len(weights)
        limit += 2 * w
        weights.append(w)

    snafu = []

    while weights:
        w = weights.pop()
        limit -= 2 * w

        if n == 0:
            snafu.append('0' * (len(weights) + 1))
            break

        if n > 0:
            digit = 0
            while abs(n) > limit:
                digit += 1
                n -= w
            snafu.append(snafu_table.inverse[digit])
        else:
            digit = 0
            while abs(n) > limit:
                digit -= 1
                n += w
            snafu.append(snafu_table.inverse[digit])

    return ''.join(snafu)


snafus = open(CTX['file']).read().splitlines()
total = sum(map(to_decimal, snafus))
print(f'In decimal, the sum of these numbers is {total}')
print(f'PART 1 - What SNAFU number? {to_snafu(total)}')
# 20=2-02-0---02=22=21
