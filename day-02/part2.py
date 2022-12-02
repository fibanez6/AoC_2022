# --- Day 2: Rock Paper Scissors ---

#  Rock Paper Scissors representation
# [A, X] for Rock,
# [B, Y] for Paper,
# [C, Z] for Scissors

# Game Scores
# X means you need to lose (0 if you lost),
# Y means you need to end the round in a draw, and (3 if the round was a draw)
# Z means you need to win (6 if you won)
gameScore = {'X': 0, 'Y': 3, 'Z': 6}

# Shape Scores
# 1 for Rock, 2 for Paper, 3 for Scissors
shapeScores = {'X': 1, 'Y': 2, 'Z': 3}

# Shape to choose
# Matrix:
#
# - | A         | B         | C
# X | Scissors  | Rock      | Paper
# Y | Rock      | Paper     | Scissors
# Z | Paper     | Scissors  | Rock
shapeChoice = {'X': {'A': 'Z', 'B': 'X', 'C': 'Y'},
               'Y': {'A': 'X', 'B': 'Y', 'C': 'Z'},
               'Z': {'A': 'Y', 'B': 'Z', 'C': 'X'}}

totalScore = 0
with open('input', 'r', encoding='utf-8') as game:
    for round in game:
        p0, p1 = round.split()
        shape = shapeChoice.get(p1).get(p0)
        totalScore += shapeScores.get(shape) + gameScore.get(p1)

print("Total score =", totalScore)
#  11998
