# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
crab_positions = input_lines[0].split(",")
crab_positions = helpers.convert_array_to_int(crab_positions)

fuel_to_align_to = {}

for position in range(max(crab_positions)):

    # skip if we already calculated
    if position in fuel_to_align_to:
        continue

    # calculate fuel cost
    total_cost = 0
    for position2 in crab_positions:

        cost = abs(position2 - position)

        # part 2
        cost = cost * (cost + 1) / 2

        total_cost = total_cost + cost

    fuel_to_align_to[position] = total_cost

print fuel_to_align_to
print min(fuel_to_align_to.values())


# Part 2 #################################
