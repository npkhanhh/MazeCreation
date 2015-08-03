'''
Created on Jul 7, 2015

@author: ldhuy
'''
from PathConnectorNew import PathConnectorNew
from PathConnector import PathConnector
import time

def FindSolution(grid, regionMap, deMap, nRegion, mazeSize, start, goal):
    """
    Find the solution from explored maze
    Params:
        grid: the maze
        regionMap: paths in each region
        deMap: deadends in each region
        nRegion: the number of region (nRegion*nRegion)
        mazeSize: the length of side of the maze
        start: coordinate of the starting cell
        goal: coordinate of the ending cell
    """
    solution = [[]]
    t0 = time.time()
    pathCnt = PathConnectorNew(grid, start, goal, regionMap, deMap, nRegion, mazeSize, solution)
    pathCnt.start()
    pathCnt.join()
    print "PathConnectorNew finished running in {0}s".format(time.time() - t0)

