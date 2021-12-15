# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input_test.txt')

# Part 1 #################################
grid = helpers.get_grid_from_lines(input_lines)
grid = helpers.convert_grid_to_int(grid)

# queue entry:
# (x, y), total_risk, set((x,y), (x,y))
queue = []
history = set()
history.add((0, 0))
#queue.append([(0, 0), grid[0][0], history]) # the starting position is never entered, so its risk is not counted
queue.append([(0, 0), 0, history])

# end / goal location
end = max(grid[0].keys())

neighbors = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0]
    ]

memoize = {}

end_node = 0
while len(queue) > 0:
    #print("queue", queue)

    node = queue.pop(0)
    if node[0][0] == end and node[0][1] == end:
        end_node = node
        break
    #print("node", node)

    for neighbor in neighbors:
        x_new = node[0][0] + neighbor[0]
        y_new = node[0][1] + neighbor[1]
        #print("node[2]", node[2])
        #print("(x_new, y_new)", (x_new, y_new), node[2], (x_new, y_new) not in node[2])

        if x_new in grid and y_new in grid[x_new]:
            risk = node[1] + grid[x_new][y_new]
            memoize_key = str(x_new)+","+str(y_new)
            if (x_new, y_new) not in node[2] and (memoize_key not in memoize or risk < memoize[memoize_key]):
                history = node[2].copy()
                history.add((x_new, y_new))
                new_node = [(x_new, y_new), risk, history]
                memoize[memoize_key] = risk
                queue.append(new_node)
        queue.sort(key = lambda x: x[1])

#print end_node

display = {}
helpers.init_grid(display, end, end, ".")
for point in end_node[2]:
    display[point[0]][point[1]] = "#"
#helpers.print_grid(display)

print end_node[1]
# Part 2 #################################
