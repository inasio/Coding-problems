import sys
import math
import numpy as np
from collections import defaultdict

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# width: width of the firewall grid
# height: height of the firewall grid

def compute_damage(x,y):
    total = 0
    for i in range(1,4):
        if x+i < height:
            total += grid[x+i, y]
        if x-i >= 0:
            total += grid[x-i, y]
        if y+i < width:
            total += grid[x, y+i]
        if y-i >= 0:
            total += grid[x, y-i]
    return total


targets = set()
blocks = set()
width, height = [int(i) for i in raw_input().split()]
grid = np.zeros([height, width])
for row in xrange(height):
    map_row = raw_input()  # one line of the firewall grid
    for col, x in enumerate(map_row):
        if x == '@':
            grid[row, col] = 1
            targets.add((row, col))
        if x == '#':
            blocks.add((row, col))

legal_targets = {(i,j) for i in range(height) for j in range(width)} - blocks - targets
damage_dict = defaultdict(lambda: [])
for (x,y) in legal_targets:
    damage = compute_damage(x,y)
    damage_dict[damage].append((x,y))
    
bomb_coords = []
sorted_damage = sorted(damage_dict.keys(),reverse=True)
for damage in sorted_damage:
    for coords in damage_dict[damage]:
        bomb_coords.append(coords)

while True:
    # rounds: number of rounds left before the end of the game
    # bombs: number of bombs left
    rounds, bombs = [int(i) for i in raw_input().split()]

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    if bombs:
        x, y = bomb_coords.pop(0)
        # x, y = height, width
        print str(y) + ' ' + str(x)
    else:
        print 'WAIT'     
    # print >> sys.stderr, "Debug messages..."
    # print "3 0"
