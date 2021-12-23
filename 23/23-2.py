# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
targetX = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9
}

energyCost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}
def isDone(amphipods):
    for a in amphipods:
        if a[1][0] != targetX[a[0]]:
            return False
    return True


def getMoves(amphipods, currCost, debug=False):
    if debug: print("getMoves", amphipods, currCost)
    moves = []
    for a in amphipods:

        # case where a is in a room
        if a[1][0] in targetX.values():

            # skip this amphipod if it's blocked in
            isSpotAboveFree = True
            for b in amphipods:
                if b[1][0] == a[1][0] and b[1][1] == (a[1][1]-1):
                    if debug: print(a[0], "blocked in by", b[0])
                    isSpotAboveFree = False
                    break
            if isSpotAboveFree == False: continue

            # skip this amphipod if it's in it's own room
            if a[1][0] == targetX[a[0]] and a[1][1] == 5:
                if debug: print(a, "is in the correct spot. Skip")
                continue

            # skip this amphipod if it's in it's own room and the correct amphipod is below it
            if a[1][0] == targetX[a[0]] and a[1][1] < 5:
                checkList = set()
                for i in range((a[1][1]+1),5+1):
                    checkList.add(i)
                for b in amphipods:
                    if b[0] == a[0] and b[1][0] == targetX[a[0]] and b[1][1] in checkList:
                        checkList.remove(b[1][1])
                if len(checkList) == 0:
                    if debug: print(a, "is in the correct spot, with correct below. Skip")
                    continue

            # All the hallway spots that a can move
            xOptions = {1,2,4,6,8,10,11}

            # remove xOptions that are blocked off by another amphipod
            for b in amphipods:
                newX = set()
                if b == a: continue
                if b[1][0] in targetX.values(): continue # b in a room; not obstructing
                if b[1][0] < a[1][0]:  # a cannot go further left than b
                    for x in xOptions:
                        if x > b[1][0]: newX.add(x)
                elif b[1][0] > a[1][0]: # a cannot go further right than b
                    for x in xOptions:
                        if x < b[1][0]: newX.add(x)
                xOptions = newX

            # skip silly moves -- always move to end
            if 11 in xOptions:
                xOptions.remove(10)
            if 1 in xOptions:
                xOptions.remove(2)

            if debug: print(a, "is free to move into the hallway", xOptions)

            for x in xOptions:
                nextAmphipods = eval(str(amphipods)) # copies amphipods list
                for idx in range(len(nextAmphipods)):
                    b = nextAmphipods[idx]
                    if b[0] == a[0] and b[1] == a[1]:
                        nextAmphipods[idx] = (b[0], (x, 1)) # move into hallway
                nextAmphipods.sort()
                nextCost = currCost + (a[1][1] - 1 + abs(a[1][0] - x)) * energyCost[a[0]]
                if debug: print("nextAmphipods", nextAmphipods, nextCost)
                if str(nextAmphipods) not in memoize or nextCost < memoize[str(nextAmphipods)]:
                    memoize[str(nextAmphipods)] = nextCost
                    moves.append([nextAmphipods, nextCost])

        # case where amphipod is in the hallway
        # an amphipod will only move if it can go to the correct room if it's not filled with a squatter
        else:
            path = range(min(a[1][0], targetX[a[0]]), max(a[1][0], targetX[a[0]])+1)

            # the amphipod can only move to its room next, iff there is not another amphipod in its way
            collision = False
            for b in amphipods:
                if b == a: continue
                if b[1][1] == 1 and b[1][0] in path: # someone is in my path to travel to the room
                    collision = True
                    break
                elif b[1][1] >= 1 and b[1][0] == targetX[a[0]] and b[0] != a[0]: # a squatter is in my room
                    collision = True
                    break
            if collision: continue

            # no collision, calculate how deep into the room we should go
            yDest = 5
            for b in amphipods:
                if b[0] == a[0] and b[1][0] == targetX[a[0]] and b[1][1] > 1:
                    yDest = min(b[1][1]-1, yDest)
                    break

            if debug: print(a, "is free to move into a room", targetX[a[0]], "with depth", yDest)

            # create the move
            nextAmphipods = eval(str(amphipods)) # copies amphipods list
            for idx in range(len(nextAmphipods)):
                b = nextAmphipods[idx]
                if b[0] == a[0] and b[1] == a[1]:
                    nextAmphipods[idx] = (b[0], (targetX[b[0]], yDest)) # move into room
            nextAmphipods.sort()
            nextCost = currCost + (abs(a[1][0] - targetX[a[0]]) + (yDest - a[1][1])) * energyCost[a[0]]
            if debug: print("nextAmphipods", nextAmphipods, nextCost)
            if str(nextAmphipods) not in memoize or nextCost < memoize[str(nextAmphipods)]:
                memoize[str(nextAmphipods)] = nextCost
                moves.append([nextAmphipods, nextCost])
    return moves


# actual code ############################
input_lines = helpers.read_lines_from_file('input2.txt')

# Part 1 #################################
grid = helpers.get_grid_from_lines(input_lines)

# extract amphipods
amphipods = []
for x in range(max(grid.keys())+1):
        for y in range(max(grid[0].keys())+1):
            if grid[x][y] != "." and grid[x][y] != "#":
                amphipods.append((grid[x][y], (x, y)))
amphipods.sort()
print("amphipods starting:", amphipods)

# init memoization
# key of all the amphipods : minimum cost to get there
memoize = {}
memoize[str(amphipods)] = 0

# debugging
#amphipods = [('A', (3, 3)), ('A', (10, 1)), ('B', (5, 2)), ('B', (5, 3)), ('C', (7, 2)), ('C', (7, 3)), ('D', (6, 1)), ('D', (8, 1))]
#amphipods.sort()

# get initial set of moves to search
q = getMoves(amphipods, 0)
print("q", q)

# debugging
#quit()

# begin the search
min_solution = None
steps = 0
#while len(q) > 0 and steps < 1000:
while len(q) > 0:
    steps += 1
    move = q.pop(0)

    if isDone(move[0]):
        if min_solution == None:
            min_solution = move[1]
        elif move[1] < min_solution:
            min_solution = move[1]
        continue
    else:
        new_moves = getMoves(move[0], move[1])
        for nm in new_moves:
            if min_solution == None or nm[1] < min_solution:
                q.append(nm)
    q.sort(key=lambda x:x[1])

print min_solution

# Part 2 #################################

'''
#############
#...........#
###B#C#B#D###
###D#C#B#A###
###D#B#A#C###
###A#D#C#A###
#############

#############
#..........D#
###B#C#B#.###
###D#C#B#A###
###D#B#A#C###
###A#D#C#A###
#############

#############
#A.........D#
###B#C#B#.###
###D#C#B#.###
###D#B#A#C###
###A#D#C#A###
#############

#############
#A........BD#
###B#C#.#.###
###D#C#B#.###
###D#B#A#C###
###A#D#C#A###
#############

#############
#A......B.BD#
###B#C#.#.###
###D#C#.#.###
###D#B#A#C###
###A#D#C#A###
#############

#############
#AA.....B.BD#
###B#C#.#.###
###D#C#.#.###
###D#B#.#C###
###A#D#C#A###
#############

#############
#AA.....B.BD#
###B#.#.#.###
###D#C#.#.###
###D#B#C#C###
###A#D#C#A###
#############

#############
#AA.....B.BD#
###B#.#.#.###
###D#.#C#.###
###D#B#C#C###
###A#D#C#A###
#############

#############
#AA...B.B.BD#
###B#.#.#.###
###D#.#C#.###
###D#.#C#C###
###A#D#C#A###
#############

#############
#AA.D.B.B.BD#
###B#.#.#.###
###D#.#C#.###
###D#.#C#C###
###A#.#C#A###
#############

#############
#AA.D...B.BD#
###B#.#.#.###
###D#.#C#.###
###D#.#C#C###
###A#B#C#A###
#############

#############
#AA.D.....BD#
###B#.#.#.###
###D#.#C#.###
###D#B#C#C###
###A#B#C#A###
#############

#############
#AA.D......D#
###B#.#.#.###
###D#B#C#.###
###D#B#C#C###
###A#B#C#A###
#############

#############
#AA.D......D#
###B#.#C#.###
###D#B#C#.###
###D#B#C#.###
###A#B#C#A###
#############

#############
#AA.D.....AD#
###B#.#C#.###
###D#B#C#.###
###D#B#C#.###
###A#B#C#.###
#############

#############
#AA.......AD#
###B#.#C#.###
###D#B#C#.###
###D#B#C#.###
###A#B#C#D###
#############

#############
#AA.......AD#
###.#B#C#.###
###D#B#C#.###
###D#B#C#.###
###A#B#C#D###
#############

#############
#AA.......AD#
###.#B#C#.###
###.#B#C#.###
###D#B#C#D###
###A#B#C#D###
#############

#############
#AA.D.....AD#
###.#B#C#.###
###.#B#C#.###
###.#B#C#D###
###A#B#C#D###
#############

#############
#A..D.....AD#
###.#B#C#.###
###.#B#C#.###
###A#B#C#D###
###A#B#C#D###
#############

#############
#...D.....AD#
###.#B#C#.###
###A#B#C#.###
###A#B#C#D###
###A#B#C#D###
#############

#############
#.........AD#
###.#B#C#.###
###A#B#C#D###
###A#B#C#D###
###A#B#C#D###
#############

#############
#..........D#
###A#B#C#.###
###A#B#C#D###
###A#B#C#D###
###A#B#C#D###
#############

#############
#...........#
###A#B#C#D###
###A#B#C#D###
###A#B#C#D###
###A#B#C#D###
#############
'''
