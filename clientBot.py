'''
Created on Aug 18, 2015

@author: ldhuy
'''
from globalGroundTruth import globalGroundTruth as ggt
import socket
import time
import threading
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.defer import Deferred
#from tablib.packages.odf.style import RegionCenter


class Echo(Protocol):
    def sendMessage(self, msg):
        self.transport.write(msg)

class EchoClientFactory(ClientFactory):
    protocol = Echo

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

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
        

        
    def run(self):
        threading.Thread.run(self)
        r = self.path[-1][0]
        c = self.path[-1][1]
        factory = EchoClientFactory()
        self.point = reactor.connectTCP('localhost', 51510, factory)
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
                    self.point.sendLine(package)
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
                    self.point.sendLine(package)
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
                    self.point.sendLine(package)
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
                    self.point.sendLine(package)
                self.lockMap[nextRegionX][nextRegionY].release()
            if not move:
                del self.path[-1]
                if self.path:
                    r = self.path[-1][0]
                    c = self.path[-1][1]

        self.point.transport.loseConnection()
                    
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
       
            
        
        