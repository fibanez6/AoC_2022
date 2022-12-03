# --- Day 1: Calorie Counting ---

sumOfElfCalList = []
sumOfElfCal = 0
with open('input', 'r', encoding='utf-8') as file:
    for line in file:
        if line == "\n":
            sumOfElfCalList.append(sumOfElfCal)
            sumOfElfCal = 0
        else:
            sumOfElfCal += int(line)

#  PART 1
top = max(sumOfElfCalList)
print('top elf = ', top)
#  71780

#  PART 2
sumOfElfCalList.sort(reverse=True)
sumOfTopThree = sum(sumOfElfCalList[:3])
print('Sum of of top three = ', sumOfTopThree)
# 212489
