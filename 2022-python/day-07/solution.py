# --- Day 7: No Space Left On Device ---

import re

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT

filesize = {}
parent_directories = []
current_directory = ["/"]


def change_directory(input):
    if input == "..":
        current_directory[0] = parent_directories.pop(-1)
    else:
        parent_directories.append(current_directory[0])
        current_directory[0] = current_directory[0] + "/" + input


def update_fs(fs, file):
    if file in filesize:
        filesize[file] = filesize[file] + int(fs)
    else:
        filesize[file] = int(fs)


def process_line(line):
    if DEBUG: print("Processing:", line)
    if len(line) == 3:
        change_directory(line[2])
    elif re.search("^\d+$", line[0]):
        update_fs(line[0], current_directory[0])
        for p in parent_directories:
            update_fs(line[0], p)


with open(CTX['file'], 'r') as f:
    commands = [line.strip().split(" ") for line in f]
    for cmd in commands[1:]:
        process_line(cmd)

# PART 1
sumOf_directories = sum(list(filter(lambda size: size <= 100000, filesize.values())))
print(f'PART 1 - The sum of the directories with a total size of at most 100000 is: {sumOf_directories}')
# 1390824

# PART 2
space_required = 30000000 - (70000000 - int(list(filesize.values())[0]))
total_size = min(list(filter(lambda size: size >= space_required, filesize.values())))
print(f'PART 2 - The total size of that directories is: {total_size}')
# 7490863
