__author__ = 'Khanh'
import random
import timeit

###################################### Recursive Backtracker ##############################################

def recursiveBacktracker(grid, size):
    visited = [[0 for i in range(size)] for j in range(size)]
    r = random.randint(0, size-1)
    c = random.randint(0, size-1)
    grid = carvePath(r, c, grid, visited, size)
    return grid

def carvePath(r, c, grid, visited, size):
    visited[r][c] = 1
    dir = [0, 1, 2, 3]
    random.shuffle(dir)
    for i in range(len(dir)):
        if dir[i] == 0:
            if r > 0 and visited[r-1][c] == 0:
                grid[r][c].top = 0
                grid[r-1][c].bottom = 0
                grid = carvePath(r-1, c, grid, visited, size)
        if dir[i] == 1:
            if c < size-1 and visited[r][c+1] == 0:
                grid[r][c].right = 0
                grid[r][c+1].left = 0
                grid = carvePath(r, c+1, grid, visited, size)
        if dir[i] == 2:
            if r < size-1 and visited[r+1][c] == 0:
                grid[r][c].bottom = 0
                grid[r+1][c].top = 0
                grid = carvePath(r+1, c, grid, visited, size)
        if dir[i] == 3:
            if c > 0 and visited[r][c-1] == 0:
                grid[r][c].left = 0
                grid[r][c-1].right = 0
                grid = carvePath(r, c-1, grid, visited, size)
    return grid

###################################### Backtracker algorithm ##############################################

def backtracker(grid, size):
    visited = [[0 for i in range(size)] for j in range(size)]
    r = random.randint(0, size-1)
    c = random.randint(0, size-1)
    dir = [0, 1, 2, 3]
    pathstack = [[r,c]]
    visited[r][c] = 1
    while(pathstack):
        cell = pathstack[-1]
        r = cell[0]
        c = cell[1]
        if (r==0 or visited[r-1][c]==1) and (c==size-1 or visited[r][c+1]==1) and (r==size-1 or visited[r+1][c]==1) and (c==0 or visited[r][c-1]==1):
            pathstack.pop(-1)
        else:
            random.shuffle(dir)
            for i in range(len(dir)):
                if dir[i] == 0:
                    if r > 0 and visited[r-1][c] == 0:
                        grid[r][c].top = 0
                        grid[r-1][c].bottom = 0
                        visited[r - 1][c] = 1
                        pathstack.append([r-1, c])
                        break
                if dir[i] == 1:
                    if c < size-1 and visited[r][c+1] == 0:
                        grid[r][c].right = 0
                        grid[r][c+1].left = 0
                        visited[r][c+1] = 1
                        pathstack.append([r, c+1])
                        break
                if dir[i] == 2:
                    if r < size-1 and visited[r+1][c] == 0:
                        grid[r][c].bottom = 0
                        grid[r+1][c].top = 0
                        visited[r+1][c] = 1
                        pathstack.append([r+1, c])
                        break
                if dir[i] == 3:
                    if c > 0 and visited[r][c-1] == 0:
                        grid[r][c].left = 0
                        grid[r][c-1].right = 0
                        visited[r][c-1] = 1
                        pathstack.append([r, c-1])
                        break
    return grid


###################################### Kruskal algorithm ##############################################

def kruskal(grid, size):
    tic = timeit.default_timer()
    set = [[0 for i in range(size)] for j in range(size)]
    edge = []
    index = 0
    for r in range(size):
        for c in range(size):
            set[r][c] = index
            index += 1
    index = 0
    for r in range(size-1):
        for c in range(size-1):
            edge.append([index,index+1])
            edge.append([index,index+size])
            index += 1
        edge.append([index,index+size])
        index += 1
    for c in range(size-1):
        edge.append([index, index+1])
        index += 1
    random.shuffle(edge)
    for i in range(len(edge)):
        index1 = edge[i][0]
        index2 = edge[i][1]
        r1 = index1 / size
        c1 = index1 % size
        r2 = index2 / size
        c2 = index2 % size
        if set[r1][c1] != set[r2][c2]:
            if index2 - index1 > 1:
                grid[r1][c1].bottom = 0
                grid[r2][c2].top = 0
            else:
                grid[r1][c1].right = 0
                grid[r2][c2].left = 0
            if set[r1][c1] < set[r2][c2]:
                min = set[r1][c1]
                max = set[r2][c2]
            else:
                min = set[r2][c2]
                max = set[r1][c1]
            for r in range(size):
                for c in range(size):
                    if set[r][c] == max:
                        set[r][c] = min
                #set[r] = [min if w==max else w for w in set[r]]
        #print str(i) + '/' + str(len(edge))
    toc = timeit.default_timer()
    print(toc-tic)
    return grid