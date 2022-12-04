# --- Day 4: Camp Cleanup ---

# data = open('input.test', 'r', encoding='utf-8').read().splitlines()
data = open('input', 'r', encoding='utf-8').read().splitlines()


def get_range_sections(section_assignment):
    return list(map(int, section_assignment.split('-')))


total_overlapping_sections = 0
for pair in data:
    elf1_sections, elf2_sections = pair.split(',')
    elf1_sections_from, elf1_sections_to = get_range_sections(elf1_sections)
    elf2_sections_from, elf2_sections_to = get_range_sections(elf2_sections)

    overlapping_sections = max(elf1_sections_from, elf2_sections_from) <= min(elf1_sections_to, elf2_sections_to)

    # overlapping_sections = list(
    #     range(max(elf1_sections_from, elf2_sections_from),
    #           min(elf1_sections_to, elf2_sections_to) + 1))

    if overlapping_sections:
        total_overlapping_sections += 1

print("Total of overlapping sections = ", total_overlapping_sections)
#  849
