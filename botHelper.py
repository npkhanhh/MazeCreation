import bot as b
import random as ran
import Maze as m

class botHelper:
    def __init__(self, no_bot, groundTruth, canvas):
        self.no_bot = no_bot
        self.groundTruth = groundTruth
        self.canvas = canvas
        self.tempMaze = m.Maze(groundTruth.size)
        self.canvas.delete("all")


    def runBot(self):
        bots = []
        paths = [[] for i in range(self.no_bot)]
        visisted = [[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.no_bot):
            r = ran.randint(0, self.size-1)
            c = ran.randint(0, self.size-1)
            while visisted[r][c]:
                r = ran.randint(0, self.size-1)
                c = ran.randint(0, self.size-1)
            bots.append(b.bot(self.canvas, 0, 0, self.size-1, self.size-1, 10+self.cellWidth*c+4, 10+self.cellHeight*r+4, 10+self.cellHeight*(c+1)-4, 10+self.cellHeight*(r+1)-4, fill='black'))
            paths[i].append([r,c,-1])
            visisted[r][c] = 1
            self.updateTempMaze(r, c)


        stop = False
        end = [False for i in range(self.no_bot)]
        overlap = self.overlapFlag.get()
        while not stop:
            stop = True
            for i in range(self.no_bot):
                if not end[i]:
                    r = paths[i][-1][0]
                    c = paths[i][-1][1]
                    move = False
                    if ((overlap and r>0) or (not overlap and r>bots[i].minr)) and self.tempGrid[r][c].top == 0 and visisted[r-1][c] == 0:
                        bots[i].move(0, -self.cellHeight)
                        r = r - 1
                        paths[i].append([r,c,2])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and r<self.size-1) or (not overlap and r<bots[i].maxr)) and self.tempGrid[r][c].bottom == 0 and visisted[r+1][c] == 0:
                        bots[i].move(0, self.cellHeight)
                        r = r + 1
                        paths[i].append([r,c,0])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and c>0) or (not overlap and c>bots[i].minc)) and self.tempGrid[r][c].left == 0 and visisted[r][c-1] == 0:
                        bots[i].move(-self.cellWidth, 0)
                        c = c - 1
                        paths[i].append([r,c,1])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    elif ((overlap and c<self.size-1) or (not overlap and c<bots[i].maxc)) and self.tempGrid[r][c].right == 0 and visisted[r][c+1] == 0:
                        bots[i].move(self.cellWidth, 0)
                        c = c + 1
                        paths[i].append([r,c,3])
                        visisted[r][c] = 1
                        self.updateTempMaze(r, c)
                        move = True
                    if not move:
                        prev = paths[i][-1][2]
                        if prev == 0:
                            bots[i].move(0, -self.cellHeight)
                        elif prev == 1:
                            bots[i].move(self.cellWidth, 0)
                        elif prev == 2:
                            bots[i].move(0, self.cellHeight)
                        elif prev == 3:
                            bots[i].move(-self.cellWidth, 0)
                        del paths[i][-1]
                        if not paths[i]:
                            end[i] = True
                for i in range(4):
                    if not end[i]:
                        stop = False
                        break

        for i in range(self.no_bot):
            print paths[i]
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if visisted[i][j]:
                    count += 1

        print('Explore completed')
        print('Cell explored: ' + str(count) + '/' + str(self.size*self.size))

    def updateTempGrid(self, r, c):
        self.tempMaze.grid[r][c].top = self.groundTruth.grid[r][c].top
        self.tempMaze.grid[r][c].bottom = self.groundTruth.grid[r][c].bottom
        self.tempMaze.grid[r][c].left = self.groundTruth.grid[r][c].left
        self.tempMaze.grid[r][c].right = self.groundTruth.grid[r][c].right
        if self.grid[r][c].top == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
        if self.grid[r][c].right == 1:
            self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.grid[r][c].bottom == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.grid[r][c].left == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))
