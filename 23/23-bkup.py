# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
class Amphipod:
    def __init__(self, letter, pos):
        self.letter = letter
        self.pos = pos
        if letter == "A":
            self.energyCost = 1
            self.destX = 3
        elif letter == "B":
            self.energyCost = 10
            self.destX = 5
        elif letter == "C":
            self.energyCost = 100
            self.destX = 7
        elif letter == "D":
            self.energyCost = 1000
            self.destX = 9

def printState(grid, amphipods):
    new_grid = helpers.copy_grid(grid)
    for a in amphipods:
        new_grid[a.pos[0]][a.pos[1]] = a.letter
    helpers.print_grid(new_grid)

def isInRoom(a):
    if a.pos[0] in (3, 5, 7, 9) and a.pos[1] >= 2:
            return True
    return False

def possibleMoves(grid, amphipods, currCost):
    moves = []
    for a in amphipods:
        move = []
        if isInRoom(a):
            if grid[a.pos[0]][a.pos[1]-1] == ".":
                #print (a.letter, "is in room and can move")
                # move into hall to pos x=1,2,4,6,8,10,11
                xOptions = {1,2,4,6,8,10,11}

                # remove xOptions that are blocked off by another amphipod
                for b in amphipods:
                    if b == a: continue
                    if isInRoom(b): continue
                    if b.pos[0] < a.pos[0]:
                        # a cannot go further left than b
                        newX = set()
                        for x in xOptions:
                            if x > b.pos[0]:
                                newX.add(x)
                        xOptions = newX
                        continue
                    if b.pos[0] > a.pos[0]:
                        # a cannot go further right than b
                        newX = set()
                        for x in xOptions:
                            if x < b.pos[0]:
                                newX.add(x)
                        xOptions = newX
                        continue

                for x in xOptions:
                    amphipodsTuples = []
                    amphipodsTuples.append([a.letter, (x, 1)])
                    for b in amphipods:
                        if b == a: continue
                        amphipodsTuples.append([b.letter, b.pos])
                    move = [
                        a,
                        (x, 1), # move into hallway
                        currCost + ((a.pos[1] - 1) + abs(a.pos[0] - x)) * a.energyCost, # cost
                        amphipodsTuples
                    ]
                    mk = moveKey(move, amphipods)
                    #print ("mk", mk, "memoize[mk]", memoize[mk] if mk in memoize else "new", "cost", move[2])
                    if mk == "['A3,3', 'A9,3', 'B3,2', 'B4,1', 'C5,2', 'C7,3', 'D5,3', 'D9,2']":
                        print ("done")
                        print move[2]
                        quit()
                    if mk not in memoize or move[2] < memoize[mk]:
                        memoize[mk] = move[2]
                        moves.append(move)
            else:
                #print (a.letter, "is in room and can't move")
                continue
        else:
            # the amphipod is in the hallway
            #print(a.letter, "is in hallway")
            path = range(min(a.pos[0], a.destX), max(a.pos[0], a.destX)+1)
            # the amphipod can only move to its room next, iff there is not another amphipod in its way
            collision = False
            for b in amphipods:
                if b == a: continue
                if b.pos[1] == 1 and b.pos[0] in path:
                    collision = True
                    break
                elif b.pos[1] >= 1 and b.pos[0] == a.destX and b.letter != a.letter:
                    collision = True
            if collision: continue
            yDest = 3 if grid[a.destX][3] == "." else 2

            amphipodsTuples = []
            amphipodsTuples.append([a.letter, (a.destX, yDest)])
            for b in amphipods:
                if b == a: continue
                amphipodsTuples.append([b.letter, b.pos])

            move = [
                a,
                (a.destX, yDest),
                currCost + (abs(a.pos[0] - a.destX) + (yDest - a.pos[1])) * a.energyCost,
                amphipodsTuples
            ]
            mk = moveKey(move, amphipods)
            if mk not in memoize or move[2] < memoize[mk]:
                memoize[mk] = move[2]
                moves.append(move)
    return moves

def moveKey(move, amphipods):
    locations = []
    locations.append(
        move[0].letter + str(move[1][0]) + "," + str(move[1][1])
    )
    for a in amphipods:
        if a == move[0]: continue
        locations.append(
            a.letter + str(a.pos[0]) + "," + str(a.pos[1])
        )
    locations.sort()
    return str(locations)

def printMoves(moves):
    print("Moves available")
    for m in moves:
        print(m[0].letter, m[1], m[2], str(m[3]))

def isDone(amphipods):
    for a in amphipods:
        if a.pos[0] != a.destX:
            return False
    return True

def getAmphipods(grid):
    amphipods = []
    for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] != "." and grid[x][y] != "#":
                amphipods.append(Amphipod(grid[x][y], (x, y)))
    return amphipods

def clearGrid(grid):
    for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] != "." and grid[x][y] != "#":
                grid[x][y] = "."

def createGrid(amphipods):
    newGrid = helpers.copy_grid(emptyGrid)
    for a in amphipods:
        newGrid[a.pos[0]][a.pos[1]] = a.letter
    return newGrid

def getAmphipodsFromTuples(amphipodsTuples):
    amphipods = []
    for a in amphipodsTuples:
        amphipods.append(Amphipod(a[0], a[1]))
    return amphipods

# actual code ############################
input_lines = helpers.read_lines_from_file('input_test.txt')

# Part 1 #################################
grid = helpers.get_grid_from_lines(input_lines)
emptyGrid = helpers.copy_grid(grid)
clearGrid(emptyGrid)

# spawn amphipods
amphipods = getAmphipods(grid)

memoize = {}

print("Initial grid --")
printState(grid, amphipods)

q = possibleMoves(grid, amphipods, 0)
q.sort(key=lambda x:x[2])
min_solution = None

print("Begin search --")

steps = 0
while len(q) > 0 and steps < 1000:
    steps += 1
    move = q.pop(0)
    #print("move", move)
    new_amphipods = getAmphipodsFromTuples(move[3])
    if isDone(new_amphipods):
        if min_solution == None:
            min_solution = move[2]
        elif move[2] < min_solution:
            min_solution = move[2]
        continue
    else:
        new_grid = createGrid(new_amphipods)
        new_moves = possibleMoves(new_grid, new_amphipods, move[2])
        for nm in new_moves:
            if min_solution == None or nm[2] < min_solution:
                q.append(nm)
    q.sort(key=lambda x:x[2])

print memoize
print steps
print min_solution

# Part 2 #################################
