'''
Created on Jul 15, 2015

@author: ldhuy
'''
import threading

class PathConnectorNew(threading.Thread):
    '''
    Receive the discovered paths and deadends and find shortest path that connect 2 specific cells
    '''


    def __init__(self, grid, startCell, goalCell, pathMap, deMap, nRegion, mazeSize, solution):
        '''
        Params:
            grid: the maze
            startCell: the coordinate of the cell this robot starts at [x, y]
            goalCell: the coordinate of the cell this robot needs to find path that leads to [x, y]
            pathMap: the map of regions discovered by RegionSolver(s)
            deMap: the 2D array stores deadends in each region
            nRegion: the program divides the maze into nRgion*nRegion regions to run RegionSolver(s)
            mazeSize: the number of cells at each side of the maze
            solution: the found solution
        '''
        threading.Thread.__init__(self)
        self.grid = grid
        self.startCell = startCell
        self.goalCell = goalCell
        
        self.pathMap = pathMap
        self.deMap = deMap
        self.nRegion = nRegion
        self.mazeSize = mazeSize
        
        self.regionSize = mazeSize / nRegion
        
        # xRegStart, yRegStart: the starting cell belong to a region, this region has the coordinate [xRegStart, yRegStart] in the region map
        self.xRegStart = startCell[0]/self.regionSize
        self.yRegStart = startCell[1]/self.regionSize
        # xRegGoal, yRegGoal: the ending cell belong to a region, this region has the coordinate [xRegGoal, yRegGoal] in the region map
        self.xRegGoal = self.goalCell[0]/self.regionSize
        self.yRegGoal = self.goalCell[1]/self.regionSize
        
        self.traversedPaths = []
        self.traversedDes = []
        self.solution = solution
        
    def run(self):
        threading.Thread.run(self)
        # Find the path that starting cell belongs to
        xRegion = self.startCell[0]/self.regionSize
        yRegion = self.startCell[1]/self.regionSize
        solutionNodes = []
        
        top, left, bottom, right = self.getBoundary(xRegion, yRegion)
        # Find the deadend that starting cell belongs to
        for i in range(len(self.deMap[xRegion][yRegion])):
            de = self.deMap[xRegion][yRegion][i]
            if self.startCell in de:
                if self.goalCell in de:
                    self.solution = [de]
                    # TODO: extract the subpath
                else:
                    traversedDEs = []
                    traversedDEs.append([xRegion, yRegion, i])
                    solutionNodes.append(de)
                    end = de[0]    # deadends have only one opened end
                    pathsInRegion = self.pathMap[xRegion][yRegion]
                    for j in range(len(pathsInRegion)):
                        p = pathsInRegion[j]
                        if self.isConnected(de, p, []): # this means the starting cell is in a deadend whose opened end is inside the current region
                            foundSolution = self.findShortestSolution([end], self.goalCell, [xRegion, yRegion], solutionNodes, [], traversedDEs)
                            if len(foundSolution) > 0:
                                self.solution = foundSolution
                                print self.solution
                                return
                        else:
                            directions = self.cellIsAt(end, xRegion, yRegion)
                            for d in directions:
                                nextRegionCoordinate = [-1, -1]
                                if  d == "top" and xRegion-1 >= 0:
                                    nextRegionCoordinate = [xRegion-1, yRegion]
                                elif d == 'bottom' and xRegion+1 < self.nRegion:
                                    nextRegionCoordinate = [xRegion+1, yRegion]
                                elif d == 'left' and yRegion-1 >= 0:
                                    nextRegionCoordinate = [xRegion, yRegion-1]
                                elif d == 'right' and yRegion+1 < self.nRegion:
                                    nextRegionCoordinate = [xRegion, yRegion+1]
                                foundSolution = self.findShortestSolution([end], self.goalCell, nextRegionCoordinate, solutionNodes, [], traversedDEs)
                                if len(foundSolution) > 0:
                                    self.solution = foundSolution
                                    print self.solution
                                    return
                            
        for i in range(len(self.pathMap[xRegion][yRegion])):
            p = self.pathMap[xRegion][yRegion][i]
            if self.startCell in p:
                if self.goalCell in p:
                    self.solution = [p]
                    # TODO: extract the subpath
                else:
                    traversedPaths = []
                    traversedPaths.append([xRegion, yRegion, i])
                    solutionNodes.append(p)
                    ends = [p[0], p[-1]]
                    for end in ends:
                        directions = self.cellIsAt(end, xRegion, yRegion)
                        for d in directions:
                            nextRegionCoordinate = [-1, -1]
                            if  d == "top" and xRegion-1 >= 0:
                                nextRegionCoordinate = [xRegion-1, yRegion]
                            elif d == 'bottom' and xRegion+1 < self.nRegion:
                                nextRegionCoordinate = [xRegion+1, yRegion]
                            elif d == 'left' and yRegion-1 >= 0:
                                nextRegionCoordinate = [xRegion, yRegion-1]
                            elif d == 'right' and yRegion+1 < self.nRegion:
                                nextRegionCoordinate = [xRegion, yRegion+1]
                            foundSolution = self.findShortestSolution([end], self.goalCell, nextRegionCoordinate, solutionNodes, traversedPaths, [])
                            if len(foundSolution) > 0:
                                self.solution = foundSolution
                                print self.solution
                                return
        
        
                        


    def findShortestSolution(self, previousNode, goal, regionCoor, solutionNodes, traversedPaths, traversedDEs):
        """
        Find the shortest path that lead to the ending cell
        Params:
            previousNode: the path/deadend at the previous region
            goal: the ending cell
            regionCoor: the coordinate of the current region in the region map
            path: the traversed path
            solutionNodes: the list that contain all the traversed paths/deadend
            traversedPaths: list of coordinates of traversed paths [xRegion, yRegion, index of path in self.pathMap[xRegion][yRegion]]
            traversedDEs: list of coordinates of traversed deadends [xRegion, yRegion, index of deadend in self.deMap[xRegion][yRegion]]
#             explorePaths: the list of explored paths
#             exploredDEs: the list of explored deadends
        Return:
            A list of paths/deadend that make up the solution
        """
        if regionCoor == [-1, -1]:
            return []
        xRegion, yRegion = regionCoor
        
        deInRegion = self.deMap[xRegion][yRegion]
        pathsInRegion = self.pathMap[xRegion][yRegion]
        for i in range(len(deInRegion)):
            de = deInRegion[i]
            if goal in de:
#                 if [xRegion, yRegion, i] not in self.traversedDes and self.isConnected(previousNode, de):
                if [xRegion, yRegion, i] not in self.traversedDes and self.hasEntrance(self.grid, regionCoor, de[0], []):
                    if self.isConnected(previousNode, de, []):
                        newTraversedDes = list(traversedDEs)
                        newTraversedDes.append([xRegion, yRegion, i])
                        newSolutionNodes = list(solutionNodes)
                        newSolutionNodes.append(de)
                        return newSolutionNodes
#                 elif [xRegion, yRegion, i] not in self.traversedDes and not self.isConnected(previousNode, de):
                elif [xRegion, yRegion, i] not in self.traversedDes and not self.hasEntrance(self.grid, regionCoor, de[0], []):
                    # The goal is in a deadend whose opened end is not an entrance. 
                    # Thus we have to look through the list of paths to find the path that connects this deadend and the previous node
                    ends = [de[0]]
                    for j in range(len(pathsInRegion)):
                        p = pathsInRegion[j]
                        if [xRegion, yRegion, i] not in traversedPaths and self.isConnected(previousNode, p, []) and self.isConnected(ends, p, []):
                            solutionNodes.append(p)
                            solutionNodes.append(de)
                            return solutionNodes
                    
        for i in range(len(pathsInRegion)):
            p = pathsInRegion[i]
            atCell = [-1, -1]
            if [xRegion, yRegion, i] not in traversedPaths and self.isConnected(previousNode, p, atCell):
                newTraversedPaths = list(traversedPaths)
                newTraversedPaths.append([xRegion, yRegion, i])
                newSolutionNodes = list(solutionNodes)
                newSolutionNodes.append(p)
                if goal in p:
                    return newSolutionNodes
                else:
                    # Check neighbor regions at both ends of this path
                    ends = [p[0], p[-1]]
                    for end in ends:
                        if len(p) > 1 and end == atCell:
                            continue
                        else:
                            directions = self.cellIsAt(end, xRegion, yRegion)
                            for d in directions:
                                nextRegionCoordinate = [-1, -1]
                                if  d == "top" and xRegion-1 >= 0:
                                    nextRegionCoordinate = [xRegion-1, yRegion]
                                elif d == 'bottom' and xRegion+1 < self.nRegion:
                                    nextRegionCoordinate = [xRegion+1, yRegion]
                                elif d == 'left' and yRegion-1 >= 0:
                                    nextRegionCoordinate = [xRegion, yRegion-1]
                                elif d == 'right' and yRegion+1 < self.nRegion:
                                    nextRegionCoordinate = [xRegion, yRegion+1]
                                foundSolution = self.findShortestSolution([end], goal, nextRegionCoordinate, newSolutionNodes, newTraversedPaths, traversedDEs)
                                if len(foundSolution) > 0:
                                    return foundSolution
        
        return []
        
    def isConnected(self, p1, p2, atCell):
        """
        Check if 2 paths are connected
        Params:
            p1, p2: 2 paths
            atCell: the cell in p2 where 2 paths connect
        """
        for i in range(len(p1)):
            c1 = p1[i]
            for j in range(len(p2)):
                c2 = p2[j]
                atCell[:] = c2[:]
                if c1 == c2:
                    return True
                if c1[0] == c2[0]:
                    if c1[1] == c2[1]-1:
                        if self.grid[c1[0]][c1[1]].right == 0 and self.grid[c2[0]][c2[1]].left == 0:
                            return True
                    elif c1[1] == c2[1]+1:
                        if self.grid[c1[0]][c1[1]].left == 0 and self.grid[c2[0]][c2[1]].right == 0:
                            return True
                elif c1[1] == c2[1]:
                    if c1[0] == c2[0]-1:
                        if self.grid[c1[0]][c1[1]].bottom == 0 and self.grid[c2[0]][c2[1]].top == 0:
                            return True
                    elif c1[0] == c2[0]+1:
                        if self.grid[c1[0]][c1[1]].top == 0 and self.grid[c2[0]][c2[1]].bottom == 0:
                            return True
        return False
    
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
        top, left, bottom, right = self.getBoundary(xRegion, yRegion)
        if cell[0] == top:
            directions.append('top')
        if cell[1] == left:
            directions.append('left')
        if cell[0] == top + self.regionSize - 1:
            directions.append('bottom')
        if cell[1] == left + self.regionSize - 1:
            directions.append('right')
        
        return directions
    
    def getBoundary(self, xRegion, yRegion):
        """
        Get the boundary limit (top, left, bottom, right) of the given region
        Params:
            xRegion, yRegion: the coordinate of the region in region map
        Return:
            an array: [top, left, bottom, right]
        """
        top = self.regionSize * xRegion
        left = self.regionSize * yRegion
        right = left + self.regionSize
        bottom = top + self.regionSize
        result = [top, left, bottom, right]
        return result
    
    def hasEntrance(self, grid, regionCoor, cell, directions):
        """
        Check if this cell has entrance
        A cell has entrance only if it lies at the boundary and has a missing border
        Params:
            grid: the whole maze
            regionCoor: the coordinate of the region
            cell: coordinate of the current cell
            directions: a list to store the directions of the entrance wrt this cell, this can be use as an additional result
                            (a cell can have more than one entrance if it is at the corner of the region
        Return: True if the cell has entrance, False if not
        """
        xRegion, yRegion = regionCoor
        top, left, bottom, right = self.getBoundary(xRegion, yRegion)
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