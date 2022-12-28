# --- Day 6: Tuning Trouble ---

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def find_marker(datastream, buffer_size):
    index = 0
    endIndex = buffer_size
    while index < len(datastream) - buffer_size - 1:
        slice = datastream[index:endIndex]
        if DEBUG: print("slice:", slice)
        if len(slice) == len(set(slice)):  # this is our marker
            break
        index += 1
        endIndex += 1

    return endIndex


data = open(CTX['file'], 'r', encoding='utf-8').readline()

# PART 1
print(f'PART 1 - First start-of-packet marker position: {find_marker(data, 4)}')
# 1531

# PART 2
print(f'PART 2 - First start-of-packet marker position: {find_marker(data, 14)}')
# 2518
