# --- Day 4: Camp Cleanup ---

# data = open('input.test', 'r', encoding='utf-8').read().splitlines()
data = open('input', 'r', encoding='utf-8').read().splitlines()


def get_range_sections(section_assignment):
    return list(map(int, section_assignment.split('-')))


total_fully_contained = 0
for pair in data:
    elf1_sections, elf2_sections = pair.split(',')
    elf1_sections_from, elf1_sections_to = get_range_sections(elf1_sections)
    elf2_sections_from, elf2_sections_to = get_range_sections(elf2_sections)

    if (elf1_sections_from <= elf2_sections_from and elf1_sections_to >= elf2_sections_to) or (
            elf1_sections_from >= elf2_sections_from and elf1_sections_to <= elf2_sections_to):
        total_fully_contained += 1

print("Total of sections fully contained = ", total_fully_contained)
#  487
