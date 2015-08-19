from FindSolution import FindSolution
import time
from constructLists import constructLists
import logging
__author__ = 'Khanh'
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import tkFileDialog as tkfd
from PathConnector import PathConnector
import sys
import bot as b
import threading
import random as ran
import Maze as m
import Utility as u
import tkMessageBox as tkmb

#### Some global variables
noPathString = 'Number of paths: '
noDEString = 'Number of deadends: '
shortestPathString = 'Shortest path length: '
defaultCellsize = 5
color = ['#00ff00', '#ff8000', '#eb3849', '#0080ff']

class GUI:
    def __init__(self, w, h, mazeSize):
        self.master = tk.Tk()
        self.master.wm_title("The Maze" +  u"\u2122")
        self.maze = None
        self.mazeSize = mazeSize 
        self.w = w
        self.h = h
        self.cellWidth = (w - 20)/mazeSize
        self.cellHeight = (h - 20)/mazeSize

        self.algoName = tk.StringVar()
        self.algoName.set('Backtracker')
        self.noPath = tk.StringVar()
        self.noPath.set(noPathString)
        self.noDE = tk.StringVar()
        self.noDE.set(noDEString)
        self.shortestPath = tk.StringVar()
        self.shortestPath.set(shortestPathString)
        self.choices = ['Backtracker', 'Recursive Backtracker', 'Kruskal']
        self.dropChoices = ['Region', 'Random']
        self.dropMode = tk.StringVar()
        self.dropMode.set('Region')

        self.gridFlag = tk.IntVar()
        self.gridFlag.set(1)
        self.solutionFlag = tk.IntVar()
        self.solutionFlag.set(1)
        self.deFlag = tk.IntVar()
        self.deFlag.set(0)
        self.zoneFlag = tk.IntVar()
        self.zoneFlag.set(0)
        self.regionFlag = tk.IntVar()
        self.regionFlag.set(0)
        self.overlapFlag = tk.IntVar()
        self.overlapFlag.set(1)
        self.startGoalFlag = tk.IntVar()
        self.startGoalFlag.set(1)

        self.sizeString = tk.StringVar()
        self.sizeString.set('Size:')
        self.zoomString = tk.StringVar()
        self.zoomString.set('Zoom')
        self.pause = False
        
        self.regionMap = []
        self.deMap = []
        self.nodeMap = []
        self.solution = []

    def createWindow(self):
        self.frame = tk.Frame(self.master, width = self.w, height=self.h)

        self.xscrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.yscrollbar = tk.Scrollbar(self.frame)
        self.canvas = tk.Canvas(self.frame, width=self.w, height=self.h, xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.menu = tk.OptionMenu(self.master, self.algoName, *self.choices)
        self.sizeEntry = tk.Entry(self.master)
        self.botEntry = tk.Entry(self.master)

        self.createButton = tk.Button(self.master, text="Create", command=self.createMaze)
        self.solveButton = tk.Button(self.master, text="Solve", command=self.solveMaze)
        self.saveButton = tk.Button(self.master, text="Save", command=self.saveGrid)
        self.loadButton = tk.Button(self.master, text="Load", command=self.loadGrid)
        self.divideZoneButton = tk.Button(self.master, text="Divide", command=self.divide)

        self.gridButton = tk.Checkbutton(self.master, text="Grid", variable=self.gridFlag, command=self.draw)
        self.solutionButton = tk.Checkbutton(self.master, text="Solution", variable=self.solutionFlag, command=self.draw)
        self.deadEndButton = tk.Checkbutton(self.master, text="Deadend", variable=self.deFlag, command=self.draw)
        self.startGoalButton = tk.Checkbutton(self.master, text="Start Goal", variable=self.startGoalFlag, command=self.draw)
        self.zoneButton = tk.Checkbutton(self.master, text="Zone", variable=self.zoneFlag, command=self.draw)
        self.regionButton = tk.Checkbutton(self.master, text="Region", variable=self.regionFlag, command=self.draw)

        self.zoomInButton = tk.Button(self.master, text="+", command=self.zoomIn)
        self.zoomOutButton = tk.Button(self.master, text = "-", command=self.zoomOut)

        self.runButton = tk.Button(self.master, text="Run Bot", command=self.runBot)
        self.overlapButton = tk.Checkbutton(self.master, text="Allowed overlap", variable=self.overlapFlag)
        self.pauseButton = tk.Button(self.master, text="Pause")
        self.pauseButton.bind("<Button-1>", self.pausePressed)
        self.master.bind("<space>", self.pausePressed)
        self.dropMenu = tk.OptionMenu(self.master, self.dropMode, *self.dropChoices)


        self.pathText = tk.Label(self.master, textvariable=self.noPath)
        self.deadEndText = tk.Label(self.master, textvariable=self.noDE)
        self.shortestPathText = tk.Label(self.master, textvariable=self.shortestPath)
        self.zoomText = tk.Label(self.master, textvariable=self.zoomString)
        self.sizeText = tk.Label(self.master, textvariable=self.sizeString)

        self.canvas.bind("<Button-1>", lambda event, arg="remove": self.editWall(event, arg))
        self.canvas.bind("<Button-3>", lambda event, arg="add": self.editWall(event, arg))
        self.canvas.bind("<Control-1>", self.setStart)
        self.canvas.bind("<Control-3>", self.setGoal)
        self.xscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.yscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas.grid(row=0, column=0, sticky=tk.NW)

        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

        self.frame.grid(row=0, column=0, rowspan=30)
        self.deadEndText.grid(row=0, column=1, columnspan=3)
        self.pathText.grid(row=1, column=1, columnspan=3)
        self.shortestPathText.grid(row=2, column=1, columnspan=3)
        self.sizeText.grid(row=3, column=1)
        self.sizeEntry.grid(row=3, column=2, columnspan=2)
        self.sizeEntry.insert(0, str(self.mazeSize))
        self.createButton.grid(row=4, column=1, columnspan=3)
        self.menu.grid(row=5, column=1, columnspan=3)
        self.solveButton.grid(row=6, column=1, columnspan=3)
        self.divideZoneButton.grid(row=7, column=1, columnspan=3)

        self.saveButton.grid(row=8, column=1, columnspan=3)
        self.loadButton.grid(row=9, column=1, columnspan=3)

        self.gridButton.grid(row=10, column=1, columnspan=3)
        self.solutionButton.grid(row=11, column=1, columnspan=3)
        self.startGoalButton.grid(row=12, column=1, columnspan=3)
        self.deadEndButton.grid(row=13, column=1, columnspan=3)
        self.zoneButton.grid(row=14, column=1, columnspan=3)
        self.regionButton.grid(row=15, column=1, columnspan=3)

        self.zoomInButton.grid(row=16, column=1)
        self.zoomText.grid(row=16, column=2)
        self.zoomOutButton.grid(row=16, column=3)

        self.botEntry.grid(row=17, column=1, columnspan=3)
        self.botEntry.insert(0, '0')
        self.dropMenu.grid(row=18, column=1, columnspan=3)
        self.runButton.grid(row=19, column=1, columnspan=3)
        self.overlapButton.grid(row=20, column=1, columnspan=3)
        self.pauseButton.grid(row=21, column=1, columnspan=3)

    
        

    def createMaze(self):
        algo = self.algoName.get()
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        size = int(self.sizeEntry.get())
        self.cellWidth = (self.w - 20)/size
        if self.cellWidth < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*size + 20, defaultCellsize*size + 20))
            self.cellWidth = defaultCellsize
        self.cellHeight = (self.h - 20)/size
        if self.cellHeight < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*size + 20, defaultCellsize*size + 20))
            self.cellHeight = defaultCellsize
        self.maze = m.Maze()
        self.maze.create(algo, size)
        self.updateInfo()

        
#         self.nRegion = constructLists(self.maze, self.regionMap, self.deMap, self.nodeMap)
        self.draw()
        #self.drawRegionMap()
        #self.drawDeadendPath()
        #self.drawGrid(self.maze)


    def solveMaze(self):
        startT = time.time()
#         self.solution = FindSolution(self.maze.grid, self.regionMap, self.deMap, self.nodeMap, self.nRegion, self.maze.size, self.maze.start, self.maze.goal)
        t = time.time() - startT
#         print "Solving time of regional method: {}".format(t)
        logging.info("Solving time of regional method: {}".format(t))
        self.maze.solve()
        self.draw()
        self.noPath.set(noPathString + str(self.maze.no_path))
        if self.maze.no_path != 0:
            self.shortestPath.set(shortestPathString + str(self.maze.shortestPathLength))
        else:
            self.shortestPath.set(shortestPathString)

    def drawDeadendPath(self):
        for i in range(len(self.deMap)):
            for j in range(len(self.deMap[i])):
                for k in range(len(self.deMap[i][j])):
                        self.drawPath(self.deMap[i][j][k], 'red')

    def draw(self):
        self.canvas.delete(tk.ALL)
        if self.zoneFlag.get():
            self.drawZone()
        if self.deFlag.get():
            self.drawDeadend()
        if self.regionFlag.get():
            self.drawRegionMap()
        if self.solutionFlag.get():
            self.drawSolution(1)
        if self.startGoalFlag.get():
            self.drawStartGoal()
        if self.gridFlag.get():
            self.drawGrid(self.maze)
        

    def drawGrid(self, maze):
        for r in range(maze.size):
            for c in range(maze.size):
                if maze.grid[r][c].top == 1 and maze.grid[r][c].right == 1 and maze.grid[r][c].bottom == 1 and maze.grid[r][c].left == 1:
                    continue
                if maze.grid[r][c].top == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
                if maze.grid[r][c].right == 1:
                    self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                if maze.grid[r][c].bottom == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                if maze.grid[r][c].left == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))

    def drawStartGoal(self):
        r = self.maze.start[0]
        c = self.maze.start[1]
        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#637ee9', outline='#637ee9')
        
        r = self.maze.goal[0]
        c = self.maze.goal[1]
        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#800080', outline='#800080')
    
    def drawSolution(self, mode):
        #if mode == 0:
        #    outColor = 'green'
        #else:
        #    outColor = 'black'
        #outColor = 'green'
        path_list = self.maze.path_list
#         path_list = [self.solution]
        for i in range(len(path_list)):
            path = path_list[i]
            for j in range(len(path)):
                r = path[j][0]
                c = path[j][1]
                if i == 0:
                    self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#00ff00', outline='#00ff00')
                elif i == 1:
                    self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#ff8000', outline='#ff8000')
                elif i == 2:
                    self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#0080ff', outline='#0080ff')
                else:
                    self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#e7ff00', outline='#e7ff00')

    def drawPath(self, path, color):
        for j in range(len(path)):
            r = path[j][0]
            c = path[j][1]
            self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill=color, outline=color)


    # def drawRegionMap(self):
    #     for i in range(len(self.regionMap)):
    #         for j in range(len(self.regionMap[i])):
    #             for k in range(len(self.regionMap[i][j])):
    #                     self.drawPath(self.regionMap[i][j][k], 'green')

    def divide(self):
        self.maze.divide()
        self.draw()

    def run(self):
        self.master.mainloop()

    def updateInfo(self):
        self.noDE.set(noDEString + str(self.maze.no_de))
        self.noPath.set(noPathString)
        self.shortestPath.set(shortestPathString)

    def saveGrid(self):
        filename = tkfd.asksaveasfilename(filetypes=[('txt files', '.txt'), ('all files', '.*')], defaultextension='.txt')
        self.maze.save(filename)

    def loadGrid(self):
        filename = tkfd.askopenfilename(filetypes=[('txt files', '.txt'), ('all files', '.*')], defaultextension='.txt')
        self.maze.load(filename)
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        size = self.maze.size
        self.sizeEntry.delete(0, 'end')
        self.sizeEntry.insert(0, str(size))
        self.cellWidth = (self.w - 20)/size
        if self.cellWidth < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*size + 20, defaultCellsize*size + 20))
            self.cellWidth = defaultCellsize
        self.cellHeight = (self.h - 20)/size
        if self.cellHeight < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*size + 20, defaultCellsize*size + 20))
            self.cellHeight = defaultCellsize
        self.updateInfo()
        self.draw()
#         self.nRegion = constructLists(self.maze, self.regionMap, self.deMap, self.nodeMap)

    def drawDeadend(self):
        for i in range(self.maze.no_de):
            r = self.maze.de[i][0]
            c = self.maze.de[i][1]
            self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='red', outline='red')

    def drawZone(self):
        if(self.maze.marked != []):
            for r in range(self.maze.size):
                for c in range(self.maze.size):
                    if self.maze.marked[r][c] == 1:
                        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#eb3849', outline='#eb3849')
                    elif self.maze.marked[r][c] == 2:
                        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#1e5cdf', outline='#1e5cdf')


    def editWall(self, event, mode):
        if not self.maze:
            return
        x = event.x - 10
        y = event.y - 10
        r = int(y / self.cellHeight)
        c = int(x / self.cellWidth)
        if abs(self.cellWidth*c-x) < abs(self.cellWidth*(c+1)-x):
            minx = abs(self.cellWidth*c-x)
            posx = 3
        else:
            minx = abs(self.cellWidth*(c+1)-x)
            posx = 1
        if abs(self.cellHeight*r-y) < abs(self.cellHeight*(r+1)-y):
            miny = abs(self.cellHeight*r-y)
            posy = 0
        else:
            miny = abs(self.cellHeight*(r+1)-y)
            posy = 2
        if minx<miny:
            pos = posx
        else:
            pos = posy
        if mode == "remove":
            action = 0
        else:
            action = 1
        if r > 0 and pos == 0:
            self.maze.grid[r][c].top = action
            self.maze.grid[r-1][c].bottom = action
        elif c < self.maze.size - 1  and pos == 1:
            self.maze.grid[r][c].right = action
            self.maze.grid[r][c+1].left = action
        elif r<self.maze.size-1 and pos == 2:
            self.maze.grid[r][c].bottom = action
            self.maze.grid[r+1][c].top = action
        elif c<self.maze.size-1 and pos == 3:
            self.maze.grid[r][c].left = action
            self.maze.grid[r][c-1].right = action
        self.maze.resetGrid()
        self.draw()

    def zoomIn(self):
        self.cellWidth+=1
        self.cellHeight+=1
        self.canvas.config(scrollregion=(0, 0, self.cellWidth*self.maze.size + 20, self.cellHeight*self.maze.size + 20))
        self.draw()


    def zoomOut(self):
        if self.cellWidth > 1 and self.cellHeight > 1:
            self.cellWidth-=1
            self.cellHeight-=1
            self.canvas.config(scrollregion=(0, 0, self.cellWidth*self.maze.size + 20, self.cellHeight*self.maze.size + 20))
            self.draw()

    def runBot(self):
        self.tempMaze = m.Maze(self.maze.size, -1)
        self.canvas.delete("all")
        size = self.maze.size
        self.no_bot = int(self.botEntry.get())
        self.bots = []
        self.paths = [[] for i in range(self.no_bot)]
        self.visisted = [[0 for i in range(size)] for j in range(size)]
        mode = self.dropMode.get()
        if mode == 'Random':
            for i in range(self.no_bot):
                r = ran.randint(0, size-1)
                c = ran.randint(0, size-1)
                while self.visisted[r][c]:
                    r = ran.randint(0, size-1)
                    c = ran.randint(0, size-1)
                self.bots.append(b.bot(self.canvas, 0, 0, size-1, size-1, 10+self.cellWidth*c+4, 10+self.cellHeight*r+4, 10+self.cellHeight*(c+1)-4, 10+self.cellHeight*(r+1)-4, fill='black'))
                self.paths[i].append([r,c,-1])
                self.visisted[r][c] = 1
                self.updateTempMaze(r, c)
        elif mode == 'Region':
            numberOfRows = u.findNearSquaredNumber(self.no_bot)
#             print(numberOfRows)
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
                    self.bots.append(b.bot(self.canvas, 0, 0, size-1, size-1, 10+self.cellWidth*c+4, 10+self.cellHeight*r+4, 10+self.cellHeight*(c+1)-4, 10+self.cellHeight*(r+1)-4, fill='black'))
                    self.paths[botcount].append([r,c,-1])
                    self.visisted[r][c] = 1
                    self.updateTempMaze(r, c)
                    botcount+=1
        self.drawGrid(self.tempMaze)

        self.stop = False
        end = [False for i in range(self.no_bot)]
        overlap = self.overlapFlag.get()
        while not self.stop:
            if not self.pause:
                self.stop = True
                for i in range(self.no_bot):
                    if not end[i]:
                        r = self.paths[i][-1][0]
                        c = self.paths[i][-1][1]
                        move = False
                        if ((overlap and r>0) or (not overlap and r>self.bots[i].minr)) and self.tempMaze.grid[r][c].top == 0 and self.visisted[r-1][c] == 0:
                            self.bots[i].move(0, -self.cellHeight)
                            r = r - 1
                            self.paths[i].append([r,c,2])
                            self.visisted[r][c] = 1
                            self.updateTempMaze(r, c)
                            move = True
                        elif ((overlap and r<size-1) or (not overlap and r<self.bots[i].maxr)) and self.tempMaze.grid[r][c].bottom == 0 and self.visisted[r+1][c] == 0:
                            self.bots[i].move(0, self.cellHeight)
                            r = r + 1
                            self.paths[i].append([r,c,0])
                            self.visisted[r][c] = 1
                            self.updateTempMaze(r, c)
                            move = True
                        elif ((overlap and c>0) or (not overlap and c>self.bots[i].minc)) and self.tempMaze.grid[r][c].left == 0 and self.visisted[r][c-1] == 0:
                            self.bots[i].move(-self.cellWidth, 0)
                            c = c - 1
                            self.paths[i].append([r,c,1])
                            self.visisted[r][c] = 1
                            self.updateTempMaze(r, c)
                            move = True
                        elif ((overlap and c<size-1) or (not overlap and c<self.bots[i].maxc)) and self.tempMaze.grid[r][c].right == 0 and self.visisted[r][c+1] == 0:
                            self.bots[i].move(self.cellWidth, 0)
                            c = c + 1
                            self.paths[i].append([r,c,3])
                            self.visisted[r][c] = 1
                            self.updateTempMaze(r, c)
                            move = True
                        if not move:
                            prev = self.paths[i][-1][2]
                            if prev == 0:
                                self.bots[i].move(0, -self.cellHeight)
                            elif prev == 1:
                                self.bots[i].move(self.cellWidth, 0)
                            elif prev == 2:
                                self.bots[i].move(0, self.cellHeight)
                            elif prev == 3:
                                self.bots[i].move(-self.cellWidth, 0)
                            del self.paths[i][-1]
                            if not self.paths[i]:
                                end[i] = True
                    for i in range(self.no_bot):
                        if not end[i]:
                            self.stop = False
                            break
                self.master.update()
                self.master.after(100)
            else:
                self.master.update()
                self.master.after(10)

#         for i in range(self.no_bot):
#             print self.paths[i]
        count = 0
        for i in range(size):
            for j in range(size):
                if self.visisted[i][j]:
                    count += 1

        print('Explore completed')
        print('Cell explored: ' + str(count) + '/' + str(size*size))
        
        tkmb.showinfo(None, "Explored completed")
        self.draw()


    def updateTempMaze(self, r, c):
        self.tempMaze.grid[r][c].top = self.maze.grid[r][c].top
        self.tempMaze.grid[r][c].bottom = self.maze.grid[r][c].bottom
        self.tempMaze.grid[r][c].left = self.maze.grid[r][c].left
        self.tempMaze.grid[r][c].right = self.maze.grid[r][c].right
        if self.tempMaze.grid[r][c].top == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
        if self.tempMaze.grid[r][c].right == 1:
            self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.tempMaze.grid[r][c].bottom == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.tempMaze.grid[r][c].left == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))

    def pausePressed(self, event):
        self.pause = not self.pause
#         print self.pause

    def setStart(self, event):
        if not self.maze:
            return
        x = event.x - 10
        y = event.y - 10
        r = int(y / self.cellHeight)
        c = int(x / self.cellWidth)
        self.maze.start = [r, c]
        print("Start is set at: " + str([r, c]))
        self.maze.resetGrid()
        self.draw()

    def setGoal(self, event):
        if not self.maze:
            return
        x = event.x - 10
        y = event.y - 10
        r = int(y / self.cellHeight)
        c = int(x / self.cellWidth)
        self.maze.goal = [r, c]
        print("Goal is set at: " + str([r, c]))
        self.maze.resetGrid()
        self.draw()