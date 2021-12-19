# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers
import inspect

# functions ##############################
class Snailfish:
    def __init__ (self, string, parent=None, debug=False):
        self.string = string
        self.parent = parent
        self.left = None
        self.leftString = ""
        self.right = None
        self.rightString = ""
        self.debug = False
        self.parseString()

    def parseString(self):
        # remove first and last chars "[" and "]"
        self.string = self.string[1:-1]
        openLeftCount = 0
        for idx in range(len(self.string)):
            c = self.string[idx]
            #if self.debug: print ("c", c)
            if c == "," and openLeftCount == 0:
                self.leftString = self.string[:idx]
                self.rightString = self.string[idx+1:] # +1 to drop the "," itself
                break
            elif c == "[":
                #if self.debug: print("c", c, "openLeftCount", openLeftCount)
                openLeftCount += 1
            elif c == "]":
                #if self.debug: print("c", c, "openLeftCount", openLeftCount)
                openLeftCount -= 1
        if self.debug: print("self.leftString", self.leftString)
        if self.debug: print("self.rightString", self.rightString)
        if "," not in self.leftString:
            self.left = int(self.leftString)
        else:
            self.left = Snailfish(self.leftString, self)
        if "," not in self.rightString:
            self.right = int(self.rightString)
        else:
            self.right = Snailfish(self.rightString, self)

    def findLeftMostDepth(self, depthTarget, depthCurrent):
        if self.debug: print ("findLeftMostDepth of self", self.pprint())
        if depthCurrent >= depthTarget and isinstance(self.left, Snailfish) == False and isinstance(self.right, Snailfish) == False:
            return self

        foundLeft = None
        if isinstance(self.left, Snailfish):
            foundLeft = self.left.findLeftMostDepth(depthTarget, depthCurrent+1)
        if foundLeft != None:
            return foundLeft
        if foundLeft == None and isinstance(self.right, Snailfish):
            return self.right.findLeftMostDepth(depthTarget, depthCurrent+1)
        return None

    def findLeftMostSplittable(self):
        if self.debug: print ("findLeftMostSplittable")
        splitThreshold = 10

        if isinstance(self.left, Snailfish) == False:
            # left is a number!
            if self.left >= splitThreshold:
                splitVal = self.left
                if self.debug: print ("splitting: ", splitVal)
                splitString = "["+str(int(math.floor(float(splitVal)/2)))+","+str(int(math.ceil(float(splitVal)/2)))+"]"
                if self.debug: print ("new snailfish: ", splitString)
                self.left = Snailfish(splitString, self)
                return self.left
            # continue on to check the right sibling, since left wasn't above threshold
        else:
            # left is a snailfish
            splitter = self.left.findLeftMostSplittable()
            if splitter != None:
                return splitter

        # check the right sibling, since left didn't find anything
        if isinstance(self.right, Snailfish) == False:
            # right is a number!
            if self.right >= splitThreshold:
                splitVal = self.right
                if self.debug: print ("splitting: ", splitVal)
                splitString = "["+str(int(math.floor(float(splitVal)/2)))+","+str(int(math.ceil(float(splitVal)/2)))+"]"
                if self.debug: print ("new snailfish: ", splitString)
                self.right = Snailfish(splitString, self)
                return self.right
        else:
            # right is a snailfish
            splitter = self.right.findLeftMostSplittable()
            if splitter != None:
                return splitter

        return None

    def reduceSelf(self):
        if self.debug: print ("reducing", self.pprint())

        actionTaken = False
        exploadable = self.findLeftMostDepth(depthTarget=4, depthCurrent=0)
        if self.debug: print("findLeftMostDepth", exploadable.pprint() if exploadable != None else None)
        if exploadable != None:
            exploadable.explode()
            actionTaken = True

        if actionTaken == False:
            splittable = self.findLeftMostSplittable()
            if self.debug: print("splittable", splittable.pprint() if splittable != None else None)
            if splittable != None:
                actionTaken = True

        if self.debug: print ("after reduce", self.pprint())
        if actionTaken:
            self.reduceSelf()

    def findNumberToLeftExplode(self, adder):
        if self.debug: print ("isRightSibling?", self.isRightSibling())
        if self.parent == None:
            return None
        if self.isRightSibling() is False:
            # handle case where we're the left sibling
            # find the parent in which we are the first right sibling
            parent = self.findParentWhereWeAreRightSibling()
            if self.debug: print("findParentWhereWeAreRightSibling", parent.pprint() if parent != None else None)
            if parent != None:
                # find the rightmost number in the left sibling of that node. a number MUST exist.
                if isinstance(parent.left, Snailfish):
                    return parent.left.findRightMostNumberExplode(adder)
                else:
                    parent.left += adder
                    return parent.left
            return None
        else:
            # handle case where we're the right sibling
            # find the rightmost number in the left sibling. a number MUST exist.
            if isinstance(self.parent.left, Snailfish):
                return self.parent.left.findRightMostNumberExplode(adder)
            else:
                self.parent.left += adder
                return self.parent.left
            return None

    def findRightMostNumberExplode(self, adder):
        if isinstance(self.right, Snailfish):
            return self.right.findRightMostNumberExplode(adder)
        else:
            self.right += adder
            return self.right

    def findParentWhereWeAreRightSibling(self):
        if self.parent == None:
            return None
        if self.isRightSibling():
            return self.parent
        return self.parent.findParentWhereWeAreRightSibling()

    def isRightSibling(self):
        if self.parent == None:
            return False
        if self.parent.right == self:
            return True
        return False

    def findNumberToRightExplode(self, adder):
        if self.debug: print ("isRightSibling?", self.isRightSibling())
        if self.parent == None:
            return None
        if self.isRightSibling() is False:
            # handle case where we're the left sibling
            # find the left number in the right sibling. a number MUST exist.
            if isinstance(self.parent.right, Snailfish):
                return self.parent.right.findLeftMostNumberExplode(adder)
            else:
                self.parent.right += adder
                return self.parent.right
            return None

        else:
            # handle case where we're the right sibling

            # find the parent in which we are the first left sibling
            parent = self.findParentWhereWeAreLeftSibling()
            if self.debug: print("findParentWhereWeAreLeftSibling", parent.pprint() if parent != None else "None")

            # find the leftmost number in the right sibling of that node. a number MUST exist.
            if parent != None:
                if isinstance(parent.right, Snailfish):
                    return parent.right.findLeftMostNumberExplode(adder)
                else:
                    parent.right += adder
                    return parent.right
            return None

    def findLeftMostNumberExplode(self, adder):
        if isinstance(self.left, Snailfish):
            return self.left.findLeftMostNumberExplode(adder)
        else:
            self.left += adder
            return self.left

    def findParentWhereWeAreLeftSibling(self):
        if self.parent == None:
            return None
        if self.isRightSibling() == False:
            return self.parent
        return self.parent.findParentWhereWeAreLeftSibling()

    def explode(self):
        if self.debug: print("Exploding:", self.pprint())
        leftExplode = self.findNumberToLeftExplode(self.left)
        if self.debug: print ("findNumberToLeftExplode", leftExplode)
        rightExplode = self.findNumberToRightExplode(self.right)
        if self.debug: print ("findNumberToRightExplode", rightExplode)
        self.zeroSelf()
        if self.debug: print("post explosion:", self.pprint())
        if self.debug: print("parent", self.parent.pprint())

    def zeroSelf(self):
        if self.debug: print("parent", self.parent.pprint())
        if self.parent.left == self:
            self.parent.left = 0
        elif self.parent.right == self:
            self.parent.right = 0

    def pprint(self):
        l = ""
        if isinstance(self.left, Snailfish):
            l = self.left.pprint()
        else:
            l = str(self.left)

        r = ""
        if isinstance(self.right, Snailfish):
            r = self.right.pprint()
        else:
            r = str(self.right)

        return "["+l+","+r+"]"

    def magnitude(self):
        leftVal = 0
        rightVal = 0
        if isinstance(self.left, Snailfish):
            leftVal = self.left.magnitude()
        else:
            leftVal = self.left

        if isinstance(self.right, Snailfish):
            rightVal = self.right.magnitude()
        else:
            rightVal = self.right
        return (3*leftVal) + (2*rightVal)


# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################

snailfishString = ""
for line in input_lines:
    if snailfishString == "":
        snailfishString = line
    else:
        snailfishString = "["+snailfishString+","+line+"]"
    #print("snailfishString:", snailfishString)
    sf = Snailfish(snailfishString, None)
    sf.reduceSelf()
    snailfishString = sf.pprint()
    #print("post reduction:", snailfishString)

# calculate magnitude
sf = Snailfish(snailfishString, None)
print (sf.pprint())
print (sf.magnitude())

# Part 2 #################################
max_mag = 0
for line1 in input_lines:
    for line2 in input_lines:
        snailfishString = "["+line1+","+line2+"]"
        sf = Snailfish(snailfishString, None)
        sf.reduceSelf()
        mag = sf.magnitude()
        if mag > max_mag:
            max_mag = mag

print max_mag
