'''
Created on Aug 18, 2015

@author: ldhuy
'''

class globalGroundTruth(object):
    '''
    ground truth for robots
    '''
    maze = None
    visited = None
    
    @staticmethod
    def setMaze(self, maze):
        self.maze = maze
        
    @staticmethod
    def setupVisited(self, nRegion):
        self.visited = [[[[0 for i in range(self.maze.size/nRegion)] for j in range(self.maze.size/nRegion)] for iReg in range(nRegion)] for jReg in range(nRegion)]