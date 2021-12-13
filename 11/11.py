# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
def increment_grid(grid):
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y, max_y+1):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x, max_x+1):
            grid[x][y] = grid[x][y] + 1

def find_ten_in_grid(grid):
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y, max_y+1):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x, max_x+1):
            if grid[x][y] == 10:
                return [x, y]
    return False

def flash_ten(grid, x, y):
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    min_x = min(grid.keys())
    max_x = max(grid.keys())

    neighbors = [
        [0, -1],
        [0, 1],
        [-1, 0],
        [1, 0],
        [-1, -1],
        [-1, 1],
        [1, -1],
        [1, 1]
    ]

    for neighbor in neighbors:
        x_new = x + neighbor[0]
        y_new = y + neighbor[1]
        if x_new in grid:
            if y_new in grid[x_new]:
                if grid[x_new][y_new] <= 9:
                    grid[x_new][y_new] = grid[x_new][y_new] + 1

def clear_energy(grid):
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y, max_y+1):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x, max_x+1):
            if grid[x][y] >= 10:
                grid[x][y] = 0

def is_all_zeroes(grid):
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y, max_y+1):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x, max_x+1):
            if grid[x][y] != 0:
                return False
    return True

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
grid = helpers.get_grid_from_lines(input_lines)
grid = helpers.convert_grid_to_int(grid)

#helpers.print_grid(grid)

count = 0

#for step in range(100):
step = -1
while True:
    step = step + 1
    increment_grid(grid)

    contains_ten = True
    while contains_ten != False:
        contains_ten = find_ten_in_grid(grid)
        if contains_ten is False:
            break
        x = contains_ten[0]
        y = contains_ten[1]
        # expend your own energy
        grid[x][y] = grid[x][y] + 1
        flash_ten(grid, x, y)

        count = count + 1

        #print "\n post flash:"
        #helpers.print_grid(grid)


    clear_energy(grid)
    if is_all_zeroes(grid):
        print "All Zeroes"
        print str(step+1)
        break

    #print "\nStep "+str(step)
    #helpers.print_grid(grid)

#print "\nFinal: "
#helpers.print_grid(grid)

print count


# Part 2 #################################
