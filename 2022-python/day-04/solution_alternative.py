# --- Day 4: Camp Cleanup ---

# For each section, generate a sequence of integers within a range
# It is less efficient

# data = open('input.test', 'r', encoding='utf-8').read().splitlines()
data = open('input', 'r', encoding='utf-8').read().splitlines()


def get_sections(section_assignment):
    #  Sample
    # section_assignment ['2-8']
    section_range = list(map(int, section_assignment.split('-')))

    # section_range [2,8]
    sections = list(range(section_range[0], section_range[1] + 1))

    # sections [2,3,4,5,6,7,8]
    return sections


def is_sublist(list1, list2):
    return set(list1) <= set(list2)


total_fully_contained = 0
total_overlapping_sections = 0
for pair in data:
    # pair ['2-8','3-7']
    elves = pair.split(',')

    elf1_sections = get_sections(elves[0])
    elf2_sections = get_sections(elves[1])

    is_fully_contained = is_sublist(elf1_sections, elf2_sections) or is_sublist(elf2_sections, elf1_sections)
    if is_fully_contained:
        total_fully_contained += 1

    overlapping_sections = set(elf1_sections).intersection(elf2_sections)
    if overlapping_sections:
        total_overlapping_sections += 1

# PART 1
print("Total of sections fully contained = ", total_fully_contained)
#  487

# PART 2
print("Total of overlapping sections = ", total_overlapping_sections)
#  849