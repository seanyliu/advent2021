# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

def is_a_win(board):
    for idx in range(5):
        # check a row
        if board[5*idx] == "*" and board[5*idx+1] == "*" and board[5*idx+2] == "*" and board[5*idx+3] == "*" and board[5*idx+4] == "*":
            return True

        # check a col
        if board[idx] == "*" and board[idx+5] == "*" and board[idx+10] == "*" and board[idx+15] == "*" and board[idx+20] == "*":
            return True
    return False

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
boards = []
draws = []

idx = 0
board = []
board_row = 0
for line in input_lines:
    if idx == 0:
        draws = line.split(',')
    elif line == "":
        # line break
        board = []
        board_row = 0
    else:
        for char in line.split(" "):
            if char != "":
                board.append(char)
        board_row = board_row + 1

        if board_row == 5:
            boards.append(board)
    idx = idx + 1

'''
found_win = False
for draw in draws:
    for board in boards:
        for idx in range(len(board)):
            if board[idx] == draw:
                board[idx] = "*"
        if is_a_win(board):
            print board
            found_win = True

            sum = 0
            for item in board:
                if item != "*":
                    sum = sum + int(item)
            print sum * int(draw)

            break
    if found_win:
        break
'''

# Part 2 #################################

winning_boards = []
for board in boards:
    winning_boards.append(False)

found_win = False
for draw in draws:
    for bidx in range(len(boards)):
        board = boards[bidx]

        for idx in range(len(board)):
            if board[idx] == draw:
                board[idx] = "*"
        if is_a_win(board):
            winning_boards[bidx] = True

        # check if all wins
        all_wins = True
        for win in winning_boards:
            if win == False:
                all_wins = False
                break

        if all_wins == True:
            sum = 0
            for item in board:
                if item != "*":
                    sum = sum + int(item)
            print sum * int(draw)
            found_win = True
            break

    if found_win:
        break
