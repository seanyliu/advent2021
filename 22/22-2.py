# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
class Cuboid:
    def __init__(self, xRange, yRange, zRange, state):
        self.xRange = xRange # range(min, max)
        self.yRange = yRange # range(min, max)
        self.zRange = zRange # range(min, max)
        self.state = state # "on" or "off"

    def pprint(self):
        return str(self.xRange) + "," + str(self.yRange) + "," + str(self.zRange)

def isRangeOverlapping(x, y):
    if len(x) == 0 or len(y) == 0:
        return False
    overlappingRange = range(max(x[0], y[0]), min(x[-1], y[-1])+1)
    if len(overlappingRange) > 0:
        return True
    return False

def getRangeOverlap(x, y):
    return range(max(x[0], y[0]), min(x[-1], y[-1])+1)

def isCuboidOverlapping(a, b):
    return isRangeOverlapping(a.xRange, b.xRange) and isRangeOverlapping(a.yRange, b.yRange) and isRangeOverlapping(a.zRange, b.zRange)

def getCuboidOverlap(a, b):
    return Cuboid(
        getRangeOverlap(a.xRange, b.xRange),
        getRangeOverlap(a.yRange, b.yRange),
        getRangeOverlap(a.zRange, b.zRange),
        "on"
    )

#def intersectCuboids(a, b):

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# generate steps
steps = []
for line in input_lines:
    onOrOff = line.split(" ")[0]
    xRange = line.split(" ")[1].split(",")[0].split("=")[1]
    yRange = line.split(" ")[1].split(",")[1].split("=")[1]
    zRange = line.split(" ")[1].split(",")[2].split("=")[1]

    xMin = int(xRange.split("..")[0])
    xMax = int(xRange.split("..")[1])
    yMin = int(yRange.split("..")[0])
    yMax = int(yRange.split("..")[1])
    zMin = int(zRange.split("..")[0])
    zMax = int(zRange.split("..")[1])
    '''
    xMin = max(-50, int(xRange.split("..")[0]))
    xMax = min(50, int(xRange.split("..")[1]))
    yMin = max(-50, int(yRange.split("..")[0]))
    yMax = min(50, int(yRange.split("..")[1]))
    zMin = max(-50, int(zRange.split("..")[0]))
    zMax = min(50, int(zRange.split("..")[1]))
    '''

    steps.append(Cuboid(range(xMin, xMax+1), range(yMin, yMax+1), range(zMin, zMax+1), onOrOff))

# we are going to store a list of cuboids
# importantly, these are all *non* overlapping cuboids
on = []

# off x=0..2,y=0..2,z=0..2
while len(steps) > 0:
    step = steps.pop(0)
    #print("step.state", step.state)
    newOn = []
    foundOverlap = False

    for o in on:
        #print("on", o.pprint())
        if isCuboidOverlapping(o, step):
            foundOverlap = True
            overlap = getCuboidOverlap(o, step)
            #print("overlap", overlap.pprint())

            # handle splitting the existing cuboid into 27
            xSegments = []
            xSegments.append(range(o.xRange[0], overlap.xRange[0]))
            xSegments.append(overlap.xRange)
            xSegments.append(range(overlap.xRange[-1]+1, o.xRange[-1]+1))
            #print("xSegments", xSegments)

            ySegments = []
            ySegments.append(range(o.yRange[0], overlap.yRange[0]))
            ySegments.append(overlap.yRange)
            ySegments.append(range(overlap.yRange[-1]+1, o.yRange[-1]+1))
            #print("ySegments", ySegments)

            zSegments = []
            zSegments.append(range(o.zRange[0], overlap.zRange[0]))
            zSegments.append(overlap.zRange)
            zSegments.append(range(overlap.zRange[-1]+1, o.zRange[-1]+1))
            #print("zSegments", zSegments)

            for xRange in xSegments:
                for yRange in ySegments:
                    for zRange in zSegments:
                        if xRange == overlap.xRange and yRange == overlap.yRange and zRange == overlap.zRange:
                            # this is the overlapping cube portion; ignore it since we'll handle it all at once later
                            continue
                        if len(xRange) > 0 and len(yRange) > 0 and len(zRange) > 0:
                            newOn.append(Cuboid(xRange, yRange, zRange, o.state))
        else:
            # no intersection with an existing cube, so re-append the existing cube
            newOn.append(o)

    # append the cube if it's "on"
    if step.state == "on":
        newOn.append(step)

    on = newOn

print("Counting on cuboids", "---")

# count on cuboids
count = 0
for c in on:
    #print(c.pprint())
    count += len(c.xRange) * len(c.yRange) * len(c.zRange)
print count
