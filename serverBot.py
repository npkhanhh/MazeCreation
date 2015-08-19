from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.python import log
import threading

class serverProtocol(LineReceiver):
    def __init__(self, factory, mazeExplored):
        self.factory = factory
        self.mazeExplored = mazeExplored


    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1


    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1
        if self.factory.numProtocols == 0:
            reactor.stop()

    def lineReceived(self, package):
        package = package.split()
        newPos = [int(package[1]), int(package[2])]
        cellInfo = [int(package[3]), int(package[4]), int(package[5]), int(package[6])]
        self.exploredMaze.grid[newPos[0]][newPos[1]].top = cellInfo[0]
        self.exploredMaze.grid[newPos[0]][newPos[1]].right = cellInfo[1]
        self.exploredMaze.grid[newPos[0]][newPos[1]].bottom = cellInfo[2]
        self.exploredMaze.grid[newPos[0]][newPos[1]].left = cellInfo[3]

class serverFactory(Factory):
    def __init__(self, mazeExplored):
        self.mazeExplored = mazeExplored
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return serverProtocol(self, self.mazeExplored)

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
        # self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.serversocket.bind((socket.gethostname(), 51515))
        # print "Server socket created"
        # self.serversocket.listen(5)

        self.connectionList = []

        self.exploredMaze = exploredMaze
        self.no_bot = no_bot
        self.mode = mode

    def run(self):
        threading.Thread.run(self)
        reactor.listenTCP(51510, serverFactory(self.exploredMaze))
        reactor.run(installSignalHandlers=0)
