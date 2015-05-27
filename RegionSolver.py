"""
Created on May 26, 2015

@author: ldhuy
"""
import threading

class RegionSolver(threading.Thread):
    """
    Run as a single thread, solve one specified region and save the result to the parameter 'regionMap'
    """

    def __init__(self, grid, top, left, right, bottom, xRegionMap, yRegionMap, regionMap, regionMapLock):
        threading.Thread.__init__(self)
        self.grid = grid
        self.top = top
        self.left= left
        self.right = right
        self.bottom = bottom
        self.xRegionMap = xRegionMap
        self.yRegionMap = yRegionMap
        self.regionMap = regionMap
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
            path: an array of string stores that path (['left', 'right', 'left', ....])
        Return: list of cells that has entrance with the format: [[row, col, length of path, [path]], ]
        """
        entranceCellList = []        # entranceCellList is a list stores coordinates of cells that have entrance(s)
                                    # [[row, col, length of path, [path]], ]
        # Check if this cell has entrance
        entranceAt = []    # list of directions of the entrance of this cell
        if self.hasEntrance(grid, top, left, right, bottom, row, col, entranceAt):
            entranceCellList.append([row, col, length + 1, path])
        
        if direction != 'right' and 'left' not in entranceAt and col > left and grid[row][col].left == 0:    # check left cell
            pathNew = list(path)
            pathNew.append('left')
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col - 1, 'left', length + 1, pathNew)
            entranceCellList = entranceCellList + entranceCells
        if direction != 'top' and 'bottom' not in entranceAt and row < bottom - 1 and grid[row][col].bottom == 0:    # check bottom cell
            pathNew = list(path)
            pathNew.append('bottom')
            entranceCells = self.findPath(grid, top, left, right, bottom, row + 1, col, 'bottom', length + 1, pathNew)
            entranceCellList = entranceCellList + entranceCells
        if direction != 'left' and 'right' not in entranceAt and col < right - 1 and grid[row][col].right == 0:    # check right cell
            pathNew = list(path)
            pathNew.append('right')
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col + 1, 'right', length + 1, pathNew)
            entranceCellList = entranceCellList + entranceCells
        if direction != 'bottom' and 'top' not in entranceAt and row > top and grid[row][col].top == 0:    # check top cell
            pathNew = list(path)
            pathNew.append('top')
            entranceCells = self.findPath(grid, top, left, right, bottom, row - 1, col, 'top', length + 1, pathNew)
            entranceCellList = entranceCellList + entranceCells
            
        return entranceCellList
    
    
    
    
    
    def sovleRegion(self, grid, top, left, right, bottom):
        """
        Find pairs of connected entrances of the regions
        Params:
            grid: the matrix represent the whole maze
            top, left, right, bottom:    co-ordinate of the top left and right bottom corners of the region
                                        (the 'right' column and 'bottom' row are exclusive)
        Return: list of pairs of cells that has entrance(s) and connected
        """
        entrancePairList = []    # entrancePairList is a 3D array stores pairs of cells that have entrance(s) and connected 
                                    # format: [[[entrance1X, entrance1Y], [entrance2X, entrance2Y]], [[entrance2X, entrance2Y], [entrance3X, entrance3Y]], ...]
        for c in  range(left, right):
            for r in range(top, bottom):
                if (c == left or c == right - 1) or (r == top or r == bottom - 1):    # Only examine cells at the boundary
                    entranceList = []    # list of entrance of this cell
                    if self.hasEntrance(grid, top, left, right, bottom, r, c, entranceList):    # check if there is entrance to the left of this cell
                        for i in range(len(entranceList)):
                            if entranceList[i] != 'right' and c + 1 < right and grid[r][c].right == 0:
                                foundEntrances = []    # list of entrances found by findPath method 
                                path = ['right']
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r, c + 1, 'right', 1, path)
                                if len(foundEntrances) > 0:
                                    for j in range(len(foundEntrances)):    # add pairs to entrancePairList
                                        entrancePairList.append([[r, c], foundEntrances[j]])
                            if entranceList[i] != 'bottom' and r + 1 < bottom and grid[r][c].bottom == 0:
                                foundEntrances = []    # list of entrances found by findPath method 
                                path = ['bottom']
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r + 1, c, 'bottom', 1, path)
                                if len(foundEntrances) > 0:
                                    for j in range(len(foundEntrances)):    # add pairs to entrancePairList
                                        entrancePairList.append([[r, c], foundEntrances[j]])
                            if entranceList[i] != 'left' and c - 1 >= left and grid[r][c].left == 0:
                                foundEntrances = []    # list of entrances found by findPath method 
                                path = ['left']
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r, c - 1, 'left', 1, path)
                                if len(foundEntrances) > 0:
                                    for j in range(len(foundEntrances)):    # add pairs to entrancePairList
                                        entrancePairList.append([[r, c], foundEntrances[j]])
                            if entranceList[i] != 'top' and r - 1 >= top and grid[r][c].top == 0:
                                foundEntrances = []    # list of entrances found by findPath method
                                path = ['top'] 
                                foundEntrances = self.findPath(grid, top, left, right, bottom, r - 1, c, 'top', 1, path)
                                if len(foundEntrances) > 0:
                                    for j in range(len(foundEntrances)):    # add pairs to entrancePairList
                                        entrancePairList.append([[r, c], foundEntrances[j]])
        
        # Remove duplicate cells
        listSize = len(entrancePairList)
        for i in range(listSize):
            for i2 in range(listSize):
                if i2 != i:
                    if    (entrancePairList[i][0] == entrancePairList[i2][1][0:2] and entrancePairList[i][1][0:2] == entrancePairList[i2][0]) or \
                        (entrancePairList[i][0] == entrancePairList[i2][0] and entrancePairList[i][1][0:2] == entrancePairList[i2][1][0:2]): 
                            entrancePairList.pop(i2)
                            listSize = len(entrancePairList)
                if i2 == listSize - 1:
                    break
            if i == listSize - 1:
                return entrancePairList
        return entrancePairList

