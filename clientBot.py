'''
Created on Aug 18, 2015

@author: ldhuy
'''
from globalGroundTruth import globalGroundTruth as ggt
import socket
import time
import threading
from tablib.packages.odf.style import RegionCenter

class clientBot(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, startPos, lockMap, regionSize):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.startRow = startPos[0]
        self.startCol = startPos[1]
        self.lockMap = lockMap
        self.globalGroundTruth = ggt.maze
        self.visited = ggt.visited
        self.path = [[self.startRow, self.startCol]]
        self.regionSize = regionSize
        
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((socket.gethostname(), 51515))
        
    def run(self):
        threading.Thread.run(self)
        r = self.path[-1][0]
        c = self.path[-1][1]
        while self.path:
            move = False
            if self.globalGroundTruth.grid[r][c].top == 0:
                nextR, nextC = r-1, c
                newCoor = []
                nextRegionX, nextRegionY = self.findCurrentReg(nextR, nextC, newCoor)
                self.lockMap[nextRegionX][nextRegionY].acquire()
                
                if self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] != 1:
                    self.path.append([r-1, c])
                    move = True
                    r = r - 1
                    self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] = 1
                    # Send message to server
                    cellInfo = self.updateTempMaze(r, c)
                    package = "{0} {1} {2} {3} {4} {5} {6}".format("updateCoor", r, c, cellInfo[0], cellInfo[1], cellInfo[2], cellInfo[3])
                    self.soc.sendall(package)                    
                self.lockMap[nextRegionX][nextRegionY].release()
            elif self.globalGroundTruth.grid[r][c].right == 0:
                nextR, nextC = r, c+1
                newCoor = []
                nextRegionX, nextRegionY = self.findCurrentReg(nextR, nextC, newCoor)
                self.lockMap[nextRegionX][nextRegionY].acquire()
                if self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] != 1:
                    self.path.append([r, c+1])
                    move = True
                    c = c + 1
                    self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] = 1
                    # Send message to server
                    cellInfo = self.updateTempMaze(r, c)
                    package = "{0} {1} {2} {3} {4} {5} {6}".format("updateCoor", r, c, cellInfo[0], cellInfo[1], cellInfo[2], cellInfo[3])
                    self.soc.sendall(package)
                self.lockMap[nextRegionX][nextRegionY].release()    
            elif self.globalGroundTruth.grid[r][c].bottom == 0:
                nextR, nextC = r+1, c
                newCoor = []
                nextRegionX, nextRegionY = self.findCurrentReg(nextR, nextC, newCoor)
                self.lockMap[nextRegionX][nextRegionY].acquire()
                if self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] != 1:
                    self.path.append([r+1, c])
                    move = True
                    r = r + 1
                    self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] = 1
                    # Send message to server
                    cellInfo = self.updateTempMaze(r, c)
                    package = "{0} {1} {2} {3} {4} {5} {6}".format("updateCoor", r, c, cellInfo[0], cellInfo[1], cellInfo[2], cellInfo[3])
                    self.soc.sendall(package)
                self.lockMap[nextRegionX][nextRegionY].release()
            elif self.globalGroundTruth.grid[r][c].left == 0:
                nextR, nextC = r, c-1
                newCoor = []
                nextRegionX, nextRegionY = self.findCurrentReg(nextR, nextC, newCoor)
                self.lockMap[nextRegionX][nextRegionY].acquire()
                if self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] != 1:
                    self.path.append([r, c-1])
                    move = True
                    c = c - 1
                    self.visited[nextRegionX][nextRegionY][newCoor[0]][newCoor[1]] = 1
                    # Send message to server
                    cellInfo = self.updateTempMaze(r, c)
                    package = "{0} {1} {2} {3} {4} {5} {6}".format("updateCoor", r, c, cellInfo[0], cellInfo[1], cellInfo[2], cellInfo[3])
                    self.soc.sendall(package)
                self.lockMap[nextRegionX][nextRegionY].release()
            if not move:
                del self.path[-1]
                if self.path:
                    r = self.path[-1][0]
                    c = self.path[-1][1]
        package = "Done"
        self.soc.sendall(package)
        self.soc.close()
                    
    def updateTempMaze(self, r, c):
        top = self.globalGroundTruth.grid[r][c].top
        bottom = self.globalGroundTruth.grid[r][c].bottom
        left = self.globalGroundTruth.grid[r][c].left
        right = self.globalGroundTruth.grid[r][c].right
        return [top, right, bottom, left]

    def findCurrentReg(self, row, col, newCoordinate):
        """
        Return a list of coordinate of current region
        """
        xNew = 0
        yNew = 0
        nRegion = len(self.lockMap[0])
        xRegion = row/self.regionSize
        if xRegion == nRegion - 1:
            xNew = row - (nRegion-1)*self.regionSize
        else:
            xNew = row % self.regionSize
        
        yRegion = col/self.regionSize
        if yRegion == nRegion-1:
            yNew = col - (nRegion-1)*self.regionSize
        else:
            yNew = col % self.regionSize
            
        newCoordinate[:] = [xNew, yNew][:] 
        return [xRegion, yRegion]
       
            
        
        