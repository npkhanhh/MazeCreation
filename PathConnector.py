'''
Created on Jun 4, 2015

@author: ldhuy
'''
import threading
import sys



class PathConnector(threading.Thread):
    """
    Receive the discovered paths and find shortest path that connect 2 specific cells
    """


    def __init__(self, grid, startCell, goalCell, pathMap, xRegion, yRegion, nRegion, mazeSize):
        """
        Params:
            grid: the maze
            startCell: the coordinate of the cell this robot starts at [x, y]
            goalCell: the coordinate of the cell this robot needs to find path that leads to [x, y]
            xRegion, yRegion: the starting cell belong to a region, this region has the coordinate [xRegion, yRegion] in the region map
            pathMap: the map of regions discovered by RegionSolver(s)
            nRegion: the program divides the maze into nRgion*nRegion regions to run RegionSolver(s)
        """
        threading.Thread.__init__(self)
        self.grid = grid
        self.startCell = startCell
        self.goalCell = goalCell
        self.xRegion = xRegion
        self.yRegion = yRegion
        self.regionMap = pathMap
        self.nRegion = nRegion
        self.mazeSize = mazeSize
        
        
    def run(self):
        threading.Thread.run(self)
        shortestPath = self.findShortestPath(self.startCell, self.goalCell, self.xRegion, self.yRegion, [], '', [-1, -1])
        print "Shortest path: "
        print shortestPath
        
    def findShortestPath(self, startingCell, endingCell, xRegion, yRegion, path, direction, entrance):
        """
        Find the shortest path that lead to the ending cell
        Params:
            startingCell: the cell from which the path starts at
            endingCell: the destination cell (self.goalCell)
            xRegion, yRegion: the coordinate of the current region in the region map
            path: the path, up to now
            direction: the direction of the current region wrt the previous region. It's used to avoid traveling the old region
            entrance: the entrance cell from which this method starts to explore the current region
        Return:
            The shortest path that leads to the ending cell
            [] if no path was found
        """
        shortestPath = []
        pathsInRegion = self.regionMap[xRegion][yRegion]
        
        # Check if the ending cell is in this region
        regionSize = self.mazeSize / self.nRegion
        x = endingCell[0]/regionSize    # [x, y] is the coordinate of the region that goalCell belongs to
        y = endingCell[1]/regionSize
        
        
        #### NEW APPROACH ####
        startCellInPath = False
        for p1 in pathsInRegion:
            if startingCell in p1:
                startCellInPath = True
                if x == xRegion and y == yRegion: # endingCell in the same region with startingCell
                    endCellInPath = False
                    for p2 in pathsInRegion:
                        if endingCell in p2:
                            endCellInPath = True
                            if p1 == p2: # startingCell and endingCell are in the same path
                                idx1 = -1
                                idx2 = -1
                                try:
                                    idx1 = p1.index(startingCell)
                                    idx2 = p1.index(endingCell)
                                except ValueError:
                                    pass
                                if idx1 <= idx2:
                                    shortestPath = p1[idx1:idx2+1]
                                else:
                                    shortestPath = list(reversed(p1[idx2:idx1+1]))
                                path = path + shortestPath
                                return path
                            else:   # endCell in another path
                                connectedPath = self.getConnectedPath(p1, p2, startingCell, endingCell)
                                if len(connectedPath) > 0:  # 2 paths intersect each other and the connected path was found
                                    path = path + connectedPath
                                    return path
                                else:   # couldn't find the connected path (2 paths don't intersect each other) => endingCell is in an isolated area
                                    break
                    if not endCellInPath: 
                        foundPath = self.findGoalInDeadend(p1, startingCell, endingCell, xRegion, yRegion, direction) 
                        if len(foundPath)>0:
                            path = path + foundPath
                            return path
                else: # endingCell is not in same region with startingCell
                    idx = -1
                    try:
                        idx = p1.index(startingCell)
                    except:
                        pass
                    if idx != -1:
                        subPath1 = p1[0:idx+1]
                        subPath1 = list(reversed(subPath1))
                        subPath2 = p1[idx:]
                        subPaths = [subPath1, subPath2]
                        for subPath in subPaths:    # move to 2 ends of the path to explore new region
                            end = subPath[-1]
                            dirList = self.cellIsAt(end, xRegion, yRegion)
                            foundPath = []
                            for d in dirList:
                                newPath = list(path)
                                newPath = newPath + subPath
                                if d == 'top' and self.grid[end[0]][end[1]].top==0 and xRegion-1>=0:
                                    nextCell = [end[0]-1, end[1]]
                                    if end != entrance:
                                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion-1, yRegion, newPath, d, nextCell)
                                elif d == 'bottom' and self.grid[end[0]][end[1]].bottom==0 and xRegion+1<self.nRegion:
                                    nextCell = [end[0]+1, end[1]]
                                    if end != entrance:
                                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion+1, yRegion, newPath, d, nextCell)
                                elif d == 'left' and self.grid[end[0]][end[1]].left==0 and yRegion-1>=0:
                                    nextCell = [end[0], end[1]-1]
                                    if end != entrance:
                                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion, yRegion-1, newPath, d, nextCell)
                                elif d == 'right' and self.grid[end[0]][end[1]].right==0 and yRegion+1<self.nRegion:
                                    nextCell = [end[0], end[1]+1]
                                    if end != entrance:
                                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion, yRegion+1, newPath, d, nextCell)
                                if len(foundPath)>0:
                                    return foundPath
        if not startCellInPath: # starting cell is in a deadend
            # Look for endingCell if it's in the deadend
            boundary = self.getBoundary(xRegion, yRegion)
            foundPath = self.gotoNearestPath(path, pathsInRegion, startingCell, endingCell, xRegion, yRegion, boundary, '')
            #foundPath = self.gotoDeadend(startingCell, endingCell, direction, path)
            if len(foundPath) > 0:
                return foundPath
            else:
                return []
        return []            

    
    def getConnectedPath(self, p1, p2, startingCell, endingCell):
        """
        Find the path connects startingCell and endingCell when these cells lie on 2 paths that intersect
        Params:
            p1, p2: 1st and 2nd path
            startingCell: starting cell, lies on p1
            endingCell: ending cell, lies on p2
        Return: a path from startingCell to endingCell
        """
        path = []
        if startingCell in p2:
            path = p2
        elif endingCell in p1:
            path = p1
            
        if len(path) > 0:   # startingCell and endingCell are in the same path
            idx1 = -1
            idx2 = -1
            try:
                idx1 = path.index(startingCell)
                idx2 = path.index(endingCell)
            except:
                pass
            
            result = []
            if idx2 < idx1:
                path = list(reversed(path))
                try:
                    idx1 = path.index(startingCell)
                    idx2 = path.index(endingCell)
                except:
                    pass
                
            result = path[idx1:idx2+1]
            return result
            
        else:   # startingCell and endingCell are in different paths
            if p1[0] == p2[0]:
                pass
            elif p1[0] == p2[-1]:
                p2 = list(reversed(p2))
            elif p1[-1] == p2[-1]:
                p1 = list(reversed(p1))
                p2 = list(reversed(p2))
            elif p1[-1] == p2[0]:
                p1 = list(reversed(p1))
            else:
                return []
                    
            idx1 = -1
            idx2 = -1
            try:
                idx1 = p1.index(startingCell)
                idx2 = p2.index(endingCell)
            except ValueError:
                pass
            
            i = 0
            lastCommonCell = []
            while i<idx1 and i<idx2:
                if p1[0] == p2[0]:
                    lastCommonCell = p1.pop(0)
                    p2.pop(0)
                else:
                    pass
                i = i + 1
            
            p1 = list(reversed(p1))
            p1.append(lastCommonCell)
            try:
                idx1 = p1.index(startingCell)
                idx2 = p2.index(endingCell)
            except:
                pass
            
            result = p1[idx1:]
            result = result + p2[0:idx2+1]
            return result
    
    def findGoalInDeadend(self, path, startingCell, endingCell, xRegion, yRegion, direction):
        """
        Find the deadend where endingCell lies on and return the path from startingCell to endingCell
        Note: the starting cell is in a path
        Params:
            path: the path where startingCell lies on
            startingCell, endingCell: start and goal
            xRegion, yRegion: the coordinate of the current region
            direction: the direction of the current region wrt the previous region. It's used to avoid traveling the old region
        Return:
            the path from startingCell to endingCell
            if could not find, which means endingCell is isolated, return []
        """
        idx = -1
        try:
            idx = path.index(startingCell)
        except:
            pass
        result = []
        
        if idx != -1:
            p1 = list(path[0:idx+1])
            p1 = list(reversed(p1))
            p2 = list(path[idx:])
            subpaths = [p1, p2]
            top, left, bottom, right = self.getBoundary(xRegion, yRegion)
            
            for subpath in subpaths:
                for i in range(len(subpath)):
                    cell = [subpath[i][0], subpath[i][1]]
                    nextCell = [cell[0]-1, cell[1]]
                    if self.grid[cell[0]][cell[1]].top == 0 and nextCell[0]>=top and not self.isInPaths(nextCell, xRegion, yRegion):
                        foundPath = self.gotoDeadend(nextCell, endingCell, 'top', [])
                        if len(foundPath) > 0:
                            result = subpath[0:i+1]
                            result = result + foundPath
                            return result
                    nextCell = [cell[0]+1, cell[1]]
                    if self.grid[cell[0]][cell[1]].bottom == 0 and nextCell[0]<bottom and not self.isInPaths(nextCell, xRegion, yRegion):
                        foundPath = self.gotoDeadend(nextCell, endingCell, 'bottom', [])
                        if len(foundPath) > 0:
                            result = subpath[0:i+1]
                            result = result + foundPath
                            return result
                    nextCell = [cell[0], cell[1]-1]
                    if self.grid[cell[0]][cell[1]].left == 0 and nextCell[1]>=left and not self.isInPaths(nextCell, xRegion, yRegion):
                        foundPath = self.gotoDeadend(nextCell, endingCell, 'left', [])
                        if len(foundPath) > 0:
                            result = subpath[0:i+1]
                            result = result + foundPath
                            return result
                    nextCell = [cell[0], cell[1]+1]
                    if self.grid[cell[0]][cell[1]].right == 0 and nextCell[1]<right and not self.isInPaths(nextCell, xRegion, yRegion):
                        foundPath = self.gotoDeadend(nextCell, endingCell, 'right', [])
                        if len(foundPath) > 0:
                            result = subpath[0:i+1]
                            result = result + foundPath
                            return result
                        
            # If no path was found, then ending cell is in the isolated area of this region
            # We have to go to other regions to approach that area
            for subpath in subpaths:    # iterate each entrance to explore neighbor regions to approach the isolated area of this region
                end = subpath[-1]
                dirList = self.cellIsAt(end, xRegion, yRegion)
                for d in dirList:
                    if d == 'top' and self.grid[end[0]][end[1]].top == 0 and direction != 'bottom' and xRegion-1 >= 0:
                        nextCell = [end[0]-1, end[1]]
                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion-1, yRegion, [], 'top', nextCell)
                        if len(foundPath) > 0:
                            result = subpath + foundPath
                            return result
                    if d == 'bottom' and self.grid[end[0]][end[1]].bottom == 0 and direction != 'top' and xRegion+1 < self.nRegion:
                        nextCell = [end[0]+1, end[1]]
                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion+1, yRegion, [], 'bottom', nextCell)
                        if len(foundPath) > 0:
                            result = subpath + foundPath
                            return result
                    if d == 'left' and self.grid[end[0]][end[1]].left == 0 and direction != 'right' and yRegion-1 >= 0:
                        nextCell = [end[0], end[1]-1]
                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion, yRegion-1, [], 'left', nextCell)
                        if len(foundPath) > 0:
                            result = subpath + foundPath
                            return result
                    if d == 'right' and self.grid[end[0]][end[1]].right == 0 and direction != 'left' and yRegion+1 < self.nRegion:
                        nextCell = [end[0], end[1]+1]
                        foundPath = self.findShortestPath(nextCell, endingCell, xRegion, yRegion+1, [], 'right', nextCell)
                        if len(foundPath) > 0:
                            result = subpath + foundPath
                            return result
                
            return []    
                      
    def gotoDeadend(self, cell, endingCell, direction, path):
        """
        Find the way to endingCell when endingCell is in a deadend
        Params:
            cell: current cell
            endingCell: ending cell
            direction: the direction of the current cell wrt the previous cell
            path: the path from the beginning of the deadend to the current cell
        Return:
            the path from the beginning of the deadend to the ending cell
        """
        if cell == endingCell:
            path.append(cell)
            return path
        else:
            if direction != 'bottom' and self.grid[cell[0]][cell[1]].top == 0:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoDeadend([cell[0]-1, cell[1]], endingCell, 'top', newPath)
                if len(foundPath) > 0:
                    return foundPath
            if direction != 'top' and self.grid[cell[0]][cell[1]].bottom == 0:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoDeadend([cell[0]+1, cell[1]], endingCell, 'bottom', newPath)
                if len(foundPath) > 0:
                    return foundPath
            if direction != 'left' and self.grid[cell[0]][cell[1]].right == 0:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoDeadend([cell[0], cell[1]+1], endingCell, 'right', newPath)
                if len(foundPath) > 0:
                    return foundPath
            if direction != 'right' and self.grid[cell[0]][cell[1]].left == 0:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoDeadend([cell[0], cell[1]-1], endingCell, 'left', newPath)
                if len(foundPath) > 0:
                    return foundPath
            return []
    
    def isInPaths(self, cell, xRegion, yRegion):
        """
        Check if the cell is in any path of the current region
        Params:
            cell: the coordinate of the cell
            xRegion, yRegion: the coordinate of the current region
        Return:
            True if the cell is in any path in the region
        """
        for p in self.regionMap[xRegion][yRegion]:
            if cell in p:
                return True
        return False
    
    def getBoundary(self, xRegion, yRegion):
        """
        Get the boundary limit (top, left, bottom, right) of the given region
        Params:
            xRegion, yRegion: the coordinate of the region in region map
        Return:
            an array: [top, left, bottom, right]
        """
        regionSize = self.mazeSize / self.nRegion
        top = regionSize * xRegion
        left = regionSize * yRegion
        right = left + regionSize
        bottom = top + regionSize
        result = [top, left, bottom, right]
        return result
                    
        
    def findPathDeadend(self, grid, top, left, right, bottom, row, col, direction, length, path):
        """
        Params:
            grid: the whole maze
            row, col: coordinate of the current cell
            direction: the direction of the current cell with respect to the previous cell
            length: the length of the path from the cell that calls this method up to the current cell (starting cell and ending cell included)
            path: an array of string stores that path ([row1, col1], [row2, col2], ...)
        Return: list of paths that lead to dead-end(s). Format: [path1, path2, ...]
        """
        pathList = []       # pathList is a list stores coordinates of cells in paths that connects neighbor regions
                                    # [[row1, col1], [row2, col2], ...]
        # Check if this cell is a deadend
        if self.isDeadend(grid, row, col, direction):
            path.append([row, col])
            pathList = pathList + path
        
        
        if direction != 'right' and col > left and grid[row][col].left == 0:    # check left cell
            pathNew = list(path)
            pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col - 1, 'left', length + 1, pathNew)
            pathList = pathList + entranceCells
        if direction != 'top' and row < bottom - 1 and grid[row][col].bottom == 0:    # check bottom cell
            pathNew = list(path)
            pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row + 1, col, 'bottom', length + 1, pathNew)
            pathList = pathList + entranceCells
        if direction != 'left' and col < right - 1 and grid[row][col].right == 0:    # check right cell
            pathNew = list(path)
            pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row, col + 1, 'right', length + 1, pathNew)
            pathList = pathList + entranceCells
        if direction != 'bottom' and row > top and grid[row][col].top == 0:    # check top cell
            pathNew = list(path)
            pathNew.append([row, col])
            entranceCells = self.findPath(grid, top, left, right, bottom, row - 1, col, 'top', length + 1, pathNew)
            pathList = pathList + entranceCells
            
        return pathList
                    
    def isDeadend(self, grid, row, col, direction):
        """
        Check if this cell is a deadend
        Params:
            grid: the whole maze
            row, col: coordinate of this cell
            direction: the direction of this cell to the previous cell
        Return: True if this is a deadend, False if not
        """ 
        result = False               
        if  direction == 'top' and grid[row][col].top == 1 and \
            grid[row][col].right == 1 and grid[row][col].left == 1:
            result = True
        elif direction == 'bottom' and grid[row][col].bottom == 1 and \
            grid[row][col].right == 1 and grid[row][col].left == 1:
            result = True
        elif direction == 'right' and grid[row][col].bottom == 1 and \
            grid[row][col].right == 1 and grid[row][col].top == 1:
            result = True
        elif direction == 'left' and grid[row][col].bottom == 1 and \
            grid[row][col].top == 1 and grid[row][col].left == 1:
            result = True
        
        return result

                    
    def cellIsAt(self, cell, xRegion, yRegion):
        """
        Find which boundary of the region this cell is at
        Params:
            cell: the current cell
            xRegion, yRegion: the coordinate of the considered region in the region map
        Return: 
            The direction which the cell is at wrt the current region. For example: ['right'] or ['left']
            The array contains 2 directions when the cell is at the corner of the region
        """
        directions = []
        regionSize = self.mazeSize / self.nRegion
        top = xRegion * regionSize
        left = yRegion * regionSize
        if cell[0] == top:
            directions.append('top')
        if cell[1] == left:
            directions.append('left')
        if cell[0] == top + regionSize - 1:
            directions.append('bottom')
        if cell[1] == left + regionSize - 1:
            directions.append('right')
        
        return directions

    def gotoNearestPath(self, path, pathList, cell, destination, xRegion, yRegion, boundary, direction):
        """
        When starting cell is in a deadend, this method goes a long that deadend to find the nearest path, then call the self.findShortestPath method
        If can't reach any path in this region from the starting cell, go to neighbor region and explore
        Params:
            path: the traversed path up to this cell
            pathList: list of all path in the current region
            cell: the coordinate of the current cell
            destination: [x, y] the destination cell
            xRegion, yRegion: coordinate of the current region in region map
            boundary: the boundary of the current region  ([top, left, bottom, right])
            direction: the direction of the current cell wrt the previous cell
        """
        r, c = cell
        top, left, bottom, right = boundary
        
        if r == destination[0] and c == destination[1]:
            path.append(cell)
            return path
        elif self.isInPaths(cell, xRegion, yRegion):
            foundPath = self.findShortestPath(cell, destination, xRegion, yRegion, path, '', [-1, -1])
            if len(foundPath) > 0:
                return foundPath
            else:
                return []
        
        entranceCells = []   # if encounter entrance cell, store it and explore or direction then come back exploring neighbor regions later (BFS) 
        if self.grid[r][c].top == 0 and [r-1, c] not in path and direction != 'bottom':
            if r-1 >= top:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoNearestPath(newPath, pathList, [r-1, c], destination, xRegion, yRegion, boundary, 'top')
                if len(foundPath) > 0:
                    return foundPath
            elif r-1 >= 0: # There's neighbor region
                entranceCells.append(cell) # save this entrance cell and explore later
        if self.grid[r][c].bottom == 0 and [r+1, c] not in path and direction != 'top':
            if r+1 < bottom:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoNearestPath(newPath, pathList, [r+1, c], destination, xRegion, yRegion, boundary, 'bottom')
                if len(foundPath) > 0:
                    return foundPath
            elif r+1 < self.mazeSize-1: # There's neighbor region
                entranceCells.append(cell) # save this entrance cell and explore later
        if self.grid[r][c].left == 0 and [r, c-1] not in path and direction != 'right':
            if c-1 >= left:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoNearestPath(newPath, pathList, [r, c-1], destination, xRegion, yRegion, boundary, 'left')
                if len(foundPath) > 0:
                    return foundPath
            elif c-1 >= 0: # There's neighbor region
                entranceCells.append(cell) # save this entrance cell and explore later
        if self.grid[r][c].right == 0 and [r, c+1] not in path and direction != 'left':
            if c+1 < right:
                newPath = list(path)
                newPath.append(cell)
                foundPath = self.gotoNearestPath(newPath, pathList, [r, c+1], destination, xRegion, yRegion, boundary, 'right')
                if len(foundPath) > 0:
                    return foundPath
            elif c+1 < self.mazeSize-1: # There's neighbor region
                entranceCells.append(cell) # save this entrance cell and explore later
        
        # Explore the next regions
        for entrance in entranceCells:
            dirList = self.cellIsAt(entrance, xRegion, yRegion)
            for d in dirList:
                if self.grid[entrance[0]][entrance[1]].top == 0 and d=='top' and entrance not in path:
                    newPath = list(path)
                    newPath.append(entrance)
                    nextCell = [entrance[0]-1, entrance[1]]
                    foundPath = self.findShortestPath(nextCell, destination, xRegion-1, yRegion, newPath, 'top', nextCell)
                    if len(foundPath) > 0:
                        return foundPath
                if self.grid[entrance[0]][entrance[1]].bottom == 0 and d=='bottom' and entrance not in path:
                    newPath = list(path)
                    newPath.append(entrance)
                    nextCell = [entrance[0]+1, entrance[1]]
                    foundPath = self.findShortestPath(nextCell, destination, xRegion+1, yRegion, newPath, 'bottom', nextCell)
                    if len(foundPath) > 0:
                        return foundPath
                if self.grid[entrance[0]][entrance[1]].left == 0 and d=='left' and entrance not in path:
                    newPath = list(path)
                    newPath.append(entrance)
                    nextCell = [entrance[0], entrance[1]-1]
                    foundPath = self.findShortestPath(nextCell, destination, xRegion, yRegion-1, newPath, 'left', nextCell)
                    if len(foundPath) > 0:
                        return foundPath
                if self.grid[entrance[0]][entrance[1]].right == 0 and d=='right' and entrance not in path:
                    newPath = list(path)
                    newPath.append(entrance)
                    nextCell = [entrance[0], entrance[1]+1]
                    foundPath = self.findShortestPath(nextCell, destination, xRegion, yRegion+1, newPath, 'right', nextCell)
                    if len(foundPath) > 0:
                        return foundPath
                
        return []
    