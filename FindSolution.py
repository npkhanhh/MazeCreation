'''
Created on Jul 7, 2015

@author: ldhuy
'''
from PathConnectorNew import PathConnectorNew

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
    regionSize = mazeSize / nRegion
    xRegion = start[0]/regionSize
    yRegion = start[1]/regionSize
    solution = [[]]
    pathCnt = PathConnectorNew(grid, start, goal, regionMap, deMap, nRegion, mazeSize, solution)
    pathCnt.start()
    pathCnt.join()
    print "\nFinish\n"
    print solution

