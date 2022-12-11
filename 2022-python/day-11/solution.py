# --- Day 11: Monkey in the Middle ---

from math import lcm

TEST = {'file': 'input.test', 'debug': True}
INPUT = {'file': 'input', 'debug': False}
CTX = INPUT
DEBUG = CTX['debug']


def read_file():
    monkeys = []
    file = open(CTX['file']).read().splitlines()
    for idx in range(0, len(file), 7):
        _, items, op, div, t, f = file[idx:idx + 6]
        monkeys.append({
            'items': [int(i) for i in items[18:].split(',')],
            'op': lambda old, op=op[19:]: eval(op),
            'div': int(div[20:]),
            'true': int(t[28:]),
            'false': int(f[29:]),
            'inspected': 0
        })
    return monkeys


def play(monkeys, times, get_worry_level):
    for r in range(times):
        if DEBUG: print(f'\n========= [Round {r}] ==========')
        for m_idx, m in enumerate(monkeys):
            if DEBUG: print(f'---------- Monkey {m_idx} ----------')
            for item in m['items']:
                # worry_level = m['op'](item) // 3
                # worry_level = m['op'](item) % lcm
                worry_level = get_worry_level(m['op'](item))
                dest = m['false'] if worry_level % m['div'] else m['true']
                monkeys[dest]['items'].append(worry_level)
                m['inspected'] += 1

                if DEBUG:
                    print(f'Worry level is {worry_level * 3}')
                    print(f'Item with worry level {worry_level} is thrown to monkey {dest}')

            m['items'] = []


# PART 1
def part_1():
    monkeys = read_file()
    play(monkeys, 20, lambda x: x // 3)
    first, second, *_ = sorted([m['inspected'] for m in monkeys], reverse=True)
    print(f'\nPART 1 - What is the level after 20 rounds? {first * second}')
    # 120756


# PART 2
def part_2():
    monkeys = read_file()

    # Least Common Multiple
    base = lcm(*(m['div'] for m in monkeys))
    play(monkeys, 10_000, lambda x: x % base)

    first, second, *_ = sorted([m['inspected'] for m in monkeys], reverse=True)
    print(f'\nPART 2 - What is the level after 10000 rounds? {first * second}')
    # 39109444654


part_1()
part_2()
