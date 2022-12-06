# --- Day 6: Tuning Trouble ---

import queue

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def find_marker(data, buffer_size):
    index = 0
    buffer = queue.Queue(buffer_size)

    for c in data.read(buffer_size):
        buffer.put(c)
        index += 1

    while True:
        if DEBUG: print(list(buffer.queue))

        # Check for no duplicates
        if len(set(buffer.queue)) == buffer_size:
            if DEBUG: print("There are not duplicates")
            break

        char = data.read(1)
        if DEBUG: print(char, ">>")
        buffer.get()
        buffer.put(char)
        index += 1

        if not char:
            if DEBUG: print('Reached end of file')
            break
    return index


# PART 1
data = open(CTX['file'], 'r', encoding='utf-8')
print("PART 1 - First start-of-packet marker position:", find_marker(data, 4))
# 1531

# PART 2
data = open(CTX['file'], 'r', encoding='utf-8')
print("PART 2 - First start-of-packet marker position:", find_marker(data, 14))
# 2518
