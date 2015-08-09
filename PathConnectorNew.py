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
        
        self.isGoalInDeadend = False
        self.doesGoalNodeHaveEntrance = True
        self.goalNode = []
        
    def run(self):
        threading.Thread.run(self)
        # Find the path that starting cell belongs to
        xRegion = self.startCell[0]/self.regionSize
        yRegion = self.startCell[1]/self.regionSize
        traversedNodes = []
        
        # Look for the deadend where goal lies in
        xRegGoal = self.goalCell[0]/self.regionSize
        yRegGoal = self.goalCell[1]/self.regionSize
        for i in range(len(self.deMap[xRegGoal][yRegGoal])):
            de = self.deMap[xRegGoal][yRegGoal][i]
            if self.goalCell in de:
                self.isGoalInDeadend = True
                self.goalNode = [xRegGoal, yRegGoal, 0, i]
                if not self.hasEntrance(self.grid, [xRegGoal, yRegGoal], de[0], []):
                    self.doesGoalNodeHaveEntrance = False
                break            
        
        # Find the deadend that starting cell belongs to
        for i in range(len(self.deMap[xRegion][yRegion])):
            de = self.deMap[xRegion][yRegion][i]
            if self.startCell in de:
                if self.goalCell in de:
                    traversedNodes.append([xRegion, yRegion, 0, i])
                    self.solution[:] = self.processRawSolution(traversedNodes)[:]
                    return
                else:
                    traversedNodes.append([xRegion, yRegion, 0, i])
                    end = de[0]    # deadends have only one opened end
                    if self.isGoalInDeadend and xRegGoal == xRegion and yRegGoal == yRegion:
                        if self.isConnected(de, self.deMap[xRegGoal][yRegGoal][self.goalNode[3]], [], True):
                            traversedNodes.append(self.goalNode)
                            self.solution[:] = self.processRawSolution(traversedNodes)[:]
                            return
                    if self.hasEntrance(self.grid, [xRegion, yRegion], end, []):
                        directions = self.cellIsAt(end, xRegion, yRegion)
                        for d in directions:
                            nextRegionCoordinate = [-1, -1]
                            if d == "top" and xRegion-1 >= 0:
                                nextRegionCoordinate = [xRegion-1, yRegion]
                            elif d == 'bottom' and xRegion+1 < self.nRegion:
                                nextRegionCoordinate = [xRegion+1, yRegion]
                            elif d == 'left' and yRegion-1 >= 0:
                                nextRegionCoordinate = [xRegion, yRegion-1]
                            elif d == 'right' and yRegion+1 < self.nRegion:
                                nextRegionCoordinate = [xRegion, yRegion+1]
                            foundSolution = self.findShortestSolution([end], self.goalCell, nextRegionCoordinate, traversedNodes)
                            if len(foundSolution) > 0:
                                self.solution[:] = self.processRawSolution(foundSolution)[:]
                                return
                    else:
                        pathsInRegion = self.pathMap[xRegion][yRegion]
                        for j in range(len(pathsInRegion)):
                            p = pathsInRegion[j]
                            ends = [end]
                            if self.isConnected([de[0]], p, [], True): # this means the starting cell is in a deadend whose opened end is inside the current region
                                traversedNodes.append([xRegion, yRegion, 1, j])
                                if len(p) == 1:
                                    ends = [p[0]]
                                else:
                                    ends = [p[0], p[-1]]
                            for e in ends:
                                directions = self.cellIsAt(e, xRegion, yRegion)
                                for d in directions:
                                    nextRegionCoordinate = [-1, -1]
                                    if d == "top" and xRegion-1 >= 0:
                                        nextRegionCoordinate = [xRegion-1, yRegion]
                                    elif d == 'bottom' and xRegion+1 < self.nRegion:
                                        nextRegionCoordinate = [xRegion+1, yRegion]
                                    elif d == 'left' and yRegion-1 >= 0:
                                        nextRegionCoordinate = [xRegion, yRegion-1]
                                    elif d == 'right' and yRegion+1 < self.nRegion:
                                        nextRegionCoordinate = [xRegion, yRegion+1]
                                    foundSolution = self.findShortestSolution([e], self.goalCell, nextRegionCoordinate, traversedNodes)
                                    if len(foundSolution) > 0:
                                        self.solution[:] = self.processRawSolution(foundSolution)[:]
                                        return
                            
        for i in range(len(self.pathMap[xRegion][yRegion])):
            p = self.pathMap[xRegion][yRegion][i]
            if self.startCell in p:
                if self.goalCell in p:
                    traversedNodes.append([xRegion, yRegion, 1, i])
                    self.solution[:] = self.processRawSolution(traversedNodes)[:]
                    return
                else:
                    if self.isGoalInDeadend and not self.doesGoalNodeHaveEntrance and self.goalNode[0] == xRegion and self.goalNode[1] == yRegion:
                        de = self.deMap[xRegion][yRegion][self.goalNode[3]]
                        if self.isConnected(p, de, [], True):
                            traversedNodes.append([xRegion, yRegion, 1, i])
                            traversedNodes.append(self.goalNode)
                            self.solution[:] = self.processRawSolution(traversedNodes)[:]
                            return
                    traversedNodes.append([xRegion, yRegion, 1, i])
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
                            foundSolution = self.findShortestSolution([end], self.goalCell, nextRegionCoordinate, traversedNodes)
                            if len(foundSolution) > 0:
                                self.solution[:] = self.processRawSolution(foundSolution)[:]
                                return
        
        


    def findShortestSolution(self, previousNode, goal, regionCoor, traversedNodes):
        """
        Find the shortest path that lead to the ending cell
        Params:
            previousNode: the path/deadend at the previous region
            goal: the ending cell
            regionCoor: the coordinate of the current region in the region map
            path: the traversed path
            traversedNodes: list of coordinates of traversed node (paths, deadends): [xRegion, yRegion, type of node (0 for deadend and 1 for path), index of node in self.pathNap of deMap]
        Return:
            A list of paths/deadend that make up the solution
        """
        if regionCoor == [-1, -1]:
            return []
        xRegion, yRegion = regionCoor
        
        deInRegion = self.deMap[xRegion][yRegion]
        pathsInRegion = self.pathMap[xRegion][yRegion]
        if self.isGoalInDeadend and regionCoor[0] == self.goalNode[0] and regionCoor[1] == self.goalNode[1]:  # If the current region has goal cell
            for i in range(len(deInRegion)):
                de = deInRegion[i]
                if goal in de:
                    if [xRegion, yRegion, 0, i] not in traversedNodes and self.hasEntrance(self.grid, regionCoor, de[0], []):
                        if self.isConnected(previousNode, [de[0]], [], False):
                            traversedNodes.append([xRegion, yRegion, 0, i])
                            return traversedNodes
                    elif [xRegion, yRegion, 0, i] not in traversedNodes and not self.hasEntrance(self.grid, regionCoor, de[0], []):
                        # The goal is in a deadend whose opened end is not an entrance. 
                        # Thus we have to look through the list of paths to find the path that connects this deadend and the previous node
                        ends = [de[0]]
                        for j in range(len(pathsInRegion)):
                            p = pathsInRegion[j]
                            if [xRegion, yRegion, 1, j] not in traversedNodes and self.isConnected(previousNode, p, [], False) and self.isConnected(ends, p, [], True):
                                traversedNodes.append([xRegion, yRegion, 1, j])
                                traversedNodes.append([xRegion, yRegion, 0, i])
                                return traversedNodes
                    
        for i in range(len(pathsInRegion)):
            p = pathsInRegion[i]
            if [xRegion, yRegion, 1, i] not in traversedNodes and self.isConnected(previousNode, p, [], False):
                newTraversedNodes = list(traversedNodes)
                newTraversedNodes.append([xRegion, yRegion, 1, i])
                if goal in p:
                    return newTraversedNodes
                else:
                    if self.isGoalInDeadend and not self.doesGoalNodeHaveEntrance and self.goalNode[0] == xRegion and self.goalNode[1] == yRegion:
                        de = self.deMap[xRegion][yRegion][self.goalNode[3]]
                        if self.isConnected(p, [de[0]], [], True):
                            traversedNodes.append(self.goalNode)
                            self.solution[:] = self.processRawSolution(traversedNodes)[:]
                            return
                    # Check neighbor regions at both ends of this path
                    ends = [p[0], p[-1]]
                    for end in ends:
                        directions = self.cellIsAt(end, xRegion, yRegion)
                        for d in directions:
                            nextRegionCoordinate = [-1, -1]
                            if  d == "top" and xRegion-1 >= 0 and [[end[0]-1, end[1]]] != previousNode:
                                nextRegionCoordinate = [xRegion-1, yRegion]
                            elif d == 'bottom' and xRegion+1 < self.nRegion and [[end[0]+1, end[1]]] != previousNode:
                                nextRegionCoordinate = [xRegion+1, yRegion]
                            elif d == 'left' and yRegion-1 >= 0 and [[end[0], end[1]-1]] != previousNode:
                                nextRegionCoordinate = [xRegion, yRegion-1]
                            elif d == 'right' and yRegion+1 < self.nRegion and [[end[0], end[1]+1]] != previousNode:
                                nextRegionCoordinate = [xRegion, yRegion+1]
                            foundSolution = self.findShortestSolution([end], goal, nextRegionCoordinate, newTraversedNodes)
                            if len(foundSolution) > 0:
                                return foundSolution
        
        return []
        
    def isConnected(self, p1, p2, atCells, bruteForce):
        """
        Check if 2 paths are connected
        Params:
            p1, p2: 2 paths
            atCell: the cell in p2 where 2 paths connect
            bruteForce: If True, scan through the paths to find the intersection
                        If False, only check the 2 ends of the paths
        """
        if bruteForce:
            hasCommonSubpath = False
            #for i in range(len(p1)):
            i = 0
            while i < len(p1):
                c1 = p1[i]
                #for j in range(len(p2)):
                j = 0
                while j < len(p2):
                    c2 = p2[j]
                    if c1 == c2:
                        hasCommonSubpath = True
                        if i+1<len(p1):
                            i = i + 1
                            j = j + 1
                            c1 = p1[i]
                            l = list([c1, c2])
                            atCells[:] = l[:]
                            continue
                        break
                    else:
                        if hasCommonSubpath:
                            return True
                        else:
                            l = list([c1, c2])
                            atCells[:] = l[:]
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
                    j = j + 1
                i = i + 1
        else:
            ends1 = [p1[0], p1[-1]]
            ends2 = [p2[0], p2[-1]]
            for e1 in ends1:
                for e2 in ends2:
                    l = list([e1, e2])
                    atCells[:] = l[:]
                    if e1 == e2:
                        return True
                    if e1[0] == e2[0]:
                        if e1[1] == e2[1]-1:
                            if self.grid[e1[0]][e1[1]].right == 0 and self.grid[e2[0]][e2[1]].left == 0:
                                return True
                        elif e1[1] == e2[1]+1:
                            if self.grid[e1[0]][e1[1]].left == 0 and self.grid[e2[0]][e2[1]].right == 0:
                                return True
                    elif e1[1] == e2[1]:
                        if e1[0] == e2[0]-1:
                            if self.grid[e1[0]][e1[1]].bottom == 0 and self.grid[e2[0]][e2[1]].top == 0:
                                return True
                        elif e1[0] == e2[0]+1:
                            if self.grid[e1[0]][e1[1]].top == 0 and self.grid[e2[0]][e2[1]].bottom == 0:
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
    
    def trimPaths(self, traversedNodes):
        """
        Remove unnecessary cells in the nodes that make up the solution
        Params:
            traversedNodes: The list of nodes (paths, deadends) that make up the solution
        Return:
            The solution path
        """
        solution = []
        
        p = self.getNode(traversedNodes, 0)
        if self.goalCell in p:
            idx1, idx2 = -1, -1
            try:
                idx1 = p.index(self.startCell)
                idx2 = p.index(self.goalCell)
            except:
                pass
            if idx1 != -1 and idx2 != -1:
                if idx2 <= idx1:
                    p = list(reversed(p))
                    l = len(p)
                    solution = p[l-1-idx2:l-idx1]
                else:
                    solution = p[idx1:idx2+1]
                return solution
        else:
            startIdx = -1
            try:
                startIdx = p.index(self.startCell)
            except:
                pass
            if startIdx != -1:
                for i in range(len(traversedNodes)):
                    if i != 0:
                        curPath = self.getNode(traversedNodes, i)
                        atCells = []
                        if traversedNodes[i][2] == 0 or traversedNodes[i-1][2] == 0:# and not self.doesGoalNodeHaveEntrance:   # curPath is a deadend whose opened end is not an entrance
                            if self.isConnected(p, curPath, atCells, True):
                                idx1, idx2 = -1, -1
                                try:
                                    idx1 = p.index(atCells[0])
                                    idx2 = curPath.index(atCells[1])
                                except:
                                    pass
                                subPath = self.getSubpath(p, startIdx, idx1)
                                solution = solution + subPath
                                p = curPath
                                startIdx = idx2
                        else:
                            if self.isConnected(p, curPath, atCells, False):
                                idx1, idx2 = -1, -1
                                try:
                                    idx1 = p.index(atCells[0])
                                    idx2 = curPath.index(atCells[1])
                                except:
                                    pass
                                subPath = self.getSubpath(p, startIdx, idx1)
                                solution = solution + subPath
                                p = curPath
                                startIdx = idx2
                goalIdx = -1
                try:
                    goalIdx = p.index(self.goalCell)
                except:
                    pass
                if goalIdx != -1:
                    subPath = self.getSubpath(p, startIdx, goalIdx)
                    solution = solution + subPath
                    
            return solution
            
    def getNode(self, traversedNodes, index):
        """
        Return the path/deadend by index from traversedNodes when index is in range
        Return None when index is out of range        
        """
        if index >= 0 and index < len(traversedNodes):
            node = traversedNodes[index]
            if node[2] == 0:
                return self.deMap[node[0]][node[1]][node[3]]
            else:
                return self.pathMap[node[0]][node[1]][node[3]]
        else:
            return None
        
    def getSubpath(self, p, idx1, idx2):
        result = []
        if idx1 < 0 or idx2 <0 or idx1 >= len(p) or idx2 >= len(p):
            return result
        else:
            if idx1 == idx2:
                result = [p[idx1]]
            elif idx1 > idx2:
                result = list(reversed(p[idx2:idx1+1]))
            else:
                result = p[idx1:idx2+1]
        return result
    
    def processRawSolution(self, rawSolution):
        """
        Params:
            rawSolution: the list of traversedNodes that make up the solution. Each element of the list is [xRegion, yRegion, type_of_node, index_of_node_in_node_list]
                        The node lists are self.deMap and self.pathMap
        Return:
            A path that is the solution
        """
        solution = self.trimPaths(rawSolution)
        #print solution
        return solution