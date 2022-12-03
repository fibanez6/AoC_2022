# --- Day 3: Rucksack Reorganization ---

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def priority(char):
    if char.isupper():
        return ord(char) - ord('A') + 27
    else:
        return ord(char) - ord('a') + 1


data = open("input", "r", encoding='utf-8')

sumOfPriorities = 0
for rucksack in data:
    elf1 = [*rucksack.strip()]
    elf2 = [*next(data).strip()]
    elf3 = [*next(data).strip()]

    # Finding the one item type that is common between all three Elves in each group.
    commonItem = set(elf1).intersection(elf2).intersection(elf3).pop()
    sumOfPriorities += priority(commonItem)

print("sumOfPriorities: ", sumOfPriorities)
# 2510
