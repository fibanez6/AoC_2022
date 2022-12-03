from itertools import groupby

# --- Day 1: Calorie Counting ---

# Cast values to integers from strings and -1 from empties
with open('input', 'r', encoding='utf-8') as file:
    calories = [-1 if (line == '\n') else int(line) for line in file]

# Group calories per elf by splitting by -1
elfCalList = [list(g) for k, g in groupby(calories, lambda x: x != -1) if k]

# Add up all the calories per elf
sumOfElfCal = [sum(c) for c in elfCalList]

#  PART 1
top = max(sumOfElfCal)
print('top elf = ', top)
#  71780

#  PART 2
sumOfElfCal.sort(reverse=True)
sumOfTopThree = sum(sumOfElfCal[:3])
print('Sum of of top three = ', sumOfTopThree)
# 212489
