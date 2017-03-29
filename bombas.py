# https://www.codingame.com/ide/puzzle/vox-codei-episode-1

import numpy as np
from collections import defaultdict

def reset_grid(grid, best_bomb):
    '''reset to zero all the target locations that will be bombed this turn'''
    x,y = best_bomb
    for i in range(1,4):
        if (x+i, y) in targets:
            grid[x+i, y] = 0
        if (x-i, y) in targets:
            grid[x-i, y] = 0
        if (x, y+i) in targets:
            grid[x, y+i] = 0
        if (x, y-i) in targets:
            grid[x, y-i] = 0
    return grid

def determine_targets_hit(open_spaces, targets, best_bomb, t):
    '''add all target locations to the open_locations dict with the time
       at which they will become available'''
    x,y = best_bomb
    targets_hit = set()
    for i in range(1,4):
        if (x+i, y) in targets:
            targets_hit.add((x+i, y))
        if (x-i, y) in targets:
            targets_hit.add((x-i, y))
        if (x, y+i) in targets:
            targets_hit.add((x, y+i))
        if (x, y-i) in targets:
            targets_hit.add((x, y-i))
    for hit in targets_hit:
        open_spaces[hit] = t+3
    return targets_hit

def compute_damage(legal_targets, grid):
    '''for all legal targets check any targets within the squares of influece,
       check if any blocks are hit and stop there (non penetrating explosions)'''
    damage_dict = defaultdict(lambda: [])
    for (x, y) in legal_targets:
        total = 0
        for i in range(1,4):
            if (x+i, y) in blocks:
                break
            if x+i < height:
                total += grid[x+i, y]
        for i in range(1,4):
            if (x-i, y) in blocks:
                break
            if x-i >= 0:
                total += grid[x-i, y]
        for i in range(1,4):
            if (x, y+i) in blocks:
                break
            if y+i < width:
                total += grid[x, y+i]
        for i in range(1,4):
            if (x, y-i) in blocks:
                break
            if y-i >= 0:
                total += grid[x, y-i]
        damage_dict[total].append((x, y))
    return damage_dict

map = ['.'*10,
       '.'*5 + '#' + '@'*2 + '#' + '.'*1, 
       '.'*10, 
       '.'*10, 
       '.'*10, 
       '.'*2 + '.'*3 + '.'*5,
       '.'*2 + '@' + '.'*7, 
       '.'*10,  
       '.'*10]

# map = ['..........',
#        '..........',
#        '..........',
#        '..........',
#        '..........',
#        '.......@..',
#        '.....@@@@.',
#        '.......@..',]
       
# map = ['.'*4,
#        '@' + '.' + '@'*2,
#        '.'*4,]
for row in map:
    print row
     
targets = set()
blocks = set()
width, height = len(map[0]), len(map)
grid = np.zeros([height, width])
for row in xrange(height):
    map_row = map[row]  # one line of the firewall grid
    for col, x in enumerate(map_row):
        if x == '@':
            grid[row, col] = 1
            targets.add((row, col))
        if x == '#':
            blocks.add((row, col))
            
legal_targets = {(i,j) for i in range(height) for j in range(width)} - blocks - targets
bomb_coords = []

bombs = 1
open_spaces = defaultdict(lambda: 0)
for t in range(5):    
    # rounds: number of rounds left before the end of the game
    # To debug: print >> sys.stderr, "Debug messages..."
    if np.sum(grid) > 0:
        damage_dict = compute_damage(legal_targets, grid)
        best_bomb = damage_dict[max(damage_dict)][0]
        targets_hit = determine_targets_hit(open_spaces, targets, best_bomb, t)
        if open_spaces[best_bomb] <= t:
            grid = reset_grid(grid, best_bomb)
            targets -= targets_hit
            legal_targets = legal_targets | set(open_spaces.keys())
            x, y = best_bomb
            print str(x) + ' ' + str(y)
        else:
            print 'WAIT'   
    else:
        print 'WAIT'    