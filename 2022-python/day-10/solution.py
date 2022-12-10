# --- Day 10: Cathode-Ray Tube ---

TEST = {'file': 'input.test', 'debug': True, 'lit_pixel': '#', 'dark_pixel': '.'}
INPUT = {'file': 'input', 'debug': False, 'lit_pixel': '\u258A', 'dark_pixel': ' '}
CTX = INPUT
DEBUG = CTX['debug']

dark = CTX['dark_pixel']
lit = CTX['lit_pixel']


def print_sprite(pos, crt_read):
    if DEBUG:
        sprite = [dark] * 40
        for idx in range(pos, min(40, pos + 3)):
            sprite[idx] = lit
        sprite[crt_read] = "[" + sprite[crt_read] + "]"
        print("Sprite:", sprite)


def print_ctr(crtScreen):
    for r in range(6):
        row = crtScreen[r * 40: r * 40 + 40]
        print(''.join(row))


def execute_program():
    cycle = 0
    with open(CTX['file'], 'r') as f:
        for line in f:
            cycle += 1
            if 'addx' in line:
                _, n = line.strip().split(' ')
                yield cycle, 0
                cycle += 1
                yield cycle, int(n)
            else:
                yield cycle, 0


register_x = 1
strengths = []
crtScreen = [dark] * 240

for c, v in execute_program():
    if DEBUG: print(f'cycle {c} ----- value: {v}')
    register_x += v

    # PART 1
    if c in (20, 60, 100, 140, 180, 220):
        strengths.append(register_x * c)
        if DEBUG: print(f'Adding signal strength: {strengths[-1]} register value: {register_x}')

    # PART 2
    print_sprite(register_x - 1, c % 40 - 1)
    if register_x - 1 <= c % 40 <= register_x + 1:
        crtScreen[c] = lit

# PART 1
print(f'The signal strength: {strengths}')
print(f'PART 1 - What is the sum of these six signal strengths?: {sum(strengths)}')
# 15120

# PART 2
print("\nPART 2\n")
print_ctr(crtScreen)

#  ▊▊  ▊  ▊ ▊▊▊    ▊▊ ▊▊▊  ▊▊▊  ▊     ▊▊
# ▊  ▊ ▊ ▊  ▊  ▊    ▊ ▊  ▊ ▊  ▊ ▊    ▊  ▊
# ▊  ▊ ▊▊   ▊  ▊    ▊ ▊▊▊  ▊  ▊ ▊    ▊  ▊
# ▊▊▊  ▊ ▊  ▊▊▊     ▊ ▊  ▊ ▊▊▊  ▊    ▊▊▊▊
# ▊ ▊  ▊ ▊  ▊    ▊  ▊ ▊  ▊ ▊    ▊    ▊  ▊
# ▊  ▊ ▊  ▊ ▊     ▊▊  ▊▊▊  ▊    ▊▊▊▊ ▊  ▊
# RKPJBPLA
