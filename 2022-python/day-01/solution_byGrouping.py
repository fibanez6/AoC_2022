from itertools import groupby

# --- Day 1: Calorie Counting ---

TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT

# Cast values to integers from strings and -1 from empties
with open(CTX['file'], 'r', encoding='utf-8') as file:
    calories = [-1 if (line == '\n') else int(line) for line in file]

# Group calories per elf by splitting by -1
groupOf_elf_calories = [list(g) for k, g in groupby(calories, lambda x: x != -1) if k]

# Add up all the calories per elf
sumOf_elf_calories = [sum(c) for c in groupOf_elf_calories]

#  PART 1
top_elf = max(sumOf_elf_calories)
print('top elf = ', top_elf)
#  71780

#  PART 2
sumOf_elf_calories.sort(reverse=True)
sumOf_top_three = sum(sumOf_elf_calories[:3])
print('Sum of top three elves = ', sumOf_top_three)
# 212489
