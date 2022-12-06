# --- Day 1: Calorie Counting ---

TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def read_calories():
    sumOf_elf_calories = []
    acc_calories = 0
    with open(CTX['file'], 'r', encoding='utf-8') as file:
        for line in file:
            if line == "\n":
                sumOf_elf_calories.append(acc_calories)
                acc_calories = 0
            else:
                acc_calories += int(line)
    return sumOf_elf_calories


def part_1(sumOf_elf_calories):
    top_elf = max(sumOf_elf_calories)
    print('Top elf = ', top_elf)


def part_2(sumOf_elf_calories):
    sumOf_elf_calories.sort(reverse=True)
    sumOf_top_three = sum(sumOf_elf_calories[:3])
    print('Sum of top three elves = ', sumOf_top_three)


sumOf_elf_calories = read_calories()

part_1(sumOf_elf_calories)
# 71780
part_2(sumOf_elf_calories)
# 212489
