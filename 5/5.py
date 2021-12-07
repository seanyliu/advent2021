# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
def init_coords(coords, x1, y1, idx_x, idx_y):

    if str(x1)+","+str(y1) not in coords:
        coords[str(x1)+','+str(y1)] = 0

    for idx in range(idx_x):
        x_new = int(x1) + idx + 1
        y_new = y1
        if str(x_new)+","+str(y_new) not in coords:
            coords[str(x_new)+','+str(y_new)] = 0

    for idx in range(idx_y):
        x_new = x1
        y_new = int(y1) + idx + 1
        if str(x_new)+","+str(y_new) not in coords:
            coords[str(x_new)+','+str(y_new)] = 0

    # initialize diagonal
    for idx in range(idx_y):
        x_new = x1 + idx + 1
        y_new = int(y1) + idx + 1
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
input_lines = helpers.read_lines_from_file('input_test.txt')

# Part 1 #################################

'''
coords = {}

for line in input_lines:

    start = line.split('->')[0]
    end = line.split('->')[1]

    ori_x1 = int(start.split(',')[0])
    ori_y1 = int(start.split(',')[1])
    ori_x2 = int(end.split(',')[0])
    ori_y2 = int(end.split(',')[1])

    x1 = ori_x1
    y1 = ori_y1
    x2 = ori_x2
    y2 = ori_y2

    if x1 == x2:
        if y2 - y1 < 0:
            x1 = ori_x2
            y1 = ori_y2
            x2 = ori_x1
            y2 = ori_y1

    if y1 == y2:
        if x2 - x1 < 0:
            x1 = ori_x2
            y1 = ori_y2
            x2 = ori_x1
            y2 = ori_y1

    # initialize all the starting coordinates
    if x1 == x2 or y1 == y2:
        coords = init_coords(coords, x1, y1, int(x2) - int(x1), int(y2) - int(y1))

    # increment the starting position by one
    if x1 == x2 or y1 == y2:
        coords[str(x1)+','+str(y1)] = coords[str(x1)+','+str(y1)] + 1

    if x1 == x2:
        for idx in range(y2 - y1):
            coords[str(x1)+','+str(y1+idx+1)] = coords[str(x1)+','+str(y1+idx+1)] + 1

    elif y1 == y2:
        for idx in range(x2 - x1):
            coords[str(x1+idx+1)+','+str(y1)] = coords[str(x1+idx+1)+','+str(y1)] + 1

# print coords
for y in range(get_max_y(coords) + 1):
    row = ""
    for x in range(get_max_x(coords) + 1):
        if str(x)+','+str(y) in coords:
            row = row + str(coords[str(x)+','+str(y)])
        else:
            row = row + "."
    print row

count = 0
for key in coords:
    if coords[key] > 1:
        count = count + 1

print count
'''

# Part 2 #################################

coords = {}

for line in input_lines:

    start = line.split('->')[0]
    end = line.split('->')[1]

    ori_x1 = int(start.split(',')[0])
    ori_y1 = int(start.split(',')[1])
    ori_x2 = int(end.split(',')[0])
    ori_y2 = int(end.split(',')[1])

    x1 = ori_x1
    y1 = ori_y1
    x2 = ori_x2
    y2 = ori_y2

    if x2 - x1 < 0 or y2 - y1 < 0:
        x1 = ori_x2
        y1 = ori_y2
        x2 = ori_x1
        y2 = ori_y1

    # initialize all the starting coordinates
    if x1 == x2 or y1 == y2 or x2-x1 == y2-y1:
        coords = init_coords(coords, x1, y1, int(x2) - int(x1), int(y2) - int(y1))

    # increment the starting position by one
    if x1 == x2 or y1 == y2 or x2-x1 == y2-y1:
        coords[str(x1)+','+str(y1)] = coords[str(x1)+','+str(y1)] + 1

    if x1 == x2:
        for idx in range(y2 - y1):
            coords[str(x1)+','+str(y1+idx+1)] = coords[str(x1)+','+str(y1+idx+1)] + 1

    elif y1 == y2:
        for idx in range(x2 - x1):
            coords[str(x1+idx+1)+','+str(y1)] = coords[str(x1+idx+1)+','+str(y1)] + 1

    elif x2-x1 == y2-y1:
        for idx in range(x2 - x1):
            coords[str(x1+idx+1)+','+str(y1+idx+1)] = coords[str(x1+idx+1)+','+str(y1+idx+1)] + 1

# print coords
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

count = 0
for key in coords:
    if coords[key] > 1:
        count = count + 1

print count
