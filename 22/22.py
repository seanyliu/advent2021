# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
on = set()
for line in input_lines:
    onOrOff = line.split(" ")[0]
    xRange = line.split(" ")[1].split(",")[0].split("=")[1]
    yRange = line.split(" ")[1].split(",")[1].split("=")[1]
    zRange = line.split(" ")[1].split(",")[2].split("=")[1]
    print ("xRange", xRange, "yRange", yRange, "zRange", zRange)

    xMin = max(-50, int(xRange.split("..")[0]))
    xMax = min(50, int(xRange.split("..")[1]))
    yMin = max(-50, int(yRange.split("..")[0]))
    yMax = min(50, int(yRange.split("..")[1]))
    zMin = max(-50, int(zRange.split("..")[0]))
    zMax = min(50, int(zRange.split("..")[1]))

    for x in range(xMin, xMax+1):
        for y in range(yMin, yMax+1):
            for z in range(zMin, zMax+1):
                if onOrOff == "on":
                    on.add((x, y, z))
                else:
                    if (x, y, z) in on:
                        on.remove((x, y, z))

print len(on)

# Part 2 #################################
