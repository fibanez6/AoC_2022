# --- Day 8: Treetop Tree House ---

import numpy as np

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = INPUT

with open(CTX['file'], 'r') as data:
    forest = np.array([[int(v) for v in [*line.strip()]] for line in data])

if DEBUG: print("Forest:\n", forest)

# PART 1
row_size, col_size = forest.shape
is_visible_grid = np.array([[True] * row_size] * col_size)
is_visible_grid[1:-1, 1:-1] = False


def is_tree_visible(candidate_tree):
    height = forest[candidate_tree]
    row, col = candidate_tree

    is_visible = all(forest[:row, col] < height)  # TOP
    is_visible |= all(forest[row, col + 1:] < height)  # RIGHT
    is_visible |= all(forest[row + 1:, col] < height)  # BOTTOM
    is_visible |= all(forest[row, :col] < height)  # LEFT

    if is_visible:
        if DEBUG: print("Tree:", candidate_tree, "=", height, "is VISIBLE")
        is_visible_grid[row, col] = True


for tree in zip(*np.nonzero(np.invert(is_visible_grid))):
    is_tree_visible(tree)

if DEBUG:
    print("\nVisibility:")
    print(is_visible_grid)

print("\nPART 1 - How many trees are visible from outside the grid?", is_visible_grid.sum())
# 1698


# PART 2
def compute_scenic_score(candidate_tree):
    height = forest[candidate_tree]
    row, col = candidate_tree

    # Skip the trees from the edges
    if row == 0 or col == 0 or row == row_size - 1 or col == col_size - 1:
        return 0

    score = (np.maximum.accumulate(forest[row - 1:0:-1, col]) < height).sum() + 1  # TOP
    score *= (np.maximum.accumulate(forest[row, col + 1:-1]) < height).sum() + 1  # RIGHT
    score *= (np.maximum.accumulate(forest[row + 1:-1, col]) < height).sum() + 1  # BOTTOM
    score *= (np.maximum.accumulate(forest[row, col - 1:0:-1]) < height).sum() + 1  # LEFT

    if DEBUG: print("Tree:", candidate_tree, "=", height, "score:", score)
    return score


if DEBUG: print("\nPART 2\n Forest:\n", forest)

# The Elves don't care about distant trees taller than those found by the rules above (PART 1);
# So, we re-use the is_visible_grid
scenic_scores = [compute_scenic_score(tree) for tree in zip(*np.nonzero(is_visible_grid))]
print("\nPART 2 - What is the highest scenic score possible for any tree?", np.max(scenic_scores))
# 672280
