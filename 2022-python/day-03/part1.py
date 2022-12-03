# --- Day 3: Rucksack Reorganization ---


# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def priority(item):
    if item.isupper():
        return ord(item) - 96
    else:
        return ord(item) - 38


data = open('input', 'r', encoding='utf-8').read().splitlines()

sumOf_item_priorities = 0
for rucksack in data:
    size = len(rucksack) // 2
    content = [*rucksack]
    compartmentA = content[0:size]
    compartmentB = content[size:]

    # Each rucksack has two large compartments. All items of a given type are meant
    # to go into exactly one of the two compartments
    common_item = set(compartmentA).intersection(compartmentB).pop()
    sumOf_item_priorities += priority(common_item)

print("Sum of priorities = ", sumOf_item_priorities)
# 8039
