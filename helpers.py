def read_lines_from_file(file_name):
  input_file = open(file_name, "r")
  input_lines = input_file.readlines()
  input_file.close()
  cleaned_lines = []
  for line in input_lines:
    cleaned_lines.append(line.strip())
  return cleaned_lines

def convert_array_to_int(arr):
  int_arr = []
  for i in arr:
    int_arr.append(int(i))
  return int_arr

def get_grid_from_lines(input_lines):
  grid = {}
  y = 0
  for line in input_lines:
    x = 0
    for c in line:
      if x not in grid:
        grid[x] = {}
      grid[x][y] = c
      #print(str(x)+","+str(y)+"="+c)
      x = x+1
    y = y+1
  return grid

def print_grid(grid):
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    line = ""
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      #print(str(x) + "," + str(y) + "=" + grid[x][y])
      line = line + str(grid[x][y])
    print(line)

def get_grid_col_count(grid):
  return len(grid.keys())

def get_grid_row_count(grid):
  return len(grid[0].keys())

def transform_flip_x(grid):
  new_grid = {}
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      new_x = max_x - x
      if new_x not in new_grid:
        new_grid[new_x] = {}
      new_grid[new_x][y] = grid[x][y]
  return new_grid

def transform_flip_y(grid):
  new_grid = {}
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      new_x = x
      new_y = max_y - y
      if new_x not in new_grid:
        new_grid[new_x] = {}
      new_grid[new_x][new_y] = grid[x][y]
  return new_grid

def transform_rotate_90(grid):
  new_grid = {}
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      new_x = max_y - y
      new_y = x
      #print("x,y from "+str(x)+","+str(y)+" to "+str(new_x)+","+str(new_y))
      if new_x not in new_grid:
        new_grid[new_x] = {}
      new_grid[new_x][new_y] = grid[x][y]
  return new_grid

def add_to_grid(x, y, value, grid):
  if x not in grid:
    grid[x] = {}
  grid[x][y] = value

def copy_grid(grid):
  new_grid = {}
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      new_x = x
      new_y = y
      if new_x not in new_grid:
        new_grid[new_x] = {}
      new_grid[new_x][new_y] = grid[x][y]
  return new_grid

def copy_grid_partial(grid, min_x, min_y, max_x, max_y):
  new_grid = {}
  for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
      new_x = x
      new_y = y
      if new_x - min_x not in new_grid:
        new_grid[new_x - min_x] = {}
      new_grid[new_x - min_x][new_y - min_y] = grid[x][y]
  return new_grid

def convert_grid_to_int(grid):
  new_grid = {}
  min_y = min(grid[0].keys())
  max_y = max(grid[0].keys())
  for y in range(min_y, max_y+1):
    min_x = min(grid.keys())
    max_x = max(grid.keys())
    for x in range(min_x, max_x+1):
      new_x = x
      new_y = y
      if new_x not in new_grid:
        new_grid[new_x] = {}
      new_grid[new_x][new_y] = int(grid[x][y])
  return new_grid

def init_grid(max_x, max_y, init_value):
  grid = {}
  min_x = 0
  min_y = 0
  for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
      new_x = x
      new_y = y
      if new_x not in grid:
        grid[new_x] = {}
      grid[new_x][new_y] = init_value
  return grid
