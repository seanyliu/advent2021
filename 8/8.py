# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input_test.txt')

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

elimination = {}
elimination['0'] = {'d'}
elimination['1'] = {'a', 'b', 'd', 'e', 'g'}
elimination['2'] = {'b', 'f'}
elimination['3'] = {'b', 'e'}
elimination['4'] = {'a', 'e', 'g'}
elimination['5'] = {'c', 'e'}
elimination['6'] = {'c'}
elimination['7'] = {'b', 'd', 'e', 'g'}
elimination['8'] = set()
elimination['9'] = {'e'}

def simplify_map(mapper):
    simplification_made = True
    processed = set()
    while simplification_made == True:
        simplification_made = False
        for key in mapper:
            e = next(iter(mapper[key]))
            if len(mapper[key]) == 1 and (key not in processed):
                processed.add(key)
                for key2 in mapper:
                    if key2 != key and e in mapper[key2]:
                        mapper[key2].remove(e)
                simplification_made = True
                break
    return mapper

for line in input_lines:
    mapper = {}
    mapper['a'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['b'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['c'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['d'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['e'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['f'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    mapper['g'] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

    outputs_str = line.split(" | ")[1]
    outputs = outputs_str.split(" ")

    inputs_str = line.split(" | ")[0]
    inputs = inputs_str.split(" ")

    all_entries = []
    for i in inputs:
        all_entries.append(i)
    for output in outputs:
        all_entries.append(output)

    elim_made = True
    while elim_made == True:
        elim_made = False
        for i in all_entries:
            elim = set()

            if len(i) == 2:
                # must be printing '1'
                elim = elimination['1']

            elif len(i) == 4:
                # must be printing '4'
                elim = elimination['4']

            elif len(i) == 3:
                # must be printing '7'
                elim = elimination['7']

            elif len(i) == 7:
                # must be printing '8'
                elim = elimination['8']

            elif len(i) == 6:
                # either a '0', '9', or a '6'
                # if 'e' isn't an option in any, then we know we have a 6
                e_is_option = False
                for j in i:
                    if 'e' in mapper[j]:
                        e_is_option = True
                        break
                if not e_is_option:
                    print e_is_option

                # if 'c' isn't an option in any, then we know we have a 9
                c_is_option = False
                for j in i:
                    if 'c' in mapper[j]:
                        c_is_option = True
                        break
                if not c_is_option:
                    print c_is_option

                # if 'd' isn't an option in any, then we know we have a 0
                d_is_option = False
                for j in i:
                    if 'd' in mapper[j]:
                        d_is_option = True
                        break
                if not d_is_option:
                    print d_is_option

            elif len(i) == 5:
                # either a '2', '3', '5'
                # if there's a letter in all of the 5 letters, then we can eliminate 'a'/'d'/'g' from the mapping


            for e in elim:
                for char in i:
                    if e in mapper[char]:
                        mapper[char].remove(e)
                        elim_made = True
            simplify_map(mapper)
    print mapper
