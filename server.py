'''
Created on Aug 18, 2015

@author: ldhuy
'''
import Maze as m
import socket
import threading

class server(threading.Thread):
    '''
    Server to get explored information from robots
    '''


    def __init__(self, no_bot, exploredMaze, mode):
        '''
        Constructor
        Param:
            nBot: the number of robots dropped in the maze
        '''
        threading.Thread.__init__(self)
        # Connect to all the robots
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socket.gethostname(), 51515))
        print "Server socket created"
        self.serversocket.listen(5)
        self.connectionList = []
        
        self.exploredMaze = exploredMaze
        self.no_bot = no_bot
        self.mode = mode
        
    def run(self):
        threading.Thread.run(self)
        nConnectedBot = 0
        while nConnectedBot < self.no_bot:
            conn, addr = self.serversocket.accept()
            self.connectionList.append([conn, addr])
            nConnectedBot += 1
            
        nBotDone = 0
        while nBotDone < self.no_bot:
            package = self.serversocket.recv(1024)
            print "Server receives package:" + package
            package = package.split()
            if package[0] == 'updateCoor':
                newPos = [int(package[1]), int(package[2])]
                cellInfo = [int(package[3]), int(package[4]), int(package[5]), int(package[6])]
                self.exploredMaze.grid[newPos[0]][newPos[1]].top = cellInfo[0]
                self.exploredMaze.grid[newPos[0]][newPos[1]].right = cellInfo[1]
                self.exploredMaze.grid[newPos[0]][newPos[1]].bottom = cellInfo[2]
                self.exploredMaze.grid[newPos[0]][newPos[1]].left = cellInfo[3]
            elif package[0] == "Done":
                print "Received package done"
                nBotDone += 1
        
        self.exploredMaze.save("TextMazeSocket.txt")    
        self.serversocket.close()
        print "Maze saved"
