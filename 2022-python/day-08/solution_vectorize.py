# --- Day 8: Treetop Tree House ---
"""
    @Author: wmvanvliet
    @Source: Redit
"""
import numpy as np

DEBUG = False
TEST = {'file': 'input.test'}
INPUT = {'file': 'input'}
CTX = TEST

with open(CTX['file']) as f:
    forest = np.array([[int(x) for x in list(line.strip())] for line in f])


def look_along(x):
    return x > np.hstack((-1, np.maximum.accumulate(x)[:-1]))


is_visible = np.apply_along_axis(look_along, 0, forest)
is_visible |= np.apply_along_axis(look_along, 1, forest)
is_visible |= np.apply_along_axis(look_along, 0, forest[::-1, :])[::-1, :]
is_visible |= np.apply_along_axis(look_along, 1, forest[:, ::-1])[:, ::-1]

print('Day 8, part 1:', is_visible.sum())


def compute_scenic_score(candidate_tree):
    height = forest[candidate_tree]
    row, col = candidate_tree
    if row == 0 or col == 0 or row == forest.shape[0] - 1 or col == forest.shape[1] - 1:
        return 0

    if DEBUG: print("candidate_tree:", candidate_tree)
    score = (np.maximum.accumulate(forest[row - 1:0:-1, col]) < height).sum() + 1  # TOP
    score *= (np.maximum.accumulate(forest[row, col + 1:-1]) < height).sum() + 1  # RIGHT
    score *= (np.maximum.accumulate(forest[row + 1:-1, col]) < height).sum() + 1  # BOTTOM
    score *= (np.maximum.accumulate(forest[row, col - 1:0:-1]) < height).sum() + 1  # LEFT
    return score


# The Elves don't care about distant trees taller than those found by the rules above (PART 1);
# the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.
scenic_scores = [compute_scenic_score(tree) for tree in zip(*np.nonzero(is_visible))]
print('Day 8, part 2:', np.max(scenic_scores))
