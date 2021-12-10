# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

def is_end_char(endc):
    return endc == ")" or endc == "]" or endc == "}" or endc == ">"

def is_start_char(endc):
    return endc == "(" or endc == "[" or endc == "{" or endc == "<"

def get_score_character(endc):
    if endc == ")":
        return 3
    elif endc == "]":
        return 57
    elif endc == "}":
        return 1197
    elif endc == ">":
        return 25137

class Chunk:
    def __init__(self, character, parent):
        self.character = character
        self.parent = parent
        self.content_chunks = []

    def is_valid_end_character(self, endc):
        if self.character == "(" and endc == ")":
            return True
        elif self.character == "[" and endc == "]":
            return True
        elif self.character == "{" and endc == "}":
            return True
        elif self.character == "<" and endc == ">":
            return True
        return False

    def process_char(self, c):
        #print "chunk "+self.character+ " processing: "+c
        if self.character == "":
            self.character = c
            return self
        elif is_end_char(c):
            #print "is end"
            #print self.is_valid_end_character(c)
            if self.is_valid_end_character(c):
                return self.parent
            else:
                #print "exception! "+c
                return False
        elif is_start_char(c):
            return self.create_child(c)

    def create_child(self, startc):
        child = Chunk(startc, self)
        return child

    def get_close_char(self):
        if self.character == "":
            return ""
        elif self.character == "(":
            return ")"
        elif self.character == "{":
            return "}"
        elif self.character == "<":
            return ">"
        elif self.character == "[":
            return "]"

    def close_chunk(self):
        return self.parent

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
valid_lines = []
chunks_lines = []
points = 0
for line in input_lines:
    chunk = Chunk("", Chunk("", Chunk("", Chunk("", False)))) # sometimes you can have a chunk completely end... creating a few nests
    error_found = False
    for c in line:
        #print c
        chunk = chunk.process_char(c)
        if chunk == False:
            #print str(get_score_character(c)) + " points"
            points = points + get_score_character(c)
            error_found = True
            break
    if error_found is False:
        valid_lines.append(line)
        chunks_lines.append(chunk)

print points

# Part 2 #################################
def score_close_string(s):
    score = 0
    for c in s:
        if c == ")":
            score = 5 * score + 1
        elif c == "]":
            score = 5 * score + 2
        elif c == "}":
            score = 5 * score + 3
        elif c == ">":
            score = 5 * score + 4
    return score

scores = []
for chunk in chunks_lines:
    close_string = ""
    while chunk != False:
        close_string = close_string + chunk.get_close_char()
        chunk = chunk.close_chunk()
    #print str(score_close_string(close_string)) + " " + close_string
    scores.append(score_close_string(close_string))

scores.sort()

print scores[int(len(scores)/2)]
