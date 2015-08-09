'''
Created on Jul 7, 2015

@author: ldhuy
'''
from PathConnectorNew import PathConnectorNew
from PathConnector import PathConnector
import time

def FindSolution(grid, pathMap, deMap, nRegion, mazeSize, start, goal):
    """
    Find the solution from explored maze
    Params:
        grid: the maze
        pathMap: paths in each region
        deMap: deadends in each region
        nRegion: the number of region (nRegion*nRegion)
        mazeSize: the length of side of the maze
        start: coordinate of the starting cell
        goal: coordinate of the ending cell
    Return:
        The solution
    """
    solution = [[]]
    #t0 = time.time()
    pathCnt = PathConnectorNew(grid, start, goal, pathMap, deMap, nRegion, mazeSize, solution)
    pathCnt.start()
    pathCnt.join()
    #print "PathConnectorNew finished running in {0}s".format(time.time() - t0)
    print "\nSolution from {0} to {1} :".format(str(start), str(goal)) 
    print solution
    
    return solution