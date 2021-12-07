# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

def unit_dir(a, b):
    # return 1 if b>a, and -1 if b<a
    if b > a:
        return 1
    elif b < a:
        return -1
    else:
        return 0

# print coords
def print_coords(coords):
    for y in range(get_max_y(coords) + 1):
        row = ""
        for x in range(get_max_x(coords) + 1):
            if str(x)+','+str(y) in coords:
                if coords[str(x)+','+str(y)] != 0:
                    row = row + str(coords[str(x)+','+str(y)])
                else:
                    row = row + "."
            else:
                row = row + "."
        print row

def init_coords2(coords, x1, y1, x2, y2):
    x_dir = unit_dir(x1, x2)
    y_dir = unit_dir(y1, y2)

    # initialize the start
    if str(x1)+","+str(y1) not in coords:
        coords[str(x1)+','+str(y1)] = 0

    # initialize the first row (case: horizontal line)
    for x_idx in range(abs(x2 - x1)):
        x_new = x1 + (x_dir * (x_idx + 1))
        y_new = y2
        if str(x_new)+","+str(y_new) not in coords:
            coords[str(x_new)+','+str(y_new)] = 0

    # initialize the first column (case: vertical line)
    for y_idx in range(abs(y2 - y1)):
        x_new = x2
        y_new = y1 + (y_dir * (y_idx + 1))
        if str(x_new)+","+str(y_new) not in coords:
            coords[str(x_new)+','+str(y_new)] = 0

    # initialize all points between the two sets of points
    if abs(x2-x1) == abs(y2-y1):
        x_dir = unit_dir(x1, x2)
        y_dir = unit_dir(y1, y2)

        for idx in range(abs(x2 - x1)):
            x_new = x1 + (x_dir * (idx + 1))
            y_new = y1 + (y_dir * (idx + 1))
            if str(x_new)+","+str(y_new) not in coords:
                coords[str(x_new)+','+str(y_new)] = 0

    return coords

def get_max_x(coords):
    max_x = 0
    for key in coords:
        x = int(key.split(",")[0])
        if x > max_x:
            max_x = x
    return max_x

def get_max_y(coords):
    max_y = 0
    for key in coords:
        y = int(key.split(",")[1])
        if y > max_y:
            max_y = y
    return max_y


# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 2 #################################

coords = {}

for line in input_lines:

    start = line.split('->')[0]
    end = line.split('->')[1]

    x1 = int(start.split(',')[0])
    y1 = int(start.split(',')[1])
    x2 = int(end.split(',')[0])
    y2 = int(end.split(',')[1])

    x_dir = unit_dir(x1, x2)
    y_dir = unit_dir(y1, y2)

    # initialize all the starting coordinates
    if x1 == x2 or y1 == y2 or abs(x2-x1) == abs(y2-y1):
        coords = init_coords2(coords, x1, y1, x2, y2)

    # increment the starting position by one
    if x1 == x2 or y1 == y2 or abs(x2-x1) == abs(y2-y1):
        coords[str(x1)+','+str(y1)] = coords[str(x1)+','+str(y1)] + 1

    if x1 == x2:
        for idx in range(abs(y2 - y1)):
            x_new = x1
            y_new = y1 + (y_dir * (idx + 1))
            coords[str(x_new)+','+str(y_new)] = coords[str(x_new)+','+str(y_new)] + 1

    elif y1 == y2:
        for idx in range(abs(x2 - x1)):
            x_new = x1 + (x_dir * (idx + 1))
            y_new = y1
            coords[str(x_new)+','+str(y_new)] = coords[str(x_new)+','+str(y_new)] + 1

    elif abs(x2-x1) == abs(y2-y1):
        #print str(str(x1) + "," + str(y1)) + " to " + str(str(x2) + "," + str(y2))

        for idx in range(abs(x2 - x1)):
            x_new = x1 + (x_dir * (idx + 1))
            y_new = y1 + (y_dir * (idx + 1))
            #print (str(x_new) + "," + str(y_new))
            coords[str(x_new)+','+str(y_new)] = coords[str(x_new)+','+str(y_new)] + 1

#print_coords(coords)

count = 0
for key in coords:
    if coords[key] > 1:
        count = count + 1

print count
