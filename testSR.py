'''
Created on Apr 29, 2015

@author: ldhuy
'''
import graphic as gp
import solveRegion as sr
size = 3
grid = [[]]



#     +  ------+
#     |     |  |
#     |__|__   |
#     |__    __|
#     +--------+
def createMaze1():
    global size
    global grid
    grid = [[gp.Cell() for i in range(size)] for j in range(size)]
    
    grid[0][0].top = 0
    grid[0][0].bottom = 0
    grid[0][0].right = 0
    grid[0][1].left = 0
    grid[0][1].bottom = 0
    grid[0][2].bottom = 0
    
    grid[1][0].top = 0
    grid[1][1].top = 0
    grid[1][1].right = 0
    grid[1][2].left = 0
    grid[1][2].bottom = 0
    grid[1][2].top = 0
    
    grid[2][0].right = 0
    grid[2][1].left = 0
    grid[2][1].right = 0
    grid[2][1].bottom = 0
    grid[2][2].left = 0
    grid[2][2].top = 0





createMaze1()
pairs = sr.sovleRegion(grid, 0, 0, 3, 3, 3)
print pairs