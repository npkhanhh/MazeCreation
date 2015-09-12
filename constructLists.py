'''
Created on Aug 9, 2015

@author: ldhuy
'''
import threading
from FindNodes import FindNodes
import time
import logging

def isConnected(grid, n1, n2, atCells, bruteForce):
    """
    Check if 2 paths are connected
    Params:
        grid: the grid of maze
        n1, n2: 2 nodes
        atCell: the cell in p2 where 2 paths connect
        bruteForce: If True, scan through the paths to find the intersection
                    If False, only check the 2 ends of the paths
    """
    p1 = n1.path
    p2 = n2.path
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
                    if n1.type == 'p' and n2.type == 'p' and i == 0 and j == 0:
                        return False
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
                                if grid[c1[0]][c1[1]].right == 0 and grid[c2[0]][c2[1]].left == 0:
                                    return True
                            elif c1[1] == c2[1]+1:
                                if grid[c1[0]][c1[1]].left == 0 and grid[c2[0]][c2[1]].right == 0:
                                    return True
                        elif c1[1] == c2[1]:
                            if c1[0] == c2[0]-1:
                                if grid[c1[0]][c1[1]].bottom == 0 and grid[c2[0]][c2[1]].top == 0:
                                    return True
                            elif c1[0] == c2[0]+1:
                                if grid[c1[0]][c1[1]].top == 0 and grid[c2[0]][c2[1]].bottom == 0:
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
                    return False
                if e1[0] == e2[0]:
                    if e1[1] == e2[1]-1:
                        if grid[e1[0]][e1[1]].right == 0 and grid[e2[0]][e2[1]].left == 0:
                            return True
                    elif e1[1] == e2[1]+1:
                        if grid[e1[0]][e1[1]].left == 0 and grid[e2[0]][e2[1]].right == 0:
                            return True
                elif e1[1] == e2[1]:
                    if e1[0] == e2[0]-1:
                        if grid[e1[0]][e1[1]].bottom == 0 and grid[e2[0]][e2[1]].top == 0:
                            return True
                    elif e1[0] == e2[0]+1:
                        if grid[e1[0]][e1[1]].top == 0 and grid[e2[0]][e2[1]].bottom == 0:
                            return True
    return False

def getNeighborRegions(nRegion, curReg):
    """
    Get the coordinates of neighbor regions of the current region
    Params:
        nRegion: the number of regions at each side of the maze
        curReg: the coordinate of the current region
    Return:
        A list of coordinates of regions next to current one 
    """
    neighborReg = []
    if curReg[0] > 0:
        neighborReg.append([curReg[0]-1, curReg[1]])
    if curReg[0] + 1 < nRegion:
        neighborReg.append([curReg[0]+1, curReg[1]])
    if curReg[1] > 0:
        neighborReg.append([curReg[0], curReg[1]-1])
    if curReg[1] + 1 < nRegion:
        neighborReg.append([curReg[0], curReg[1]+1])
    return neighborReg

def constructLists(maze, pathMap, deMap, nodeMap):
    """
    Divide the maze into regions, in each region find all the paths and dead-ends. These paths and dead-ends are called nodes.
    Then build a map of regions.
    Return the number of region at each side of the maze
    """
    nRegion = 5
    regionSize = maze.size / nRegion
    pathMap[:] = [[[] for x in range(nRegion)] for y in range(nRegion)][:]
    deMap[:] = [[[] for x in range(nRegion)] for y in range(nRegion)][:]
    nodeMap[:] = [[[] for x in range(nRegion)] for y in range(nRegion)][:]
    lock = threading.Lock()
    threads = []
    for i in range(nRegion):
        for j in range(nRegion):
            nodeFinder = FindNodes(maze.grid, [i*regionSize, (i+1)*regionSize, j*regionSize, (j+1)*regionSize], i, j, pathMap, deMap, nodeMap, lock)
            threads.append(nodeFinder)
            nodeFinder.start()
    
    for t in threads:
        t.join()

#     print "Path Map"
#     print(pathMap)
#     print "\nDeadend Map"
#     print(deMap)
#     print "\nNode Map"
#     print(nodeMap)
    
    # Set neighbors
    count = 0
    t0 = time.time()
    for iReg in range(nRegion):
        for jReg in range(nRegion):
            neighborReg = getNeighborRegions(nRegion, [iReg, jReg])
            count += len(nodeMap[iReg][jReg])
            for iNode in nodeMap[iReg][jReg]:
                for jNode in nodeMap[iReg][jReg]:
                    # Consider nodes in local region
                    if iNode != jNode and isConnected(maze.grid, iNode, jNode, [], True):
                        iNode.add_neighbor(jNode)
                        jNode.add_neighbor(iNode)
                    for nb in neighborReg:
                        nodeList = nodeMap[nb[0]][nb[1]]
                        for kNode in nodeList:
                            if isConnected(maze.grid, iNode, kNode, [], False):
                                if kNode not in iNode.neighbors:
                                    iNode.add_neighbor(kNode)
                                if iNode not in kNode.neighbors:
                                    kNode.add_neighbor(iNode)

    t = time.time() - t0
    print "Constructing time: {}s".format(t)
    print "Number of nodes: {}".format(count)
    logging.info("Constructing time: {}s".format(t))
    logging.info("Number of nodes: {}".format(count))
    return nRegion