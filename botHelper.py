import botThread as bt
from clientBot import clientBot as cb
import random as ran
import Maze as m
import Utility as u
import timeit
import threading
from server import server 
from globalGroundTruth import globalGroundTruth as gg

class botHelper:
    def __init__(self, no_bot, groundTruth, mode):
        self.no_bot = no_bot
        self.groundTruth = groundTruth
        self.tempMaze = m.Maze(groundTruth.size)
        gg.setMaze(groundTruth)
        self.mode = mode


    def runBot(self):
        f = open('timeexplore.txt', 'a')
        
        self.nRegion = u.findGreatestSmallerSquaredNumber(self.no_bot)
        gg.setupVisited(self.nRegion)
        self.sv = server(self.no_bot, self.tempMaze, 'blah')
        self.sv.start()
        
        self.lockMap = [[threading.Lock() for i in range(self.nRegion)] for j in range(self.nRegion)]
        

        bots = []
        paths = [[] for i in range(self.no_bot)]
        visited = [[0 for i in range(self.groundTruth.size)] for j in range(self.groundTruth.size)]
        size = self.groundTruth.size
        if self.mode == 'Random':
            for i in range(self.no_bot):
                r = ran.randint(0, size-1)
                c = ran.randint(0, size-1)
                while visited[r][c]:
                    r = ran.randint(0, size-1)
                    c = ran.randint(0, size-1)
                paths[i].append([r,c,-1])
                visited[r][c] = 1
                self.updateTempMaze(r, c)
        elif self.mode == 'Region':
            numberOfRows = u.findNearSquaredNumber(self.no_bot)
            noBotsPerRow = int(self.no_bot/numberOfRows)
            botsPerRow = [noBotsPerRow for i in range(numberOfRows)]
            botLeft = self.no_bot - noBotsPerRow*numberOfRows
            for i in range(botLeft):
                botsPerRow[i] += 1
            vsize = size/numberOfRows
            botcount = 0
            for i in range(numberOfRows):
                hsize = size/botsPerRow[i]
                for j in range(botsPerRow[i]):
                    r = ran.randint(vsize*i, vsize*(i+1)-1)
                    c = ran.randint(hsize*j, hsize*(j+1)-1)
                    paths[botcount].append([r,c,-1])
                    visited[r][c] = 1
                    self.updateTempMaze(r, c)
                    botcount+=1

        tic = timeit.default_timer()
#         stop = False
#         end = [False for i in range(self.no_bot)]
#         overlap = True
#         lock = threading.Lock()
#         for cell in paths:
#             bots.append(bt.bot(cell[0][0], cell[0][1], lock, self.groundTruth, self.tempMaze, visited))
#         for i in range(self.no_bot):
#             bots[i].start()
#         for i in range(self.no_bot):
#             bots[i].join()
#         #for i in range(self.no_bot):
#         #    print paths[i]

        regionSize = self.groundTruth.size/self.nRegion
        for i in range(self.no_bot):
            bots.append(cb(paths[i][0], self.lockMap, regionSize))
        
        for i in range(self.no_bot):
            bots[i].start()
            
        for t in bots:
            t.join()
        print "All bots done"
        toc = timeit.default_timer()
        f.write(str(size) + ' ' + str(self.no_bot) + ' ' + str(self.mode) + ' ' + str(toc-tic) + '\n')
        count = 0
        for i in range(size):
            for j in range(size):
                if visited[i][j]:
                    count += 1

        print('Explore completed')
        print('Cell explored: ' + str(count) + '/' + str(size*size))

    def updateTempMaze(self, r, c):
        self.tempMaze.grid[r][c].top = self.groundTruth.grid[r][c].top
        self.tempMaze.grid[r][c].bottom = self.groundTruth.grid[r][c].bottom
        self.tempMaze.grid[r][c].left = self.groundTruth.grid[r][c].left
        self.tempMaze.grid[r][c].right = self.groundTruth.grid[r][c].right
