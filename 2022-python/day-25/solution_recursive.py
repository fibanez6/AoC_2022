# --- Day 25: Full of Hot Air ---

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = TEST
DEBUG = CTX['debug']

snafu_table = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def to_decimal(snafu):
    return sum((5 ** e) * snafu_table[s] for e, s in enumerate(reversed(snafu)))


def to_snafu(n, limit=None):
    if limit is None:
        limit = 0
        while abs(n) > (5 ** limit - 1) / 2:
            limit += 1
    if limit == 0:
        return ""

    pw = 5 ** (limit - 1)
    lim = (5 ** (limit - 1)) / 2

    if abs(n - 2 * pw) <= lim:
        return "2" + to_snafu(n - 2 * pw, limit - 1)
    elif abs(n - 1 * pw) <= lim:
        return "1" + to_snafu(n - 1 * pw, limit - 1)
    elif abs(n - 0 * pw) <= lim:
        return "0" + to_snafu(n - 0 * pw, limit - 1)
    elif abs(n - (-1) * pw) <= lim:
        return "-" + to_snafu(n - (-1) * pw, limit - 1)
    elif abs(n - (-2) * pw) <= lim:
        return "=" + to_snafu(n - (-2) * pw, limit - 1)


snafus = open(CTX['file']).read().splitlines()
total = sum(map(to_decimal, snafus))
print(f'In decimal, the sum of these numbers is {total}')
print(f'PART 1 - What SNAFU number? {to_snafu(total)}')
# 20=2-02-0---02=22=21
