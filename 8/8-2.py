# regular imports ########################
import math
import os, sys
import itertools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
count = 0
for line in input_lines:
    outputs_str = line.split(" | ")[1]
    outputs = outputs_str.split(" ")

    for output in outputs:
        if len(output) == 2:
            count = count + 1
        elif len(output) == 4:
            count = count + 1
        elif len(output) == 3:
            count = count + 1
        elif len(output) == 7:
            count = count + 1

print count

# Part 2 #################################

'''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
'''

dictionary = {}
dictionary['abcefg'] = '0'
dictionary['cf'] = '1'
dictionary['acdeg'] = '2'
dictionary['acdfg'] = '3'
dictionary['bcdf'] = '4'
dictionary['abdfg'] = '5'
dictionary['abdefg'] = '6'
dictionary['acf'] = '7'
dictionary['abcdefg'] = '8'
dictionary['abcdfg'] = '9'

def get_mapped(input, mapper):
    mapped = ""
    for char in input:
        mapped = mapped + mapper[char]
    return mapped

output_digits = []
for line in input_lines:

    outputs_str = line.split(" | ")[1]
    outputs = outputs_str.split(" ")
    inputs_str = line.split(" | ")[0]
    inputs = inputs_str.split(" ")
    all_entries = []
    for i in inputs:
        all_entries.append(i)
    for output in outputs:
        all_entries.append(output)

    permutations = itertools.permutations('abcdefg')
    mapper = {}
    for perm in list(permutations):
        mapper['a'] = perm[0]
        mapper['b'] = perm[1]
        mapper['c'] = perm[2]
        mapper['d'] = perm[3]
        mapper['e'] = perm[4]
        mapper['f'] = perm[5]
        mapper['g'] = perm[6]

        match_found = True
        for i in all_entries:
            mapped_string = get_mapped(i, mapper)
            if "".join(sorted(mapped_string)) not in dictionary:
                match_found = False
                break
            #else:
            #    print "could be: "+dictionary["".join(sorted(mapped_string))]

        if match_found:
            break

    i_digit = ""
    for i in outputs:
        mapped_string = get_mapped(i, mapper)
        i_digit = i_digit + dictionary["".join(sorted(mapped_string))]
    output_digits.append(int(i_digit))

print output_digits
sum = 0
for i in output_digits:
    sum = sum + i

print sum
