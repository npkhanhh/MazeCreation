'''
Created on Jul 7, 2015

@author: ldhuy
'''
from PathConnector import PathConnector

def FindSolution(grid, regionMap, nRegion, mazeSize, start, goal):
    """
    Find the solution from explored maze
    Params:
        grid: the maze
        regionMap: paths in each region
        nRegion: the number of region (nRegion*nRegion)
        mazeSize: the length of side of the maze
        start: coordinate of the starting cell
        goal: coordinate of the ending cell
    """
    regionSize = mazeSize / nRegion
    xRegion = start[0]/regionSize
    yRegion = start[1]/regionSize
    pathCnt = PathConnector(grid, start, goal, regionMap, xRegion, yRegion, nRegion, mazeSize)
    pathCnt.start()
    pathCnt.join()
    print "\nFinish\n"

