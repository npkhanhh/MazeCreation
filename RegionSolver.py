"""
Created on May 26, 2015

@author: ldhuy
"""
import threading

class RegionSolver(threading.Thread):
    """
    Run as a single thread, solve one specified region and save the result to the parameter 'regionMap'
    """

    def __init__(self, grid, top, left, right, bottom, xRegionMap, yRegionMap, pathMap, regionMapLock):
        threading.Thread.__init__(self)
        self.grid = grid
        self.top = top
        self.left= left
        self.right = right
        self.bottom = bottom
        self.xRegionMap = xRegionMap
        self.yRegionMap = yRegionMap
        self.regionMap = pathMap
        self.regionMapLock = regionMapLock
        
        
        
    def run(self):
        solution = self.sovleRegion(self.grid, self.top, self.left, self.right, self.bottom)
        # Acquire lock
        if self.regionMapLock.acquire() == 1:
            self.regionMap[self.xRegionMap][self.yRegionMap] = solution
            self.regionMapLock.release()
    
    def hasEntrance(self, grid, top, left, right, bottom, row, col, directions):
        """
        Check if this cell has entrance
        A cell has entrance only if it lies at the boundary and has a missing border
        Params:
            grid: the whole maze
            row, col: coordinate of the current cell
            directions: a list to store the directions of the entrance wrt this cell, this can be use as an additional result
                            (a cell can have more than one entrance if it is at the corner of the region
        Return: True if the cell has entrance, False if not
        """
        result = False
        if row == top and grid[row][col].top == 0:
            result = True
            directions.append('top')
        if row == bottom - 1 and grid[row][col].bottom == 0:
            result = True
            directions.append('bottom')
        if col == left and grid[row][col].left == 0:
            result = True
            directions.append('left')
        if col == right - 1 and grid[row][col].right == 0:
            result = True
            directions.append('right')
        return result
    
    
    
    
    def findPath(self, grid, top, left, right, bottom, row, col, direction, length, path):
        """
        Params:
            grid: the whole maze
            row, col: coordinate of the current cell
            direction: the direction of the current cell with respect to the previous cell
            length: the length of the path from the cell that calls this method up to the current cell (starting cell and ending cell included)
            path: an array of string stores that path ([row1, col1], [row2, col2], ...)
        Return: list of paths that connect neighbor regions. Format: [path1, path2, ...]
        """
        entranceCellList = []       # entranceCellList is a list stores coordinates of cells in paths that connects neighbor regions
                                    # [[row1, col1], [row2, col2], ...]
        # Check if this cell has entrance
        entranceAt = []    # list of directions of the entrance of this cell
        appended = False
        if self.hasEntrance(grid, top, left, right, bottom, row, col, entranceAt):
            path.append([row, col])
            appended = True
#             entranceCellList = entranceCellList.append(path)
            entranceCellList.append(path)
        
        
        if direction != 'right' and 'left' not in entranceAt and col > left and grid[row][col].left == 0:    # check left cell
            pathNew = list(path)
            if not appended:
                pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col - 1, 'left', length + 1, pathNew)
            #entranceCellList = entranceCellList + entranceCells
            for p in entranceCells:
                entranceCellList.append(p)
        if direction != 'top' and 'bottom' not in entranceAt and row < bottom - 1 and grid[row][col].bottom == 0:    # check bottom cell
            pathNew = list(path)
            if not appended:
                pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row + 1, col, 'bottom', length + 1, pathNew)
            #entranceCellList = entranceCellList + entranceCells
            for p in entranceCells:
                entranceCellList.append(p)
        if direction != 'left' and 'right' not in entranceAt and col < right - 1 and grid[row][col].right == 0:    # check right cell
            pathNew = list(path)
            if not appended:
                pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col + 1, 'right', length + 1, pathNew)
            #entranceCellList = entranceCellList + entranceCells
            for p in entranceCells:
                entranceCellList.append(p)
        if direction != 'bottom' and 'top' not in entranceAt and row > top and grid[row][col].top == 0:    # check top cell
            pathNew = list(path)
            if not appended:
                pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row - 1, col, 'top', length + 1, pathNew)
            #entranceCellList = entranceCellList + entranceCells
            for p in entranceCells:
                entranceCellList.append(p)
            
        return entranceCellList
    
    
    
    
    
    def sovleRegion(self, grid, top, left, right, bottom):
        """
        Find pairs of connected entrances of the regions
        Params:
            grid: the matrix represent the whole maze
            top, left, right, bottom:    co-ordinate of the top left and right bottom corners of the region
                                        (the 'right' column and 'bottom' row are exclusive)
        Return: list of paths that connect neighbor regions
        """
        entrancePairList = []   # List of paths that connect neighbor regions
        for c in  range(left, right):
            for r in range(top, bottom):
                if (c == left or c == right - 1) or (r == top or r == bottom - 1):    # Only examine cells at the boundary
                    entranceAt = []    # list of entrance of this cell
                    if self.hasEntrance(grid, top, left, right, bottom, r, c, entranceAt):
                        if  'right' in entranceAt and 'top' in entranceAt or \
                            'right' in entranceAt and 'bottom' in entranceAt or \
                            'left' in entranceAt and 'top' in entranceAt or \
                            'left' in entranceAt and 'bottom' in entranceAt:    # Check if this cell is at the corner of region and has 2 entrance
                            entrancePairList = entrancePairList + [[[r, c]]]
                        for i in range(len(entranceAt)):
                            if entranceAt[i] != 'right' and c + 1 < right and grid[r][c].right == 0:
                                foundEntrances = []    # list of entrances found by findPath method
                                path = [[r, c]]
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r, c + 1, 'right', 1, path)
                                if len(foundEntrances) > 0:
                                    entrancePairList = entrancePairList + foundEntrances
                            if entranceAt[i] != 'bottom' and r + 1 < bottom and grid[r][c].bottom == 0:
                                foundEntrances = []    # list of entrances found by findPath method
                                path = [[r, c]]
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r + 1, c, 'bottom', 1, path)
                                if len(foundEntrances) > 0:
                                    entrancePairList = entrancePairList + foundEntrances
                            if entranceAt[i] != 'left' and c - 1 >= left and grid[r][c].left == 0:
                                foundEntrances = []    # list of entrances found by findPath method
                                path = [[r, c]]
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r, c - 1, 'left', 1, path)
                                if len(foundEntrances) > 0:
                                    entrancePairList = entrancePairList + foundEntrances
                            if entranceAt[i] != 'top' and r - 1 >= top and grid[r][c].top == 0:
                                foundEntrances = []    # list of entrances found by findPath method
                                path = [[r, c]] 
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r - 1, c, 'top', 1, path)
                                if len(foundEntrances) > 0:
                                    entrancePairList = entrancePairList + foundEntrances
        
        # Remove duplicated paths
        i1 = 0
        while i1 < len(entrancePairList):#for i1 in range1:
            i2 = 0
            while i2 < len(entrancePairList):#for i2 in range1:
                if i2 != i1:
                    reversedList = list(reversed(entrancePairList[i2]))
                    if reversedList == entrancePairList[i1]:
                        entrancePairList.pop(i2)
#                     if  entrancePairList[i1][0] == entrancePairList[i2][len(entrancePairList[i2])-1] and entrancePairList[i1][len(entrancePairList[i1])-1] == entrancePairList[i2][0]:
#                         entrancePairList.pop(i2)
                if i2 == len(entrancePairList) - 1:
                    break
                i2 += 1
            if i1 == len(entrancePairList) - 1:
                break
            i1 += 1
            
        return entrancePairList


