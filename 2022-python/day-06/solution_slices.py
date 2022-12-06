# --- Day 6: Tuning Trouble ---

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
DOMAIN = INPUT


def find_marker(datastream, buffer_size):
    index = 0
    endIndex = buffer_size
    while index < len(datastream) - buffer_size - 1:
        slice = datastream[index:endIndex]
        if DEBUG: print("slice", slice)
        if len(slice) == len(set(slice)):  # this is our marker
            break
        index += 1
        endIndex += 1

    return endIndex


# PART 1
data = open(DOMAIN['file'], 'r', encoding='utf-8').readline()
marker_pos = find_marker(data, 4)
print("PART 1 - First start-of-packet marker position:", marker_pos)
# 1531

# PART 2
data = open(DOMAIN['file'], 'r', encoding='utf-8').readline()
marker_pos = find_marker(data, 14)
print("PART 2 - First start-of-packet marker position:", marker_pos)
# 2518
