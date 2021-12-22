# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
def getPixel(inputImage, x, y):
    if x not in inputImage:
        return "."
    if y not in inputImage[x]:
        return "."
    return inputImage[x][y]

def getOutputKey(inputImage, x, y):
    outputKey = ""
    neighborOffsets = [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, 0],
        [0, 0],
        [1, 0],
        [-1, 1],
        [0, 1],
        [1, 1]
    ]
    for offset in neighborOffsets:
        newX = x + offset[0]
        newY = y + offset[1]
        outputKey += getPixel(inputImage, newX, newY)
    return outputKey


def expandGrid(grid):
    new_grid = {}
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y-4, max_y+6):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x-4, max_x+6):
            if x not in new_grid:
                new_grid[x] = {}
            new_grid[x][y] = "."
    return new_grid

def copyAndExpandGrid(grid, default):
    new_grid = {}
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y-4, max_y+6):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x-4, max_x+6):
            if x not in new_grid:
                new_grid[x] = {}
            if x in grid and y in grid[x]:
                new_grid[x][y] = grid[x][y]
            else:
                new_grid[x][y] = default
    return new_grid

def convertOutputKeyToBinary(outputKey):
    binaryString = ""
    for c in outputKey:
        if c == ".":
            binaryString += "0"
        else:
            binaryString += "1"
    return binaryString

def convertOutputKeyToDec(outputBinary):
    return int(outputBinary, 2)

def outputImage(inputImage):
    # create a grid that's one larger than the current one
    outputImage = {}

    min_x = min(inputImage.keys())
    max_x = max(inputImage.keys())
    min_y = min(inputImage[0].keys())
    max_y = max(inputImage[0].keys())

    # calculate out the output
    for x in range(min_x+2, max_x-1):
        for y in range(min_y+2, max_y-1):
            outputKey = getOutputKey(inputImage, x, y)
            outputBin = convertOutputKeyToBinary(outputKey)
            outputDec = convertOutputKeyToDec(outputBin)
            outputPxl = imageEnhancementAlgorithm[outputDec]
            helpers.add_to_grid(x, y, outputPxl, outputImage)
    return outputImage

def countGrid(grid, character):
    count = 0
    min_y = min(grid[0].keys())
    max_y = max(grid[0].keys())
    for y in range(min_y, max_y+1):
        min_x = min(grid.keys())
        max_x = max(grid.keys())
        for x in range(min_x, max_x+1):
            if grid[x][y] == character:
                count += 1
    return count

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')
imageEnhancementAlgorithm = ""
inputImageLines = []
for idx in range(len(input_lines)):
    line = input_lines[idx]
    if line == "":
        inputImageLines = input_lines[idx+1:]
        break
    imageEnhancementAlgorithm += line
#print("imageEnhancementAlgorithm", imageEnhancementAlgorithm)

inputImage = helpers.get_grid_from_lines(inputImageLines)

#print("getOutputKey", getOutputKey(inputImage, 2, 2))
#print("convertOutputKeyToDec", convertOutputKeyToDec(convertOutputKeyToBinary(getOutputKey(inputImage, 2, 2))))

out2 = {}

for i in range(25):
    inputImage = copyAndExpandGrid(inputImage, ".")
    out1 = outputImage(inputImage)
    out1 = copyAndExpandGrid(out1, "#")
    out2 = outputImage(out1)
    inputImage = out2

helpers.print_grid(out2)

print countGrid(out2, "#")

#5053 is too high


# Part 1 #################################

# Part 2 #################################
