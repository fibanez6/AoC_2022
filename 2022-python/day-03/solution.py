# --- Day 3: Rucksack Reorganization ---

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def priority(item):
    if item.islower():
        # a-z = 1-26
        return ord(item) - 96
    else:
        # A-Z = 27-52
        return ord(item) - 38


def part_1():
    data = open(CTX['file'], 'r', encoding='utf-8').read().splitlines()
    sumOf_item_priorities = 0
    for rucksack in data:
        size = len(rucksack) // 2
        content = [*rucksack]
        compartment_a = content[0:size]
        compartment_b = content[size:]

        # Each rucksack has two large compartments. All items of a given type are meant
        # to go into exactly one of the two compartments
        common_item = set(compartment_a).intersection(compartment_b).pop()
        sumOf_item_priorities += priority(common_item)

    return sumOf_item_priorities


def part_2():
    data = open(CTX['file'], 'r', encoding='utf-8')
    sumOf_item_priorities = 0
    for rucksack in data:
        elf1 = [*rucksack.strip()]
        elf2 = [*next(data).strip()]
        elf3 = [*next(data).strip()]

        # Finding the one item type that is common between all three Elves in each group.
        common_item = set(elf1).intersection(elf2).intersection(elf3).pop()
        sumOf_item_priorities += priority(common_item)

    return sumOf_item_priorities


# PART 1
print(f'PART 1 - Sum of priorities {part_1()}')
# 8039

# PART 2
print(f'PART 2 - Sum of priorities = {part_2()}')
# 2510
