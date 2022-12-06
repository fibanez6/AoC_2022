# --- Day 4: Camp Cleanup ---

# For each section, generate a sequence of integers within a range
# It is less efficient

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def get_sections(section_range):
    #  Sample
    # section_range ['2-8']
    section_from, section_to = list(map(int, section_range.split('-')))

    # section_from = 2, section_to = 8
    sections = list(range(section_from, section_to + 1))

    # sections [2,3,4,5,6,7,8]
    return sections


def run(data):
    total_fully_contained = 0
    total_overlapping_sections = 0
    for pair in data:
        # pair ['2-8','3-7']
        elf1, elf2 = pair.split(',')

        elf1_sections = set(get_sections(elf1))
        elf2_sections = set(get_sections(elf2))

        if DEBUG:
            print("Elf1 sections =", elf1_sections)
            print("Elf2 sections =", elf2_sections)

        # PART 1
        # total_fully_contained += 1 if elf1_sections <= elf2_sections or elf2_sections <= elf1_sections else 0
        total_fully_contained += 1 if elf1_sections.issubset(elf2_sections) or \
                                      elf1_sections.issuperset(elf2_sections) else 0

        # PART 2
        # total_overlapping_sections += 1 if elf1_sections.intersection(elf2_sections) else 0
        total_overlapping_sections += 1 if elf1_sections & elf2_sections else 0

    return total_fully_contained, total_overlapping_sections


data = open(CTX['file'], 'r', encoding='utf-8').read().splitlines()
total_fully_contained, total_overlapping_sections = run(data)

# PART 1
print("PART 1 - Total of sections fully contained =", total_fully_contained)
# 487

# PART 2
print("PART 2 - Total of overlapping sections =", total_overlapping_sections)
# 849
