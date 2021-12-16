# regular imports ########################
import math
import os, sys
from enum import Enum
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
def hexTo4BitBin(hex):
    output = ""
    for h in hex:
        binary = str(bin(int(h, 16)))[2:]
        while len(binary) < 4:
            binary = "0" + binary
        output += binary
    return output

class Packet:
    class State(Enum):
        GET_VERSION = 0
        GET_TYPE_ID = 1
        PROCESS_TYPE_ID = 2
        GET_LITERAL_VALUE = 3
        PROCESS_OPERATOR = 4

    def __init__(self, packet):
        self.packet = packet
        self.state = self.State.GET_VERSION
        self.instructionPointer = 0
        self.lengthTypeID = None
        self.operands = []
        self.totalLengthInBitsOfSubpackets = None
        self.literalValue = None
        self.typeID = None
        self.version = None
        self.numberOfSubPacketsImmediatelyContained = None

    def processPacket(self, debug=False):
        if debug: print("processing packet", self.packet, self.packet[self.instructionPointer:])

        if self.state == self.State.GET_VERSION:
            self.getVersion(debug)
        elif self.state == self.State.GET_TYPE_ID:
            self.getTypeID(debug)
        elif self.state == self.State.PROCESS_TYPE_ID:
            self.processTypeID(debug)
        elif self.state == self.State.GET_LITERAL_VALUE:
            self.getLiteralValue(debug)
        elif self.state == self.State.PROCESS_OPERATOR:
            self.processOperator(debug)

    def processOperator(self, debug=False):
        if debug: print("lengthTypeID", self.lengthTypeID)
        if self.lengthTypeID == 0:
            self.totalLengthInBitsOfSubpackets = int(self.packet[self.instructionPointer:self.instructionPointer+15], base=2)
            self.instructionPointer += 15
            if debug: print("totalLengthInBitsOfSubpackets", self.totalLengthInBitsOfSubpackets)
            endOfOperands = self.instructionPointer + self.totalLengthInBitsOfSubpackets
            while self.instructionPointer < endOfOperands:
                operandPacket = Packet(self.packet[self.instructionPointer:endOfOperands])
                operandPacket.processPacket(debug)
                if debug: print("advance instruction pointer by", operandPacket.instructionPointer)
                self.instructionPointer += operandPacket.instructionPointer
                self.operands.append(operandPacket)
        elif self.lengthTypeID == 1:
            self.numberOfSubPacketsImmediatelyContained = int(self.packet[self.instructionPointer:self.instructionPointer+11], base=2)
            self.instructionPointer += 11
            if debug: print("numberOfSubPacketsImmediatelyContained", self.numberOfSubPacketsImmediatelyContained)
            for i in range(self.numberOfSubPacketsImmediatelyContained):
                operandPacket = Packet(self.packet[self.instructionPointer:])
                operandPacket.processPacket(debug)
                if debug: print("advance instruction pointer by", operandPacket.instructionPointer)
                self.instructionPointer += operandPacket.instructionPointer
                self.operands.append(operandPacket)

    def getLiteralValue(self, debug=False):
        finishedExtractingValue = False
        literalBinaryString = ""
        while finishedExtractingValue is False:
            if debug: print("self.instructionPointer", self.instructionPointer, "length", len(self.packet))
            finishedExtractingValue = self.packet[self.instructionPointer] == "0"
            self.instructionPointer += 1
            literalBinaryString += self.packet[self.instructionPointer:self.instructionPointer+4]
            self.instructionPointer += 4
        if debug: print("literalBinaryString", literalBinaryString)
        self.literalValue = int(literalBinaryString, base=2)
        if debug: print("literalValue", self.literalValue)

    def processTypeID(self, debug=False):
        if self.typeID == 4:
            self.state = self.State.GET_LITERAL_VALUE
            self.processPacket(debug)
        else:
            self.state = self.State.PROCESS_OPERATOR
            self.lengthTypeID = int(self.packet[self.instructionPointer])
            self.instructionPointer += 1
            self.processPacket(debug)

    def getVersion(self, debug=False):
        self.version = int(self.packet[self.instructionPointer:self.instructionPointer+3], base=2)
        if debug: print("version", self.version, self.packet[self.instructionPointer:self.instructionPointer+3])
        self.instructionPointer += 3
        self.state = self.State.GET_TYPE_ID
        self.processPacket(debug)

    def getTypeID(self, debug=False):
        self.typeID = int(self.packet[self.instructionPointer:self.instructionPointer+3], base=2)
        self.instructionPointer += 3
        if debug: print("typeID", self.typeID)
        self.state = self.State.PROCESS_TYPE_ID
        self.processPacket(debug)

    def getValue(self, debug=False):
        if self.typeID == 4:
            return self.literalValue
        elif self.typeID == 0:
            sum = 0
            for o in self.operands:
                sum += o.getValue()
            return sum
        elif self.typeID == 1:
            product = 1
            for o in self.operands:
                product = product * o.getValue()
            return product
        elif self.typeID == 2:
            values = []
            for o in self.operands:
                values.append(o.getValue())
            return min(values)
        elif self.typeID == 3:
            values = []
            for o in self.operands:
                values.append(o.getValue())
            return max(values)
        elif self.typeID == 5:
            if self.operands[0].getValue() > self.operands[1].getValue():
                return 1
            else:
                return 0
        elif self.typeID == 6:
            if self.operands[0].getValue() < self.operands[1].getValue():
                return 1
            else:
                return 0
        elif self.typeID == 7:
            if self.operands[0].getValue() == self.operands[1].getValue():
                return 1
            else:
                return 0

def sumVersions(packet):
    sum = packet.version
    for o in packet.operands:
        sum += sumVersions(o)
    return sum

# actual code ############################
input_lines = helpers.read_lines_from_file('input_test.txt')

# Part 1 #################################
packet = hexTo4BitBin(input_lines[0])
packet = Packet(packet)
packet.processPacket(debug=False)

print sumVersions(packet)
print packet.getValue()

# Part 2 #################################
