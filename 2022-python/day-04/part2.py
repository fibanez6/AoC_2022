# --- Day 4: Camp Cleanup ---

# data = open('input.test', 'r', encoding='utf-8').read().splitlines()
data = open('input', 'r', encoding='utf-8').read().splitlines()


def get_range_sections(section_assignment):
    return list(map(int, section_assignment.split('-')))


total_overlapping_sections = 0
for pair in data:
    # pair ['2-8','3-7']
    elves = pair.split(',')

    elf1_sections = get_range_sections(elves[0])
    elf2_sections = get_range_sections(elves[1])

    overlapping_sections = list(
        range(max(elf1_sections[0], elf2_sections[0]),
              min(elf1_sections[-1], elf2_sections[-1]) + 1))
    # print("overlapping_sections = ", overlapping_sections)

    if overlapping_sections:
        total_overlapping_sections += 1

print("Total of overlapping sections = ", total_overlapping_sections)
#  849
