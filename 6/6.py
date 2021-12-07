# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################

lantern_fish = helpers.convert_array_to_int(input_lines[0].split(","))
print lantern_fish

for day in range(256):

    total_fish = len(lantern_fish)
    for idx in range(total_fish):
        fish = lantern_fish[idx]
        if fish == 0:
            lantern_fish.append(8)
            lantern_fish[idx] = 6
        else:
            lantern_fish[idx] = fish - 1

    # print
    day_str = day + 1
    if day_str < 10:
        day_str = " " +str(day_str)
    else:
        day_str = str(day_str)
    #print "After " + day_str + " days: " + str(lantern_fish)

print(len(lantern_fish))

# Part 2 #################################
