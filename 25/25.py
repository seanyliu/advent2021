# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

def step(grid, direction):
    new_grid = helpers.init_grid(max(grid.keys()), max(grid[0].keys()), ".")
    for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] == direction:
                if direction == ">":
                    check_x = (x + 1) % (max(grid.keys()) + 1)
                    check_y = y
                    if grid[check_x][check_y] == ".":
                        new_grid[check_x][check_y] = direction
                    else:
                        new_grid[x][y] = direction
                elif direction == "v":
                    check_x = x
                    check_y = (y + 1) % (max(grid[0].keys()) + 1)
                    #print("v", check_x, check_y)
                    if grid[check_x][check_y] == ".":
                        #print("free")
                        new_grid[check_x][check_y] = direction
                        #helpers.print_grid(new_grid)
                        #print("--")
                    else:
                        new_grid[x][y] = direction
            elif grid[x][y] != ".":
                new_grid[x][y] = grid[x][y]
    return new_grid

def isSame(grid, grid2):
    for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] != grid2[x][y]:
                return False
    return True

# Part 1 #################################
grid = helpers.get_grid_from_lines(input_lines)
print("initial")
helpers.print_grid(grid)

count = 0
while True:
    count += 1
    #print("count", count)

    g1 = step(grid, ">")
    #helpers.print_grid(g1)
    #print("#")
    g2 = step(g1, "v")

    if isSame(grid, g2):
        print("Finished", count)
        break

    grid = g2
    #helpers.print_grid(g2)


# Part 2 #################################
