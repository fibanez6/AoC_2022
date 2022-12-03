# --- Day 3: Rucksack Reorganization ---


# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def priority(char):
    if char.isupper():
        return ord(char) - ord('A') + 27
    else:
        return ord(char) - ord('a') + 1


data = open('input', 'r', encoding='utf-8').read().splitlines()

sumOfPriorities = 0
for rucksack in data:
    size = len(rucksack) // 2
    content = [*rucksack]
    compartmentA = content[0:size]
    compartmentB = content[size:]

    # Each rucksack has two large compartments. All items of a given type are meant
    # to go into exactly one of the two compartments
    commonItem = set(compartmentA).intersection(compartmentB).pop()
    sumOfPriorities += priority(commonItem)

print("sumOfPriorities: ", sumOfPriorities)
# 8039
