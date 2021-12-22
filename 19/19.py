# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

def splitScannerLines(input_lines):
    scanners = []
    scanner = []
    for line in input_lines:
        if "---" in line:
            scanners.append(scanner)
            scanner = []
        elif line == "":
            continue
        else:
            scanner.append(line)
    scanners.append(scanner)
    scanners.pop(0)
    return scanners

def initScanners(scannerLines):
    scanners = []
    for s in scannerLines:
        scanners.append(Scanner(s))
    return scanners

class Scanner:
    def __init__(self, beaconLines):
        self.beacons = set()
        for b in beaconLines:
            coords = b.split(",")
            coords = tuple(convertArrToInt(coords))
            self.beacons.add(coords)
        self.scannerCoords = set()
        self.scannerCoords.add((0, 0, 0))

    def pprint(self):
        return self.beacons

def convertArrToInt(arr):
    new = []
    for i in arr: new.append(int(i))
    return new

def findOverlap(scannerA, scannerB):
    offset = None
    #print("overlaps:", scannerA.beacons, scannerB.beacons, countOverlaps(scannerA.beacons, scannerB.beacons))

    # generate all possible rotations:
    rotations = [
        [1, 2, 3],
        [2, -1, 3],
        [-1, -2, 3],
        [1, -2, 3],
        [1, 3, -2],
        [2, 3, 1],
        [-1, 3, 2],
        [-2, 3, -1],
        [2, 1, -3],
        [1, -2, -3],
        [-2, 1, -3],
        [-1, 2, -3],
        [2, -3, -1],
        [1, -3, 2],
        [-2, -3, 1],
        [-1, -3, -2],
        [3, -2, 1],
        [3, 1, 2],
        [3, 2, -1],
        [3, -1, -2],
        [-3, -2, -1],
        [-3, -1, 2],
        [-3, 2, 1],
        [-3, 1, -2]
    ]

    for rotation in rotations:
        # generate a rotation of all of scanner B

        rotatedBeaconsB = set()
        for beaconB in scannerB.beacons:
            point = beaconB
            newPointList = []
            for axis in rotation:
                multiplier = int(float(axis)/abs(axis))
                value = point[abs(axis)-1]
                newPointList.append(multiplier*value)
            newPoint = tuple(newPointList)
            rotatedBeaconsB.add(newPoint)

        rotatedScanners = set()
        for s in scannerB.scannerCoords:
            point = s
            newPointList = []
            for axis in rotation:
                multiplier = int(float(axis)/abs(axis))
                value = point[abs(axis)-1]
                newPointList.append(multiplier*value)
            newPoint = tuple(newPointList)
            rotatedScanners.add(newPoint)

        # generate all possible offsets per axis ===

        # generate all the minMax offsets per axis
        minMaxPerAxisA = minMaxPerAxis(scannerA.beacons)
        minMaxPerAxisB = minMaxPerAxis(rotatedBeaconsB)
        offsetRanges = [] # [(xmin, xmax), (ymin, ymax), (zmin, zmax)]
        for axisIdx in range(len(minMaxPerAxisA)):
            mmA = minMaxPerAxisA[axisIdx]
            mmB = minMaxPerAxisB[axisIdx]
            #print("mmA", mmA, "mmB", mmB)
            offsetMin = mmA[0] - abs(mmB[1] - mmB[0])
            offsetMax = mmA[1] + abs(mmB[1] - mmB[0])
            offsetRanges.append((offsetMin, offsetMax))
        #print("offsetRanges", offsetRanges)

        # generate all the offset possibilities
        offsets = []
        for bA in scannerA.beacons:
            for bB in rotatedBeaconsB:
                tupleList = []
                for axisIdx in range(len(bA)):
                    tupleList.append(bA[axisIdx] - bB[axisIdx])
                offsets.append(tuple(tupleList))
        #print("offsets:", offsets)

        # apply the offsets to scannerB, and count overlaps
        for offset in offsets:
            beaconsOffsetB = transformOffset(rotatedBeaconsB, offset)
            scannerOffsets = transformOffset(rotatedScanners, offset)
            if countOverlaps(scannerA.beacons, beaconsOffsetB) >= overlapThreshold:
                print("Found overlap!", offset)
                scannerB.beacons = beaconsOffsetB
                scannerB.scannerCoords = scannerOffsets
                return True

    return None

def minMaxPerAxis(beacons):
    minMaxPerAxis = []
    for axisIdx in range(len(next(iter(beacons)))):
        minimum = min(beacons, key = lambda x: x[axisIdx])[axisIdx]
        if minimum > 0: minimum = 0
        maximum = max(beacons, key = lambda x: x[axisIdx])[axisIdx]
        if maximum < 0: maximum = 0
        minMaxPerAxis.append([minimum, maximum])
    return minMaxPerAxis

def countOverlaps(beaconsA, beaconsB):
    count = 0
    for b in beaconsA:
        if b in beaconsB:
            count += 1
    return count

def transform(beacons, axes, flip, offset):
    newList = []
    return newlist

def transformAxes(beacons, axes):
    # axes: [0, 1, 2] representing indeces of x,y,z
    new = set()
    for b in beacons:
        tempList = []
        for a in axes:
            print ("axes", axes)
            tempList.append(b[a])
        new.add(tuple(tempList))
    return new

def transformOffset(beacons, offset):
    new = set()
    for b in beacons:
        tempList = []
        for idx in range(len(offset)):
            tempList.append(b[idx] + offset[idx])
        new.add(tuple(tempList))
    return new

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')
overlapThreshold = 12

# Part 1 #################################
scanners = initScanners(splitScannerLines(input_lines))

'''
for s in scanners:
    print("scanner", s.pprint())

for s in scanners[1:]:
    print ("attempt to overlap", s.pprint())
    findOverlap(scanners[0], s)
'''

scannerCount = len(scanners)
while scannerCount > 1:
    overlapFound = False
    for i in range(len(scanners)):
        for j in range(len(scanners)):
            if i == j:
                continue
            overlap = findOverlap(scanners[i], scanners[j])
            if overlap != None:
                overlapFound = True
                newscanners = []
                for k in range(len(scanners)):
                    if k != i and k != j:
                        newscanners.append(scanners[k])
                for o in scanners[j].beacons:
                    scanners[i].beacons.add(o)
                for o in scanners[j].scannerCoords:
                    scanners[i].scannerCoords.add(o)
                newscanners.append(scanners[i])
                break
        if overlapFound:
            break
    scanners = newscanners
    scannerCount = len(scanners)

    if overlapFound == False:
        print("INFINITE LOOP")
        break

def manhattan(a, b):
    sum = 0
    for i in range(len(a)):
        sum += abs(a[i] - b[i])
    return sum

print len(scanners[0].beacons)
print(scanners[0].scannerCoords)

coords = scanners[0].scannerCoords
maxDist = 0
for i in coords:
    for j in coords:
        if i == j: continue
        dist = manhattan(i, j)
        if dist > maxDist:
            maxDist = dist
print maxDist

# Part 2 #################################
