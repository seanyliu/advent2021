# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################

first_line = input_lines[0]
gamma = ""
epsilon = ""
for char_idx in range(len(first_line)):
    count0 = 0
    count1 = 0
    for line in input_lines:
        char = line[char_idx]
        if char == "0":
            count0 = count0 + 1
        elif char == "1":
            count1 = count1 + 1
    if count0 > count1:
        gamma = gamma + "0"
        epsilon = epsilon + "1"
    else:
        gamma = gamma + "1"
        epsilon = epsilon + "0"
print int(gamma, 2) * int(epsilon, 2)

# Part 2 #################################

# build up a seed of the current lines
current_lines = []
for line in input_lines:
    current_lines.append(line)

first_line = input_lines[0]

for char_idx in range(len(first_line)):

    count0 = 0
    count1 = 0
    for line in current_lines:
        char = line[char_idx]
        if char == "0":
            count0 = count0 + 1
        elif char == "1":
            count1 = count1 + 1

    keep_digit = ""
    if count0 > count1:
        keep_digit = "0"
    elif count1 > count0:
        keep_digit = "1"
    else:
        keep_digit = "1"

    keep_lines = []
    for line in current_lines:
        if line[char_idx] == keep_digit:
            keep_lines.append(line)

    current_lines = keep_lines

# oxygen generator rating
oxygen_generator_rating = int(current_lines[0], 2)
print oxygen_generator_rating

# build up a seed of the current lines
current_lines = []
for line in input_lines:
    current_lines.append(line)

first_line = input_lines[0]

for char_idx in range(len(first_line)):

    count0 = 0
    count1 = 0
    if len(current_lines) == 1:
        break

    for line in current_lines:
        char = line[char_idx]
        if char == "0":
            count0 = count0 + 1
        elif char == "1":
            count1 = count1 + 1

    keep_digit = ""
    if count0 > count1:
        keep_digit = "1"
    elif count1 > count0:
        keep_digit = "0"
    else:
        keep_digit = "0"

    keep_lines = []
    for line in current_lines:
        if line[char_idx] == keep_digit:
            keep_lines.append(line)

    current_lines = keep_lines

# CO2 scrubber rating
co2_rating = int(current_lines[0], 2)
print co2_rating

print oxygen_generator_rating * co2_rating
