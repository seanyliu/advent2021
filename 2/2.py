# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
depth = 0
horizontal = 0
for line in input_lines:
  direction = line.split(' ')[0]
  x = int(line.split(' ')[1])
  if direction == 'forward':
    horizontal = horizontal + x
  elif direction == 'down':
    depth = depth + x
  elif direction == 'up':
    depth = depth - x
print depth * horizontal

# Part 2 #################################
depth = 0
horizontal = 0
aim = 0
for line in input_lines:
  direction = line.split(' ')[0]
  x = int(line.split(' ')[1])
  if direction == 'forward':
    horizontal = horizontal + x
    depth = depth + (aim * x)
  elif direction == 'down':
    aim = aim + x
  elif direction == 'up':
    aim = aim - x
print horizontal * depth
