# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
heightmap = helpers.get_grid_from_lines(input_lines)

lowpoints = []
lowpoint_coords = []

min_y = min(heightmap[0].keys())
max_y = max(heightmap[0].keys())
for y in range(min_y, max_y+1):
    min_x = min(heightmap.keys())
    max_x = max(heightmap.keys())
    for x in range(min_x, max_x+1):
        is_lowpoint = True

        # up
        if y-1 >= min_y and heightmap[x][y-1] <= heightmap[x][y]:
            is_lowpoint = False

        # right
        if x+1 <= max_x and heightmap[x+1][y] <= heightmap[x][y]:
            is_lowpoint = False

        # down
        if y+1 <= max_y and heightmap[x][y+1] <= heightmap[x][y]:
            is_lowpoint = False

        # left
        if x-1 >= min_x and heightmap[x-1][y] <= heightmap[x][y]:
            is_lowpoint = False

        if is_lowpoint:
            lowpoints.append(heightmap[x][y])
            lowpoint_coords.append([x, y])

sum = 0
for point in lowpoints:
    sum = sum + int(point) + 1

print sum

# Part 2 #################################

def get_basin_size(start, heightmap):
    size = 0
    c = helpers.copy_grid(heightmap)
    helpers.convert_grid_to_int(c)
    queue = []
    queue.append(start)
    while len(queue) > 0:
        vertex = queue.pop()
        x = vertex[0]
        y = vertex[1]
        min_y = min(c[0].keys())
        max_y = max(c[0].keys())
        min_x = min(c.keys())
        max_x = max(c.keys())
        if c[x][y] == 9:
            # 9 is not part of any basin
            continue
        elif c[x][y] == ".":
            # somehow already visited
            continue
        else:
            # append any of the other entries to the search
            # up
            if y-1 >= min_y and c[x][y-1] != "." and c[x][y-1] >= c[x][y]:
                queue.append([x, y-1])

            # right
            if x+1 <= max_x and c[x+1][y] != "." and c[x+1][y] >= c[x][y]:
                queue.append([x+1, y])

            # down
            if y+1 <= max_y and c[x][y+1] != "." and c[x][y+1] >= c[x][y]:
                queue.append([x, y+1])

            # left
            if x-1 >= min_x and c[x-1][y] != "." and c[x-1][y] >= c[x][y]:
                queue.append([x-1, y])

            c[x][y] = "."
            size = size + 1
    return size

basins = []
for point in lowpoint_coords:
    basins.append(get_basin_size(point, heightmap))

basins.sort()

print basins.pop() * basins.pop() * basins.pop()

'''
c = helpers.copy_grid(heightmap)
helpers.convert_grid_to_int(c)
helpers.print_grid(c)

queue = []
queue.append([2, 2])
while len(queue) > 0:
    vertex = queue.pop()
    x = vertex[0]
    y = vertex[1]
    print "analyzing vertex ["+str(x)+", "+str(y)+"]"
    min_y = min(c[0].keys())
    max_y = max(c[0].keys())
    min_x = min(c.keys())
    max_x = max(c.keys())
    if c[x][y] == 9:
        # 9 is not part of any basin
        continue
    elif c[x][y] == ".":
        # somehow already visited
        continue
    else:
        # append any of the other entries to the search
        # up
        if y-1 >= min_y and c[x][y-1] != "." and c[x][y-1] >= c[x][y]:
            queue.append([x, y-1])

        # right
        if x+1 <= max_x and c[x+1][y] != "." and c[x+1][y] >= c[x][y]:
            queue.append([x+1, y])

        # down
        if y+1 <= max_y and c[x][y+1] != "." and c[x][y+1] >= c[x][y]:
            queue.append([x, y+1])

        # left
        if x-1 >= min_x and c[x-1][y] != "." and c[x-1][y] >= c[x][y]:
            queue.append([x-1, y])

        c[x][y] = "."
helpers.print_grid(c)
'''
