# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################

lantern_fish = helpers.convert_array_to_int(input_lines[0].split(","))
print "init: "+str(lantern_fish)

how_many_children_on_day = []
day_0 = []
for fish in range(9):
    day_0.append(1)
how_many_children_on_day.append(day_0)

runtime = 256

for idx in range(runtime):
    day = idx + 1
    #print "day "+str(day)+" memorized:"+str(how_many_children_on_day)

    # initialize a new set for this day
    day_new = []
    for fish in range(9):
        day_new.append(0)

    for fish in range(9):

        #print "fish="+str(fish)
        #print "day="+str(day)

        last_spawn_day = day - fish - 1 # since a fish doesn't spawn until it hits -1 idx
        #print "last_spawn_day="+str(last_spawn_day)

        fish_count = 1
        while last_spawn_day >= 0:
            # the spawn of the spawn will spawn!
            #print "how_many_children_on_day["+str(last_spawn_day)+"][8]="+str(how_many_children_on_day[last_spawn_day][8])
            fish_count = fish_count + how_many_children_on_day[last_spawn_day][8]
            last_spawn_day = last_spawn_day - 7

        #print "fish_count="+str(fish_count)

        day_new[fish] = fish_count

    how_many_children_on_day.append(day_new)

#for day in how_many_children_on_day:
#    print day

test_day = 2
for idx in range(9):
    print "Age "+str(idx)+" fish on day "+str(test_day)+" will spawn " + str(how_many_children_on_day[test_day][idx]) + " fish"

for idx in range(256):
    test_day = idx + 1
    sum = 0
    for fish in lantern_fish:
        if test_day == 2:
            print "fish "+str(fish) + " spawned: "+str(how_many_children_on_day[test_day][fish]) + " over "+str(test_day) + " days"
        sum = sum + how_many_children_on_day[test_day][fish]
    print "After "+str(test_day) + " days: "+str(sum)


sum = 0
for fish in lantern_fish:
    sum = sum + how_many_children_on_day[test_day][fish]
print sum

# Part 2 #################################
