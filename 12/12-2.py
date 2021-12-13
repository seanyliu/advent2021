# regular imports ########################
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers

# functions ##############################
nodes_dict = {}
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor, nodes_dict):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            if neighbor not in nodes_dict:
                nodes_dict[neighbor] = Node(neighbor)
            nodes_dict[neighbor].add_neighbor(self.name, nodes_dict)

    def print_neighbors(self):
        output = ""
        for neighbor in self.neighbors:
            output = output + "," + neighbor
        return output

    def get_neighbors(self):
        return self.neighbors

# actual code ############################
input_lines = helpers.read_lines_from_file('input.txt')

# Part 2 #################################
for line in input_lines:
    a = line.split("-")[0]
    b = line.split("-")[1]
    if a not in nodes_dict:
        nodes_dict[a] = Node(a)
    if b not in nodes_dict:
        nodes_dict[b] = Node(b)
    nodes_dict[a].add_neighbor(b, nodes_dict)

#for key in nodes_dict:
#    print(key, '->', nodes_dict[key].print_neighbors())

history = set() # string of past visited nodes
q = []
q.append("0:start")
history.add("0:start")

while len(q) > 0:
    node = q.pop()
    small_caves_visited = []
    current = nodes_dict[node.split(":")[1].split("-")[-1]]
    if current.name == "end":
        continue
    for cave in node.split("-"):
        if cave.islower():
            small_caves_visited.append(cave)
    for neighbor in current.get_neighbors():
        if neighbor == "start":
            continue
        if neighbor not in small_caves_visited:
            path = node + "-" + nodes_dict[neighbor].name
            if path not in history:
                q.append(path)
                history.add(path)
        else:
            small_cave_visited_twice = int(node.split(":")[0])
            if small_cave_visited_twice == 0:
                path = "1:" + node.split(":")[1] + "-" + nodes_dict[neighbor].name
                if path not in history:
                    q.append(path)
                    history.add(path)

solutions_count = 0
for path in history:
    if path.split("-")[-1] == "end":
        solutions_count = solutions_count + 1
        print path

print solutions_count
