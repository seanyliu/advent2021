# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################

# initialize grid
grid = {}

# get maximum x
max_x = 0
for line in input_lines:
    if line == "":
        break
    x = int(line.split(",")[0])
    if x > max_x:
        max_x = x

# get maximum y
max_y = 0
for line in input_lines:
    if line == "":
        break
    y = int(line.split(",")[1])
    if y > max_y:
        max_y = y

helpers.init_grid(grid, max_x, max_y, ".")

# fill grid and get fold lines
processing_points = True
fold_lines = []
for line in input_lines:
    if line == "":
        processing_points = False
        continue
    if processing_points:
        helpers.add_to_grid(int(line.split(",")[0]), int(line.split(",")[1]), "#", grid)
    else:
        fold_lines.append(line.split("along ")[1])

# process folds
for fold in fold_lines:
    #print("processing "+fold)
    axis = fold.split("=")[0]
    value = int(fold.split("=")[1])

    # extract the either upper or left piece of the grid
    base_grid = {}
    max_x = max(grid.keys())
    max_y = max(grid[0].keys())
    if axis == "y":
        max_y = value - 1
    elif axis == "x":
        max_x = value - 1
    base_grid = helpers.copy_grid_partial(grid, 0, 0, max_x, max_y)
    #helpers.print_grid(base_grid)

    #print("---")

    # extract the lower or right piece of the grid to fold
    fold_grid = {}
    max_x = max(grid.keys())
    max_y = max(grid[0].keys())
    min_x = 0
    min_y = 0
    if axis == "y":
        min_y = value + 1
    elif axis == "x":
        min_x = value + 1
    fold_grid = helpers.copy_grid_partial(grid, min_x, min_y, max_x, max_y)
    #helpers.print_grid(fold_grid)

    #print("--post fold--")

    base_x_max = max(base_grid.keys())
    base_y_max = max(base_grid[0].keys())
    for x in range(max(fold_grid.keys())+1):
        for y in range(max(fold_grid[0].keys())+1):
            base_x = x
            base_y = y

            if axis == "y":
                base_y = base_y_max - y
            if axis == "x":
                base_x = base_x_max - x

            if fold_grid[x][y] == "#":
                base_grid[base_x][base_y] = "#"

    grid = base_grid
    #helpers.print_grid(base_grid)

def count_grid(grid):
    count = 0
    for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] == "#":
                count = count + 1
    return count

#print count_grid(grid)



helpers.print_grid(grid)


# Part 2 #################################
