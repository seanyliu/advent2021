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

    def getValueEval(self, varOrInt):
        if varOrInt in self.vars.keys():
            return self.vars[varOrInt]
        else:
            return str(varOrInt)

    def equations(self):
        for i in self.instructions:
            instruction = i.split(" ")[0]
            if instruction == "inp":
                # inp a - Read an input value and write it to variable a.
                self.vars[i.split(" ")[1]] = self.input[0]
                self.input = self.input[1:]
            elif instruction == "add":
                # add a b - Add the value of a to the value of b, then store the result in variable a.
                self.vars[i.split(" ")[1]] = "( " + self.getValueEval(i.split(" ")[1]) + " + " + self.getValueEval(i.split(" ")[2]) + " )"
            elif instruction == "mul":
                # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
                self.vars[i.split(" ")[1]] = "( " + self.getValueEval(i.split(" ")[1]) + " * " + self.getValueEval(i.split(" ")[2]) + " )"
            elif instruction == "div":
                # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
                self.vars[i.split(" ")[1]] = "( " + self.getValueEval(i.split(" ")[1]) + " / " + self.getValueEval(i.split(" ")[2]) + " )"
            elif instruction == "mod":
                # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
                self.vars[i.split(" ")[1]] = "( " + self.getValueEval(i.split(" ")[1]) + " % " + self.getValueEval(i.split(" ")[2]) + " )"
            elif instruction == "eql":
                # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
                self.vars[i.split(" ")[1]] = "( 1 if (" + self.getValueEval(i.split(" ")[1]) + " ) == ( "+ self.getValueEval(i.split(" ")[2]) + " ) else 0 )"

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

# actual code ############################
input_lines = helpers.read_lines_from_file('input_test.txt')
print(input_lines)

alu = ALU(input_lines)

alu.input = "i" # update
alu.vars = { # update
    "y": "yPrev",
    "x": "xPrev",
    "z": "zPrev",
    "w": "wPrev"
}
alu.equations()
for key in alu.vars.keys():
    print(key, alu.vars[key])



for i in range(1,10):
    alu.vars = {
        "y": 10,
        "x": 1,
        "z": 218,
        "w": 2
    }
    inputString = str(i)
    alu.input = inputString
    alu.run()
    print("input", inputString, alu.vars)

quit()

'''
print("digit 2:")
seen = set()
repeatCount = 0
for i in range(1,10):
    for j in range(1, 10):
        for k in range(1, 10):
            inputString = str(i) + str(j) + str(k)
            alu.input = inputString
            alu.run()
            print("input", inputString, alu.vars)
            if alu.vars["z"] in seen:
                print("Repeat!")
            else:
                seen.add(alu.vars["z"])
print ("unique", len(seen))
quit()
'''

alu.input = "99939399999999"
alu.run()
print alu.vars

max_input = ""
for i in range(14):
    max_input += "9"
inputStr = max_input


while True:
    alu.input = inputStr
    alu.run()
    print("inputStr", inputStr, alu.vars)
    if alu.vars["z"] == 0:
        print("valid", inputStr)
        break
    else:
        #print("invalid", inputStr)

        inputInt = int(inputStr)
        while True:
            inputInt -= 1
            if "0" not in str(inputInt):
                inputStr = str(inputInt)
                break

# Part 1 #################################
'''
w = 0
x = 0
y = 0
z = 0

w = input[0]
  x = x * 0
  z = x + z
  x = x % 26
  z = z / 1
x = 14     #x = x + 14
x = 0      #x = 1 if x == input[0] else 0
x = 1      #x = 1 if x == 0 else 0
y = 0      #y = y * 0
y = 25     #y = y + 25
y = 25     #y = y * x
y = 26     #y = y + 1
z = 0      #z = z * y
y = 0      #y = y * 0
y = input[0]  #y = y + w
  y = y + 0
  y = y * x
z = z + y

w = input[0]
x = 1
y = input[0]
z = input[0]

w = input[1]
x = 0
x = input[0]
  #x = x % 26
x = input[0] + 13
x = 0
x = 1
y = 0
y = 25
y = 26
z = input[0] * 26
y = 0
y = input[1]
y = input[1] + 8
z = input[0] + input[1] + 8

w = input[1]
x = 1
y = input[1] + 8
z = input[0] + input[1] + 8

w = input[2]
x = 0
y = 0
z = input[0] + input[1] + 8

w = input[3]
x = (input[0] + input[1] + 8) % 26 + 12

eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y


== char[12] ==
w = input[12] # inp w
x = z % 26 - 13 # mul x 0, add x z, mod x 26, add x -13
z = z / 26 # div z 26
x = 1 if (z % 26 - 13 == input[12]) else 0 # eql x w
x = 1 if x == 0 else 0
y = (25 * x) + 1 # mul y 0, add y 25, mul y x, add y 1
z = z * y # mul z y
y = (input[12] + 2) * x # mul y 0, add y w, add y, mul y x
z = z + (input[12] + 2) * x # add z y

== char[13] ==

w = don't care
x = don't care
y = don't care
z = ?

w = input[13] # inp w
x = 1 # mul x 0, add x z, mod x 26, div z 26, add x -6, eql x w, eql x 0
    y = 26 # mul y 0, add y 25, mul y x, add y 1
y = input[13] + 7 # mul y 0, add y w, add y 7, mul y x
z = z * 26 + y # mul z y, add z y
z = z * 26 + input[13] + 7


'''

# Part 2 #################################
