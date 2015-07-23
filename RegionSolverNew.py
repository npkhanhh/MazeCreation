"""
Created on Jul 11, 2015

@author: ldhuy
"""
import threading

class RegionSolverNew(threading.Thread):
    """
    Run as a single thread, solve one specified region.
    This thread will find
        + all the paths that connect neighbor regions and save it to the parameter 'pathMap'
        + all the deadendsin this regions save it to the parameter 'deMap'
    """

    def __init__(self, grid, boundary, xRegionMap, yRegionMap, pathMap, deMap, regionMapLock):
        threading.Thread.__init__(self)
        self.grid = grid
        self.boundary = boundary
        self.xRegionMap = xRegionMap
        self.yRegionMap = yRegionMap
        self.pathMap = pathMap
        self.deMap = deMap
        self.regionMapLock = regionMapLock
        self.pathList = []
        self.deList = []
        
        
        
    def run(self):
        self.pathList = self.sovleRegion(self.grid, self.boundary)
        # Acquire lock
        if self.regionMapLock.acquire() == 1:
            self.pathMap[self.xRegionMap][self.yRegionMap] = self.pathList
            self.regionMapLock.release()
            
        self.FindDeadends(self.grid, self.boundary)
        if self.regionMapLock.acquire() == 1:
            self.deMap[self.xRegionMap][self.yRegionMap] = self.deList
            self.regionMapLock.release()
    
    def hasEntrance(self, grid, boundary, cell, directions):
        """
        Check if this cell has entrance
        A cell has entrance only if it lies at the boundary and has a missing border
        Params:
            grid: the whole maze
            boundary: the boundary of the current region
            cell: coordinate of the current cell
            directions: a list to store the directions of the entrance wrt this cell, this can be use as an additional result
                            (a cell can have more than one entrance if it is at the corner of the region
        Return: True if the cell has entrance, False if not
        """
        top, bottom, left, right = boundary
        row, col = cell
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
        if self.hasEntrance(grid, [top, bottom, left, right], [row, col], entranceAt):
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
    
    
    
    
    
    def sovleRegion(self, grid, boundary):
        """
        Find pairs of connected entrances of the regions
        Params:
            grid: the matrix represent the whole maze
            boundary: the boundary of this region [top, bottom, left, right] (the 'right' column and 'bottom' row are exclusive)
        Return: list of paths that connect neighbor regions
        """
        top, bottom, left, right = boundary
        entrancePairList = []   # List of paths that connect neighbor regions
        for c in  range(left, right):
            for r in range(top, bottom):
                if (c == left or c == right - 1) or (r == top or r == bottom - 1):    # Only examine cells at the boundary
                    entranceAt = []    # list of entrance of this cell
                    if self.hasEntrance(grid, [top, bottom, left, right], [r, c], entranceAt):
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
#         i1 = 0
#         while i1 < len(entrancePairList):#for i1 in range1:
#             i2 = 0
#             while i2 < len(entrancePairList):#for i2 in range1:
#                 if i2 != i1:
#                     reversedList = list(reversed(entrancePairList[i2]))
#                     if reversedList == entrancePairList[i1]:
#                         entrancePairList.pop(i2)
#                 if i2 == len(entrancePairList) - 1:
#                     break
#                 i2 += 1
#             if i1 == len(entrancePairList) - 1:
#                 break
#             i1 += 1
        i = 0
        length = len(entrancePairList)
        while i < length:
            j = i + 1
            while j < length:
                if entrancePairList[i] == entrancePairList[j]:
                    entrancePairList.pop(j)
                    length = len(entrancePairList)
                else:
                    reversedList = list(reversed(entrancePairList[j]))
                    if reversedList == entrancePairList[i]:
                        entrancePairList.pop(j)
                        length = len(entrancePairList)
                    else:
                        j += 1
            i += 1
        return entrancePairList


    def FindDeadends(self, grid, boundary):
        """
        Find the deadends in this region
        Param:
            grid: the maze
            boundary: the boundary of this region [top, bottom, left, right]
        Return: The list of deadends
        """
        top, bottom, left, right = boundary
        
        # Find deadends start from path
        for path in self.pathList:
            for cell in path:
                x, y = cell
                nextCell = [x-1, y]
                if self.grid[x][y].top == 0 and nextCell not in path and x-1 >= top and not self.isInPath(nextCell):
                    deadends = self.traverseDeadend(nextCell, [], 'top', boundary)
                    self.deList = self.deList + deadends
                nextCell = [x+1, y]
                if self.grid[x][y].bottom == 0 and nextCell not in path and x+1 <bottom and not self.isInPath(nextCell):
                    deadends = self.traverseDeadend(nextCell, [], 'bottom', boundary)
                    self.deList = self.deList + deadends
                nextCell = [x, y-1]
                if self.grid[x][y].left == 0 and nextCell not in path and y-1 >= left and not self.isInPath(nextCell):
                    deadends = self.traverseDeadend(nextCell, [], 'left', boundary)
                    self.deList = self.deList + deadends
                nextCell = [x, y+1]
                if self.grid[x][y].right == 0 and nextCell not in path and y+1 < right and not self.isInPath(nextCell):
                    deadends = self.traverseDeadend(nextCell, [], 'right', boundary)
                    self.deList = self.deList + deadends
                    
        # Find deadends start from entrance
        for c in range(left, right):
            for r in range(top, bottom):
                entranceAt = []
                if self.hasEntrance(self.grid, boundary, [r, c], entranceAt) and not self.isInPath([r, c]):
                    temp = self.grid[r][c]
                    if self.isDeadend([r, c]):
                        self.deList.append([[r, c]])
                    else:
                        if temp.top == 0 and 'top' not in entranceAt and r-1 >= top:
                            nextCell = [r-1, c]
                            p = [[r, c]]
                            deadends = self.traverseDeadend(nextCell, p, 'top', boundary)
                            self.deList = self.deList + deadends
                        if temp.bottom == 0 and 'bottom' not in entranceAt and r+1 < bottom:
                            nextCell = [r+1, c]
                            p = [[r, c]]
                            deadends = self.traverseDeadend(nextCell, p, 'bottom', boundary)
                            self.deList = self.deList + deadends
                        if temp.left == 0 and 'left' not in entranceAt and c-1 >= left:
                            nextCell = [r, c-1]
                            p = [[r, c]]
                            deadends = self.traverseDeadend(nextCell, p, 'left', boundary)
                            self.deList = self.deList + deadends
                        if temp.right == 0 and 'right' not in entranceAt and c+1 < right:
                            nextCell = [r, c+1]
                            p = [[r, c]]
                            deadends = self.traverseDeadend(nextCell, p, 'right', boundary)
                            self.deList = self.deList + deadends
                        
        # Remove duplicate deadends
        length = len(self.deList)
        i = 0
        j = i + 1
        while i < length:
            while j < length:
                if self.deList[i] == self.deList[j]:
                    self.deList.remove(self.deList[j])
                    length = len(self.deList)
                else:
                    j += 1
            i += 1
            j = i + 1
        
            
                    
    def traverseDeadend(self, cell, path, direction, boundary):
        """
        Params:
            cell: the coordinate of the current cell
            path: the traversed deadend
            direction: the direction of the current cell wrt the previous one
            boundary: the boundary of the current region
        """
        top, bottom, left, right = boundary
        deList = []
        if self.isDeadend(cell):
            path.append(cell)
            deList.append(path)
        else:
            temp = self.grid[cell[0]][cell[1]]
            x, y = cell
            nextCell = [x-1, y]
            if temp.top == 0 and direction != 'bottom' and x-1 >= 0:
                newPath = list(path)
                newPath.append(cell)
                result = self.traverseDeadend(nextCell, newPath, 'top', boundary)
                deList = deList + result
            nextCell = [x+1, y]
            if temp.bottom == 0 and direction != 'top' and x+1 < bottom:
                newPath = list(path)
                newPath.append(cell)
                result = self.traverseDeadend(nextCell, newPath, 'bottom', boundary)
                deList = deList + result
            nextCell = [x, y-1]
            if temp.left == 0 and direction != 'right' and y-1 >= 0:
                newPath = list(path)
                newPath.append(cell)
                result = self.traverseDeadend(nextCell, newPath, 'left', boundary)
                deList = deList + result
            nextCell = [x, y+1]
            if temp.right == 0 and direction != 'left' and y+1 < right:
                newPath = list(path)
                newPath.append(cell)
                result = self.traverseDeadend(nextCell, newPath, 'right', boundary)
                deList = deList + result
        
        return deList
    
    
    def isDeadend(self, cell):
        temp = self.grid[cell[0]][cell[1]]
        if temp.top + temp.right + temp.bottom + temp.left == 3:
            return True
        else:
            return False 
        
    def isInPath(self, cell):
        """
        Check if the cell is in any path of the current region
        Params:
            cell: the coordinate of the cell
        """
        for p in self.pathList:
            if cell in p:
                return True
        
        return False
    
        