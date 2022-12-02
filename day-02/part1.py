# --- Day 2: Rock Paper Scissors ---

#  Rock Paper Scissors representation
# [A, X] for Rock,
# [B, Y] for Paper,
# [C, Z] for Scissors

# Game Scores
# 0 if you lost,
# 3 if the round was a draw, and
# 6 if you won
#
# Matrix:
#
# - | A    | B    | C
# X | draw | lost | won
# Y | won  | draw | lost
# Z | lost | won  | draw
gameScore = {'X': {'A': 3, 'B': 0, 'C': 6},
             'Y': {'A': 6, 'B': 3, 'C': 0},
             'Z': {'A': 0, 'B': 6, 'C': 3}}

# Shape Scores
# 1 for Rock, 2 for Paper, 3 for Scissors
shapeScores = {'X': 1, 'Y': 2, 'Z': 3}

totalScore = 0
with open('input', 'r', encoding='utf-8') as game:
    for round in game:
        p0, p1 = round.split()
        totalScore += shapeScores.get(p1) + gameScore.get(p1).get(p0)

print("Total score =", totalScore)
# 8933
