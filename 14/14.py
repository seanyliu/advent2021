# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
template = input_lines.pop(0)
template2 = template
input_lines.pop(0) # remove white space

rules = {}
for line in input_lines:
    rules[line.split(" -> ")[0]] = line.split(" -> ")[1]

# polymer operations
for i in range(10):

    # generate insertions
    insertions = []
    for pattern in rules:
        for j in range(len(template)-1):
            if template[j] == pattern[0] and template[j+1] == pattern[1]:
                insertions.append((j, rules[pattern]))
    insertions.sort(key = lambda x: x[0])

    # do insertions
    offset = 0
    for insert in insertions:
        offset = offset + 1
        index = insert[0] + offset
        template = template[:index] + insert[1] + template[index:]

# count elements
count = {}
for char in template:
    if char not in count:
        count[char] = 0
    count[char] = count[char] + 1

print max(count.values()) - min(count.values())


# Part 2 #################################
bigrams = {}
template = template2

# convert template into bigrams
for i in range(len(template)-1):
    bigram = template[i] + template[i+1]
    if bigram not in bigrams:
        bigrams[bigram] = 0
    bigrams[bigram] = bigrams[bigram] + 1

for i in range(40):
    # generate insertions
    insertions = {}
    for pattern in rules:
        if pattern in bigrams and bigrams[pattern] > 0:
            newbigram1 = pattern[0] + rules[pattern]
            newbigram2 = rules[pattern] + pattern[1]
            if newbigram1 not in insertions:
                insertions[newbigram1] = 0
            if newbigram2 not in insertions:
                insertions[newbigram2] = 0
            insertions[newbigram1] = insertions[newbigram1] + bigrams[pattern]
            insertions[newbigram2] = insertions[newbigram2] + bigrams[pattern]

    # zero out the insertions
    for pattern in rules:
        if pattern in bigrams and bigrams[pattern] > 0:
            bigrams[pattern] = 0

    # do insertions
    for insert in insertions.keys():
        if insert not in bigrams:
            bigrams[insert] = 0
        bigrams[insert] = bigrams[insert] + insertions[insert]

print bigrams

# count elements
count = {}
for bigram in bigrams.keys():
    if bigram[0] not in count:
        count[bigram[0]] = 0
    count[bigram[0]] = count[bigram[0]] + bigrams[bigram]
count[template2[-1]] = count[template2[-1]] + 1 # last character
print count
print max(count.values()) - min(count.values())
