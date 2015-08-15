'''
Created on Jul 15, 2015

@author: ldhuy
'''
import threading

class PathConnector(threading.Thread):
    '''
    Receive the discovered nodes and find shortest path that connect 2 specific cells
    '''


    def __init__(self, grid, startCell, goalCell, mazeSize, nodeMap, nRegion, solution):
        '''
        Params:
            maze: the maze
            startCell: the coordinate of the cell this robot starts at [x, y]
            goalCell: the coordinate of the cell this robot needs to find path that leads to [x, y]
            nodeMap: the 2D array of nodes (paths, dead-ends) 
            nRegion: the program divides the maze into nRgion*nRegion regions to run RegionSolver(s)
            solution: the found solution
        '''
        threading.Thread.__init__(self)
        self.grid = grid
        self.startCell = startCell
        self.goalCell = goalCell
        
        self.nRegion = nRegion
        self.mazeSize = mazeSize
        
        self.nodeMap = nodeMap
        
        self.regionSize = self.mazeSize / nRegion
        
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
        traversedNodes = []
        discoveredNodes = []
        solutionFound = False
        stack = []
        nodesInStartReg = self.nodeMap[self.xRegStart][self.yRegStart]
        for node in nodesInStartReg:
            if self.startCell in node.path:
                stack.append(node)
                break
        
        # Look for goal cell using DFS
        while not solutionFound and len(stack) > 0:
            n = stack.pop(0)
            if n not in discoveredNodes:
                discoveredNodes.append(n)
                if len(traversedNodes) > 0 and n not in traversedNodes[-1].neighbors:
                    # This node is not a neighbor of the last node in traversedNode
                    newTraversedNodes = self.findLastNeighbor(traversedNodes, n)
                    newTraversedNodes.append(n)
                    traversedNodes = newTraversedNodes
                elif n not in traversedNodes:
                    traversedNodes.append(n)
                if self.goalCell in n.path:
                    solutionFound = True
                    print "traversedNodes:"
                    print traversedNodes
                    self.solution[:] = self.getSolution(traversedNodes)[:]
                else:
                    children = n.neighbors
                    for child in children:
                        if child not in stack and child not in discoveredNodes:
                            stack.insert(0, child)
            
        
        
    def findLastNeighbor(self, traversedNodes, node):
        """
        Params:
            traversedNodes: list of traversed nodes
            node: the current node
        Return:
            A new traversedNode does not contain list of nodes from last neighbor of node to the end of the old traversedNodes
        """
        idx = -1
        for i in reversed(range(len(traversedNodes))):
            if traversedNodes[i] not in node.neighbors:
                idx = i
                break
        result = traversedNodes[0:idx+1]
        return result
        
    def getSolution(self, traversedNodes):
        """
        Get the list of cells that make up the solution from the traversed nodes
        Param:
            traversedNodes: a list of nodes that make up the solution
        Return:
            The solution
        """
        solution = []
        p1 = traversedNodes[0].path
        startIdx = -1
        try:
            startIdx = p1.index(self.startCell)
        except:
            pass
            
        for i in range(len(traversedNodes)):
            if i == 1 or i == len(traversedNodes)-1:
                p2 = traversedNodes[i].path 
                atCells = []
                if self.isConnected(p1, p2, atCells, True):
                    p1 = self.getSubpath(p1, startIdx, atCells[0])
                    solution = solution + p1
                    p1 = p2
                    startIdx = atCells[1]
            if i != 0 and i != 1 and i != len(traversedNodes)-1:
                p2 = traversedNodes[i].path 
                atCells = []
                if self.isConnected(p1, p2, atCells, False):
                    p1 = self.getSubpath(p1, startIdx, atCells[0])
                    solution = solution + p1
                    p1 = p2
                    startIdx = atCells[1]
        return solution
        
     
        


    
        
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