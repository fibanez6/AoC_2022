# --- Day 4: Camp Cleanup ---

# data = open('input.test', 'r', encoding='utf-8').read().splitlines()
data = open('input', 'r', encoding='utf-8').read().splitlines()


def get_range_sections(section_assignment):
    return list(map(int, section_assignment.split('-')))


total_fully_contained = 0
for pair in data:
    # pair ['2-8','3-7']
    elves = pair.split(',')

    elf1_sections = get_range_sections(elves[0])
    elf2_sections = get_range_sections(elves[1])

    if (elf1_sections[0] <= elf2_sections[0] and elf1_sections[1] >= elf2_sections[1]) or (
            elf1_sections[0] >= elf2_sections[0] and elf1_sections[1] <= elf2_sections[1]):
        total_fully_contained += 1

print("Total of sections fully contained = ", total_fully_contained)
#  487