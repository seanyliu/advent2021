# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 1 #################################
depths_arr = helpers.convert_array_to_int(input_lines)
increased_count = 0
prev_depth = 0
for depth in depths_arr:
  if prev_depth != 0:
    if depth > prev_depth:
      increased_count = increased_count + 1
  prev_depth = depth
 
print increased_count 

# Part 2 #################################

window_depths = []
for i in range(len(depths_arr)):
  window_sum = depths_arr[i]
  if i+1 < len(depths_arr):
    window_sum = window_sum + depths_arr[i+1]
  if i+2 < len(depths_arr):
    window_sum = window_sum + depths_arr[i+2]
  window_depths.append(window_sum)

increased_count = 0
prev_depth = 0
for depth in window_depths:
  if prev_depth != 0:
    if depth > prev_depth:
      increased_count = increased_count + 1
  prev_depth = depth
 
print increased_count 
