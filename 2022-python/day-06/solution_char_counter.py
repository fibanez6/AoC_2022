# --- Day 6: Tuning Trouble ---

import queue

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
DOMAIN = INPUT

class Datastream():

    def __init__(self, buffer_size):
        self.buffer = queue.Queue(buffer_size)
        self.total_uniq = buffer_size
        self.char_counter = {}
        self.unique_char_counter = 0

    def put(self, c):
        if DEBUG: print(c, ">>")
        self.buffer.put(c)
        if c not in self.char_counter.keys():
            self.char_counter[c] = 1
            self.unique_char_counter += 1
        else:
            self.char_counter[c] += 1

    def pop(self):
        c = self.buffer.get()
        if self.char_counter[c] == 1:
            self.char_counter.pop(c)
            self.unique_char_counter -= 1
        else:
            self.char_counter[c] -= 1

    def contains_only_uniques(self):
        return self.unique_char_counter == self.buffer.qsize()

    def print(self):
        print("Datastream:\n", list(self.buffer.queue))
        print("Buffer chars counter:\n", self.char_counter)


def find_marker(data, buffer_size):
    datastream = Datastream(buffer_size)
    index = 0

    for c in data.read(buffer_size):
        datastream.put(c)
        index += 1

    while True:
        if DEBUG: datastream.print()

        # Check if marker is found <> no duplicates in the buffer
        if datastream.contains_only_uniques():
            if DEBUG: print("There are not duplicates")
            break

        char = data.read(1)
        index += 1

        datastream.pop()
        datastream.put(char)

        if not char:
            if DEBUG: print('Reached end of file')
            index = -1
            break

    return index


# PART 1
buffer_size = 4
data = open(DOMAIN['file'], 'r', encoding='utf-8')
marker_pos = find_marker(data, buffer_size)
print("PART 1 - First start-of-packet marker position:", marker_pos)
# 1531

# PART 2
buffer_size = 14
data = open(DOMAIN['file'], 'r', encoding='utf-8')
marker_pos = find_marker(data, buffer_size)
print("PART 2 - First start-of-packet marker position:", marker_pos)
# 2518
