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

# Part 1 #################################

# Part 2 #################################
