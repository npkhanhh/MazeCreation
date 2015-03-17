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
    if grid[r][c].top == 0 and prev != 0 and path.count([r-1, c]) != 1:
        path.append([r-1, c])
        path_list = dfs_recursion(grid, size, path_list, path, r-1, c, 2)
        del path[-1]
    if grid[r][c].right == 0 and prev != 1 and path.count([r, c+1]) != 1:
        path.append([r, c+1])
        path_list = dfs_recursion(grid, size, path_list, path, r, c+1, 3)
        del path[-1]
    if grid[r][c].bottom == 0 and prev != 2 and path.count([r+1, c]) != 1:
        path.append([r+1, c])
        path_list = dfs_recursion(grid, size, path_list, path, r+1, c, 0)
        del path[-1]
    if grid[r][c].left == 0 and prev != 3 and path.count([r, c-1]) != 1:
        path.append([r, c-1])
        path_list = dfs_recursion(grid, size, path_list, path, r, c-1, 1)
        del path[-1]
    return path_list