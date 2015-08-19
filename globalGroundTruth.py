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
    def setMaze(_maze):
        globalGroundTruth.maze = _maze
        
    @staticmethod
    def setupVisited(nRegion):
        globalGroundTruth.visited = [[[[0 for i in range(globalGroundTruth.maze.size/nRegion)] for j in range(globalGroundTruth.maze.size/nRegion)] for iReg in range(nRegion)] for jReg in range(nRegion)]
        regSize = globalGroundTruth.maze.size/nRegion
        extra = globalGroundTruth.maze.size % nRegion
        
        # Add extra column
        for e in range(extra):
            for i in range(nRegion-1):
                currentReg = globalGroundTruth.visited[i][-1]
                for j in range(regSize):
                    currentReg[j].append(0)
        
        # Add extra row
        for e in range(extra):
            for i in range(nRegion-1):
                currentReg = globalGroundTruth.visited[-1][i]
                currentReg.append([0 for j in range(regSize)])
        
        # Add extra cell for region at the corner
        for e in range(extra):
            currentReg = globalGroundTruth.visited[-1][-1]
            currentReg.append([0 for i in range(regSize+e)])
            for j in range(len(currentReg)):
                currentReg[j].append(0)
            
        
        
#         if extra > 0:
#             for i in range(extra):
#                 for j in range(nRegion):
#                     globalGroundTruth.visited[j][-1].append([0 for k in range(regSize)])
#                     regSize =regSize
#                     for k in range(regSize):
#                         globalGroundTruth.visited[-1][j].append([0 for k in range(regSize)])
#                         globalGroundTruth.visited[-1][-1][-1].append(1)
                    

            
            
            
            
        
        