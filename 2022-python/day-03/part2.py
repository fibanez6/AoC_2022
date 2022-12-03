# --- Day 3: Rucksack Reorganization ---

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def priority(item):
    if item.isupper():
        return ord(item) - 96
    else:
        return ord(item) - 38


data = open("input", "r", encoding='utf-8')

sumOf_item_priorities = 0
for rucksack in data:
    elf1 = [*rucksack.strip()]
    elf2 = [*next(data).strip()]
    elf3 = [*next(data).strip()]

    # Finding the one item type that is common between all three Elves in each group.
    common_item = set(elf1).intersection(elf2).intersection(elf3).pop()
    sumOf_item_priorities += priority(common_item)

print("Sum of priorities = ", sumOf_item_priorities)
# 2510
