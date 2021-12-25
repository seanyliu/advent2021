# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
class ALU:
    def __init__(self, instructions):
        self.vars = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.instructions = instructions
        self.input = ""

    def getValue(self, varOrInt):
        if varOrInt in self.vars.keys():
            return self.vars[varOrInt]
        else:
            return int(varOrInt)

    def run(self):
        for i in self.instructions:
            instruction = i.split(" ")[0]
            if instruction == "inp":
                # inp a - Read an input value and write it to variable a.
                self.vars[i.split(" ")[1]] = int(self.input[0])
                #print("post input:", self.vars)
                self.input = self.input[1:]
            elif instruction == "add":
                # add a b - Add the value of a to the value of b, then store the result in variable a.
                self.vars[i.split(" ")[1]] = self.getValue(i.split(" ")[1]) + self.getValue(i.split(" ")[2])
            elif instruction == "mul":
                # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
                self.vars[i.split(" ")[1]] = self.getValue(i.split(" ")[1]) * self.getValue(i.split(" ")[2])
            elif instruction == "div":
                # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
                self.vars[i.split(" ")[1]] = self.getValue(i.split(" ")[1]) / self.getValue(i.split(" ")[2])
            elif instruction == "mod":
                # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
                self.vars[i.split(" ")[1]] = self.getValue(i.split(" ")[1]) % self.getValue(i.split(" ")[2])
            elif instruction == "eql":
                # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
                self.vars[i.split(" ")[1]] = 1 if self.getValue(i.split(" ")[1]) == self.getValue(i.split(" ")[2]) else 0

def shouldPrune(node):
    # the next node has > 14 characters
    if len(node[2]) == 14:
        return True

    elif len(node[2]) == 13:
        # we're on the last block
        # If: (( ( (zPrev) % 26 ) + -6 ) ) == ( c )
        #   z = ( zPrev / 26 )
        # else:
        #   z = ( ( ( zPrev / 26 ) * 26 ) + (c + 7) )
        # therefore only advance if we know that the condition is true
        return (eval(node[0])["z"] % 26 - 6) != int(node[1])

    # there are 6 forced multiplys. So we must force the checks for 6 divisions.

    elif len(node[2]) == 12:
        # we're on the second to last block. We MUST force a divide
        #If: ((zPrev % 26) - 13) == c
        #   z = ( zPrev / 26 ) <-- only way for z to get smaller
        #Else:
        #   z = (((zPrev / 26) * 26) + (c + 2))
        return (eval(node[0])["z"] % 26 - 13) != int(node[1])

    elif len(node[2]) == 11:
        return (eval(node[0])["z"] % 26 - 12) != int(node[1])

    elif len(node[2]) == 10:
        return (eval(node[0])["z"] % 26 - 0) != int(node[1])

    elif len(node[2]) == 7:
        return (eval(node[0])["z"] % 26 - 11) != int(node[1])

    elif len(node[2]) == 6:
        return (eval(node[0])["z"] % 26 - 2) != int(node[1])

    elif len(node[2]) == 4:
        return (eval(node[0])["z"] % 26 - 12) != int(node[1])

    return False

# actual code ############################
input_lines = helpers.read_lines_from_file('input_original.txt')

# initialize alus that represent sub-systems
alus = []
for i in range(14):
    alus.append(ALU([]))

# build up the alu lines
i = -1
for line in input_lines:
    if line.split(" ")[0] == "inp": i += 1
    alus[i].instructions.append(line)

# initialize the queue.
# "{w,x,y,z}", "input as string"
q = []
for j in range(1, 9+1):
    i = 9 - (j - 1)
    q.append(
        [
            str({
                "w": 0,
                "x": 0,
                "y": 0,
                "z": 0,
            }),
            str(i),
            ""
        ]
    )

# perform depth-first-search until we get an answer
while len(q) > 0:
    node = q.pop()

    # get the node inputs
    aluInp = node[1]
    prevDigits = node[2]
    aluIdx = len(prevDigits)
    aluVars = eval(node[0])

    # run the alu
    alus[aluIdx].vars = aluVars
    alus[aluIdx].input = aluInp
    alus[aluIdx].run()
    print ("prevDigits", prevDigits, "node:", aluInp, aluIdx, aluVars, "gives:", alus[aluIdx].vars)

    # check the output if we're done
    if alus[aluIdx].vars["z"] == 0:
        print("Done:", prevDigits+aluInp)
        break

    # create the next nodes to append to queue
    for j in range(1, 9+1):
        i = 9 - (j - 1)
        new = [
            str(alus[aluIdx].vars),
            str(i),
            prevDigits+aluInp
        ]
        if shouldPrune(new) == False:
            q.append(new)
