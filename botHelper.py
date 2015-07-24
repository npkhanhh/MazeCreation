import bot as b
import random as ran
import Maze as m
import Utility as u
import timeit

class botHelper:
    def __init__(self, no_bot, groundTruth, mode):
        self.no_bot = no_bot
        self.groundTruth = groundTruth
        self.tempMaze = m.Maze(groundTruth.size)
        self.mode = mode


    def runBot(self):
        f = open('timeexplore.txt', 'a')

        bots = []
        paths = [[] for i in range(self.no_bot)]
        visisted = [[0 for i in range(self.groundTruth.size)] for j in range(self.groundTruth.size)]
        size = self.groundTruth.size
        if self.mode == 'Random':
            for i in range(self.no_bot):
                r = ran.randint(0, size-1)
                c = ran.randint(0, size-1)
                while visisted[r][c]:
                    r = ran.randint(0, size-1)
                    c = ran.randint(0, size-1)
                paths[i].append([r,c,-1])
                visisted[r][c] = 1
                self.updateTempMaze(r, c)
        elif self.mode == 'Region':
            numberOfRows = u.findNearSquaredNumber(self.no_bot)
            print(numberOfRows)
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
                    visisted[r][c] = 1
                    self.updateTempMaze(r, c)
                    botcount+=1

        tic = timeit.default_timer()
        stop = False
        end = [False for i in range(self.no_bot)]
        overlap = True
        while not stop:
            stop = True
            for i in range(self.no_bot):
                if not end[i]:
                    r = paths[i][-1][0]
                    c = paths[i][-1][1]
                    move = False
                    if ((overlap and r>0) or (not overlap and r>bots[i].minr)) and self.groundTruth.grid[r][c].top == 0 and visisted[r-1][c] == 0:
                        r = r - 1
                        paths[i].append([r,c,2])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and r<size-1) or (not overlap and r<bots[i].maxr)) and self.groundTruth.grid[r][c].bottom == 0 and visisted[r+1][c] == 0:
                        r = r + 1
                        paths[i].append([r,c,0])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and c>0) or (not overlap and c>bots[i].minc)) and self.groundTruth.grid[r][c].left == 0 and visisted[r][c-1] == 0:
                        c = c - 1
                        paths[i].append([r,c,1])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and c<size-1) or (not overlap and c<bots[i].maxc)) and self.groundTruth.grid[r][c].right == 0 and visisted[r][c+1] == 0:
                        c = c + 1
                        paths[i].append([r,c,3])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    if not move:
                        prev = paths[i][-1][2]
                        del paths[i][-1]
                        if not paths[i]:
                            end[i] = True
                for i in range(self.no_bot):
                    if not end[i]:
                        stop = False
                        break

        #for i in range(self.no_bot):
        #    print paths[i]
        toc = timeit.default_timer()
        f.write(str(self.no_bot) + ' ' + str(self.mode) + ' ' + str(toc-tic) + '\n')
        count = 0
        for i in range(size):
            for j in range(size):
                if visisted[i][j]:
                    count += 1

        print('Explore completed')
        print('Cell explored: ' + str(count) + '/' + str(size*size))

    def updateTempMaze(self, r, c):
        self.tempMaze.grid[r][c].top = self.groundTruth.grid[r][c].top
        self.tempMaze.grid[r][c].bottom = self.groundTruth.grid[r][c].bottom
        self.tempMaze.grid[r][c].left = self.groundTruth.grid[r][c].left
        self.tempMaze.grid[r][c].right = self.groundTruth.grid[r][c].right
