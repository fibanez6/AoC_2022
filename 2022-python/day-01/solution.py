# --- Day 1: Calorie Counting ---

sumOf_elf_calories = []
acc_calories = 0
with open('input', 'r', encoding='utf-8') as file:
    for line in file:
        if line == "\n":
            sumOf_elf_calories.append(acc_calories)
            acc_calories = 0
        else:
            acc_calories += int(line)

#  PART 1
top_elf = max(sumOf_elf_calories)
print('top elf = ', top_elf)
#  71780

#  PART 2
sumOf_elf_calories.sort(reverse=True)
sumOf_top_three = sum(sumOf_elf_calories[:3])
print('Sum of top three elves = ', sumOf_top_three)
# 212489
