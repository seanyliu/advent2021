# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')
target_coords = input_lines[0].split(": ")[1]
target_coords_x = target_coords.split(", ")[0].split("=")[1]
target_coords_y = target_coords.split(", ")[1].split("=")[1]
target_min_x = int(target_coords_x.split("..")[0])
target_max_x = int(target_coords_x.split("..")[1])
target_min_y = int(target_coords_y.split("..")[0])
target_max_y = int(target_coords_y.split("..")[1])
print("target_coords_x", target_coords_x, "target_coords_y", target_coords_y)
print("target_min_x", target_min_x, "target_max_x", target_max_x)
print("target_min_y", target_min_y, "target_max_y", target_max_y)

def trajectory_max_y(velocity):
    pos = (0, 0)
    max_y_achieved = 0
    while True:
        pos = (pos[0] + velocity[0], pos[1] + velocity[1])
        if pos[1] > max_y_achieved:
            max_y_achieved = pos[1]
        velocity = (velocity[0] - 1 if velocity[0] > 0 else velocity[0], velocity[1] - 1)
        #print("position", pos, "velocity", velocity)
        if pos[0] in range(target_min_x, target_max_x+1) and pos[1] in range(target_min_y, target_max_y+1):
            #print("In target range")
            return max_y_achieved
        elif pos[0] > target_max_x or pos[1] < target_min_y:
            #print("Over shot")
            return -1

# Part 1 #################################
velocity = (0, 0)
#print trajectory_max_y(velocity)

working_velocities = set()

print ("target_max_x", target_max_x+1)
print ("xrange", range(1, target_max_x+1))
print ("yrange", range(-abs(target_min_y), abs(target_min_y)+1))
max_y_achieved = 0
for testVelX in range(1, target_max_x+1):
    for testVelY in range(-abs(target_min_y), abs(target_min_y)+1):
        testY = trajectory_max_y((testVelX, testVelY))
        if testY > -1:
            if (testVelX, testVelY) not in working_velocities:
                working_velocities.add((testVelX, testVelY))
            if testY > max_y_achieved:
                max_y_achieved = testY

test_sets = '''23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7'''
'''
for line in test_sets.split("\n"):
    for coord in line.split(" "):
        if coord == "":
            continue
        x = int(coord.split(",")[0])
        y = int(coord.split(",")[1])
        if (x, y) not in working_velocities:
            print("not in", (x, y))
'''

print max_y_achieved
print len(working_velocities)
# max number of steps you can take: target_max_x (if you moved 1 step every time)
#


# Part 2 #################################
