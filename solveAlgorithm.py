__author__ = 'Khanh'
import copy

############## recursion dfs ##############
def dfs(grid, size):
    path_list = []
    path = [[0, 0]]
    path_list = dfs_recursion(grid, size, path_list, path, 0, 0, 0)
    return path_list

def dfs_recursion(grid, size, path_list, path, r, c, prev):
    if r==size-1 and c == size-1:
        pathtemp = copy.deepcopy(path)
        path_list.append(pathtemp)
        return path_list
    if grid[r][c].top == 0 and path.count([r-1, c]) != 1:
        path.append([r-1, c])
        path_list = dfs_recursion(grid, size, path_list, path, r-1, c, 2)
        del path[-1]
    if grid[r][c].right == 0 and path.count([r, c+1]) != 1:
        path.append([r, c+1])
        path_list = dfs_recursion(grid, size, path_list, path, r, c+1, 3)
        del path[-1]
    if grid[r][c].bottom == 0 and path.count([r+1, c]) != 1:
        path.append([r+1, c])
        path_list = dfs_recursion(grid, size, path_list, path, r+1, c, 0)
        del path[-1]
    if grid[r][c].left == 0 and path.count([r, c-1]) != 1:
        path.append([r, c-1])
        path_list = dfs_recursion(grid, size, path_list, path, r, c-1, 1)
        del path[-1]
    return path_list

def dfsIterative(grid, size):
    path_list = []
    path = [[0, 0]]
    stack = [[0, 0]]
    visited_from = [[[-1] for i in range(size)] for j in range(size)]
    while stack:
        cell = stack.pop(-1)
        r = cell[0]
        c = cell[1]
        if grid[r][c].top == 0 and path.count([r-1, c]) != 1:
            path.append([r-1, c])
            if r==size-1 and c == size-1:
                pathtemp = copy.deepcopy(path)
                path_list.append(pathtemp)
    return path_list

def dfsMarker(grid, size):
    marked = [[0 for i in range(size)] for i in range(size)]
    marker = 1
    row = 0
    column = 0
    marked[row][column] = marker
    marked = dfsRecursionMarker(grid, size, marked, marker, row, column, 0)
    marker = 2
    row = size-1
    column = size-1
    if marked[row][column] == 0:
        marked[row][column] = marker
    marked = dfsRecursionMarker(grid, size, marked, marker, row, column, 2)
    return marked

def dfsRecursionMarker(grid, size, marked, marker, r, c, prev):
    if grid[r][c].top == 0 and prev != 0 and marked[r-1][c] == 0:
        marked[r-1][c] = marker
        marked = dfsRecursionMarker(grid, size, marked, marker, r-1, c, 2)
    if grid[r][c].right == 0 and prev != 1 and marked[r][c+1] == 0:
        marked[r][c+1] = marker
        marked = dfsRecursionMarker(grid, size, marked, marker, r, c+1, 3)
    if grid[r][c].bottom == 0 and prev != 2 and marked[r+1][c] == 0:
        marked[r+1][c] = marker
        marked = dfsRecursionMarker(grid, size, marked, marker, r+1, c, 0)
    if grid[r][c].left == 0 and prev != 3 and marked[r][c-1] == 0:
        marked[r][c-1] = marker
        marked = dfsRecursionMarker(grid, size, marked, marker, r, c-1, 1)
    return marked