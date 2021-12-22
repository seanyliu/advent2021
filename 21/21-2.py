# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
class Dice:
    def __init__(self):
        self.value = 1
        self.rolls = 0

    def roll(self):
        val = self.value
        self.value += 1
        if (self.value > 100):
            self.value = 1
        self.rolls += 1
        return val

def movePlayer(start, spaces):
    newPos = start + (spaces % 10)
    if newPos > 10:
        newPos -= 10
    return newPos


# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')
player1Pos = int(input_lines[0].split(": ")[1])
player2Pos = int(input_lines[1].split(": ")[1])
print("player1StartPos", player1Pos, "player2StartPos", player2Pos)

distributions = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1}
'''
distributions = {}
for i in range(3):
    for j in range(3):
        for k in range(3):
            roll1 = i+1
            roll2 = j+1
            roll3 = k+1
            total = roll1+roll2+roll3
            if total not in distributions:
                distributions[total] = 1
            else:
                distributions[total] += 1
print distributions
'''

# memoize player1Pos, player2Pos, player1Score, player2Score [output]
memoize = {}

# return # of universes in which player 1 wins, # of universes in which player 2 wins
def countUnivWins(player1Pos, player2Pos, player1Score, player2Score):

    # check if we already saw a solution
    key = str((player1Pos, player2Pos, player1Score, player2Score))
    if key in memoize:
        return memoize[key]

    # calculate number of wins
    player1Wins = 0
    player2Wins = 0

    # player 1 rolls
    for rolls1 in distributions.keys():
        count1 = distributions[rolls1]
        player1PosNext = movePlayer(player1Pos, rolls1)
        player1ScoreNext = player1Score + player1PosNext
        if player1ScoreNext >= 21:
            player1Wins += count1
            continue

        for rolls2 in distributions.keys():
            count2 = distributions[rolls2]
            player2PosNext = movePlayer(player2Pos, rolls2)
            player2ScoreNext = player2Score + player2PosNext
            if player2ScoreNext >= 21:
                player2Wins += count2
                continue

            # neither player won
            scores = countUnivWins(player1PosNext, player2PosNext, player1ScoreNext, player2ScoreNext)
            player1Wins += scores[0] * count1 * count2
            player2Wins += scores[1] * count1 * count2

    memoize[key] = (player1Wins, player2Wins)
    return (player1Wins, player2Wins)

print max(countUnivWins(player1Pos, player2Pos, 0, 0))

'''
# universe = tuple(player1Pos, player2Pos, player1Score, player2Score, countOfUniverses)
universes = []
universes.append((player1Pos, player2Pos, 0, 0, 1))

player1WinningUniversesCount = 0
player2WinningUniversesCount = 0

stopCount = 0
while(len(universes) > 0 and stopCount < 100):
    if stopCount == 99:
        for u in universes:
            print u

    stopCount += 1
    u = universes.pop()

    player1Pos = u[0]
    player2Pos = u[1]
    player1Score = u[2]
    player2Score = u[3]
    countOfUniverses = u[4]

    # player 1 rolls
    for rolls1 in distributions.keys():
        count1 = distributions[rolls1]

        player1PosNext = movePlayer(player1Pos, rolls1)
        player1ScoreNext = player1Score + player1PosNext
        countOfUniversesNext = countOfUniverses * count1
        if player1ScoreNext >= 21:
            player1WinningUniversesCount += countOfUniversesNext
            continue

        for rolls2 in distributions.keys():
            count2 = distributions[rolls2]
            player2PosNext = movePlayer(player2Pos, rolls2)
            player2ScoreNext = player2Score + player2PosNext
            countOfUniversesNext2 = countOfUniversesNext * count2
            if player2ScoreNext >= 21:
                player2WinningUniversesCount += countOfUniversesNext2
                continue

            # neither player won
            universes.append((player1PosNext, player2PosNext, player1ScoreNext, player2ScoreNext, countOfUniversesNext2))

print ("player1WinningUniversesCount", player1WinningUniversesCount, "player2WinningUniversesCount", player2WinningUniversesCount)
'''





'''
player1Score = 0
player2Score = 0
die = Dice()

while player1Score < 1000 and player2Score < 1000:
    rolls = die.roll() + die.roll() + die.roll()
    player1Pos = movePlayer(player1Pos, rolls)
    player1Score += player1Pos

    if player1Score >= 1000:
        break

    rolls = die.roll() + die.roll() + die.roll()
    player2Pos = movePlayer(player2Pos, rolls)
    player2Score += player2Pos

print("player1Score", player1Score, "player2Score", player2Score, "dice rolls", die.rolls)
print min(player1Score, player2Score) * die.rolls
'''

# Part 1 #################################

# Part 2 #################################
