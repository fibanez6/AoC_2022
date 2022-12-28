# --- Day 4: Camp Cleanup ---

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT


def get_range_sections(section_assignment):
    return list(map(int, section_assignment.split('-')))


def run(data):
    total_fully_contained = 0
    total_overlapping_sections = 0
    for pair in data:
        elf1_sections, elf2_sections = pair.split(',')
        elf1_sections_from, elf1_sections_to = get_range_sections(elf1_sections)
        elf2_sections_from, elf2_sections_to = get_range_sections(elf2_sections)

        if DEBUG:
            print("Elf1 sections =", elf1_sections)
            print("Elf2 sections =", elf2_sections)

        # PART 1
        if (elf1_sections_from <= elf2_sections_from and elf1_sections_to >= elf2_sections_to) or (
                elf1_sections_from >= elf2_sections_from and elf1_sections_to <= elf2_sections_to):
            total_fully_contained += 1

        # PART 2
        overlapping_sections = max(elf1_sections_from, elf2_sections_from) <= min(elf1_sections_to, elf2_sections_to)

        # overlapping_sections = list(
        #     range(max(elf1_sections_from, elf2_sections_from),
        #           min(elf1_sections_to, elf2_sections_to) + 1))

        if overlapping_sections:
            total_overlapping_sections += 1

    return total_fully_contained, total_overlapping_sections


data = open(CTX['file'], 'r', encoding='utf-8').read().splitlines()
total_fully_contained, total_overlapping_sections = run(data)

# PART 1
print(f'PART 1 - Total of sections fully contained = {total_fully_contained}')
# 487

# PART 2
print(f'PART 2 - Total of overlapping sections =  {total_overlapping_sections}')
# 849
