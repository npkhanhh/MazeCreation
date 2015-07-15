from FindSolution import FindSolution
from RegionSolver_FW import RegionSolver_FW
#from FloydWarshallImpl import FloydWarshallImpl
__author__ = 'Khanh'
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import createAlgorithm as ca
import solveAlgorithm as sa
from PathConnector import PathConnector
import sys
import bot as b
from RegionSolver import RegionSolver
import threading
import random as ran

#### Some global variables
noPathString = 'Number of paths: '
noDEString = 'Number of deadends: '
shortestPathString = 'Shortest path length: '
defaultCellsize = 5
color = ['#00ff00', '#ff8000', '#eb3849', '#0080ff']

class Cell:
    def __init__(self, *args, **kwargs):
        if args and args[0] == 0:
            self.top = 0
            self.right = 0
            self.bottom = 0
            self.left = 0
        else:
            self.top = 1
            self.right = 1
            self.bottom = 1
            self.left = 1

class GUI:
    def __init__(self, w, h, size):
        self.master = tk.Tk()
        self.w = w
        self.h = h
        self.size = size
        self.cellWidth = (w - 20)/size
        self.cellHeight = (h - 20)/size
        self.de = []

        self.no_path = 0
        self.path_list=[]
        self.marked=[]
        self.shortestPathLength = self.size*self.size+1
        self.algoName = tk.StringVar()
        self.algoName.set('Backtracker')
        self.noPath = tk.StringVar()
        self.noPath.set(noPathString)
        self.noDE = tk.StringVar()
        self.noDE.set(noDEString)
        self.shortestPath = tk.StringVar()
        self.shortestPath.set(shortestPathString)
        self.choices = ['Backtracker', 'Recursive Backtracker', 'Kruskal']

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

        self.sizeString = tk.StringVar()
        self.sizeString.set('Size:')
        self.zoomString = tk.StringVar()
        self.zoomString.set('Zoom')

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
        self.zoneButton = tk.Checkbutton(self.master, text="Zone", variable=self.zoneFlag, command=self.draw)
        self.regionButton = tk.Checkbutton(self.master, text="Region", variable=self.regionFlag, command=self.draw)

        self.zoomInButton = tk.Button(self.master, text="+", command=self.zoomIn)
        self.zoomOutButton = tk.Button(self.master, text = "-", command=self.zoomOut)

        self.runButton = tk.Button(self.master, text="Run Bot", command=self.runBot)
        self.overlapButton = tk.Checkbutton(self.master, text="Allowed overlap", variable=self.overlapFlag)

        self.pathText = tk.Label(self.master, textvariable=self.noPath)
        self.deadEndText = tk.Label(self.master, textvariable=self.noDE)
        self.shortestPathText = tk.Label(self.master, textvariable=self.shortestPath)
        self.zoomText = tk.Label(self.master, textvariable=self.zoomString)
        self.sizeText = tk.Label(self.master, textvariable=self.sizeString)

        self.canvas.bind("<Button-1>", lambda event, arg="remove": self.editWall(event, arg))
        self.canvas.bind("<Button-3>", lambda event, arg="add": self.editWall(event, arg))
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
        self.sizeEntry.insert(0, str(self.size))
        self.createButton.grid(row=4, column=1, columnspan=3)
        self.menu.grid(row=5, column=1, columnspan=3)
        self.solveButton.grid(row=6, column=1, columnspan=3)
        self.divideZoneButton.grid(row=7, column=1, columnspan=3)

        self.saveButton.grid(row=8, column=1, columnspan=3)
        self.loadButton.grid(row=9, column=1, columnspan=3)

        self.gridButton.grid(row=10, column=1, columnspan=3)
        self.solutionButton.grid(row=11, column=1, columnspan=3)
        self.deadEndButton.grid(row=12, column=1, columnspan=3)
        self.zoneButton.grid(row=13, column=1, columnspan=3)
        self.regionButton.grid(row=14, column=1, columnspan=3)

        self.zoomInButton.grid(row=15, column=1)
        self.zoomText.grid(row=15, column=2)
        self.zoomOutButton.grid(row=15, column=3)

        self.botEntry.grid(row=16, column=1, columnspan=3)
        self.botEntry.insert(0, '0')
        self.runButton.grid(row=17, column=1, columnspan=3)
        self.overlapButton.grid(row=18, column=1, columnspan=3)

    
    
    def doHuysStuff(self):
        # TODO: use bots to explore maze 
        ########## Explore ##########
        nRegion = 2
        regionSize = self.size / nRegion
        self.regionMap = [[[] for x in range(nRegion)] for y in range(nRegion)]
        """lock = threading.Lock()
        threads = []
        for i in range(nRegion):
            for j in range(nRegion):
                regSolver = RegionSolver(self.grid, i*regionSize, j*regionSize, (j+1)*regionSize, (i+1)*regionSize, i, j, self.regionMap, lock)
                threads.append(regSolver)
                regSolver.start()
        
        for t in threads:
            t.join()

        print(self.regionMap)"""
        #############################################################################################
        #self.setupTest1()
        deMap = [[[] for x in range(nRegion)] for y in range(nRegion)]
        lock = threading.Lock()
        threads = []
        for i in range(nRegion):
            for j in range(nRegion):
                regSolver = RegionSolver_FW(self.grid, [i*regionSize, (i+1)*regionSize, j*regionSize, (j+1)*regionSize], i, j, self.regionMap, deMap, lock)
                threads.append(regSolver)
                regSolver.start()
        
        for t in threads:
            t.join()

        print "Path Map\n"
        print(self.regionMap)
        print "\nDeadend Map\n"
        print(deMap)
        
        #fw = FloydWarshallImpl(self.regionMap, deMap, nRegion)
        
        #############################################################################################




    def createMaze(self):
        algo = self.algoName.get()
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        self.size = int(self.sizeEntry.get())
        self.cellWidth = (self.w - 20)/self.size
        if self.cellWidth < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*self.size + 20, defaultCellsize*self.size + 20))
            self.cellWidth = defaultCellsize
        self.cellHeight = (self.h - 20)/self.size
        if self.cellHeight < defaultCellsize:
            self.canvas.config(scrollregion=(0, 0, defaultCellsize*self.size + 20, defaultCellsize*self.size + 20))
            self.cellHeight = defaultCellsize
        self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
        if algo == 'Recursive Backtracker':
            self.grid = ca.recursiveBacktracker(self.grid, self.size)
        elif algo == 'Backtracker':
            self.grid = ca.backtracker(self.grid, self.size)
        elif algo == 'Kruskal':
            self.grid = ca.kruskal(self.grid, self.size)
        self.resetGrid()

        
        self.doHuysStuff()
        self.draw()


    def solveMaze(self):
        # Solve maze by using explored paths
        start = [4, 4]
        goal = [0, 4]
        # TODO: set the number of region before exploring maze
        nRegion = 2
        FindSolution(self.grid, self.regionMap, nRegion, self.size, start, goal)
        
#         self.path_list = sa.dfs(self.grid, self.size)
#         self.draw()
#         self.no_path = len(self.path_list)
#         for i in range(len(self.path_list)):
#             if len(self.path_list[i]) < self.shortestPathLength  :
#                 self.shortestPathLength = len(self.path_list[i])
#         self.noPath.set(noPathString + str(self.no_path))
#         if self.no_path != 0:
#             self.shortestPath.set(shortestPathString + str(self.shortestPathLength))
#         else:
#             self.shortestPath.set(shortestPathString)
        #print self.path_list

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
        if self.gridFlag.get():
            self.drawGrid(1)


    def drawGrid(self, flag):
        if flag:
            for r in range(self.size):
                for c in range(self.size):
                    if self.grid[r][c].top == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
                    if self.grid[r][c].right == 1:
                        self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                    if self.grid[r][c].bottom == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                    if self.grid[r][c].left == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))
        else:
            for r in range(self.size):
                for c in range(self.size):
                    if self.tempGrid[r][c].top == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
                    if self.tempGrid[r][c].right == 1:
                        self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                    if self.tempGrid[r][c].bottom == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
                    if self.tempGrid[r][c].left == 1:
                        self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))

    def drawSolution(self, mode):
        #if mode == 0:
        #    outColor = 'green'
        #else:
        #    outColor = 'black'
        #outColor = 'green'
        for i in range(len(self.path_list)):
            path = self.path_list[i]
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

    def drawRegionMap(self):
        for i in range(len(self.regionMap)):
            for j in range(len(self.regionMap[i])):
                for k in range(len(self.regionMap[i][j])):
                    self.drawPath(self.regionMap[i][j][k], color[i%len(color)+1])

    def divide(self):
        self.marked = sa.dfsMarker(self.grid, self.size)
        self.draw()

    #function to help with debugging
    def printGrid(self):
        for i in range(self.size):
            for j in range(self.size):
                sys.stdout.write(str(self.grid[i][j].top))
                sys.stdout.write(str(self.grid[i][j].right))
                sys.stdout.write(str(self.grid[i][j].bottom))
                sys.stdout.write(str(self.grid[i][j].left))
                sys.stdout.write(" ")
            print("")

    def run(self):
        self.master.mainloop()

    def deadEndCount(self):
        t = 0
        for i in range(self.size):
            for j in range(self.size):
                temp = self.grid[i][j]
                if temp.top + temp.right + temp.bottom + temp.left == 3:
                    if (i!=0 or j!=0) and (i!=self.size-1 or j!=self.size-1):
                        t += 1
                        self.de.append([i, j])


    def resetGrid(self):
        self.no_path = 0
        self.shortestPathLength = self.size*self.size+1
        self.de = []
        self.canvas.delete(tk.ALL)
        self.deadEndCount()
        self.path_list=[]
        self.noDE.set(noDEString + str(len(self.de)))
        self.noPath.set(noPathString)
        self.shortestPath.set(shortestPathString)

    def saveGrid(self):
        fileName = raw_input("Input file name to save: ")
        f = open(fileName, 'w')
        f.write(str(self.size) + "\n")
        for i in range(self.size):
            for j in range(self.size):
                f.write(str(self.grid[i][j].top))
                f.write(str(self.grid[i][j].right))
                f.write(str(self.grid[i][j].bottom))
                f.write(str(self.grid[i][j].left))
                f.write(" ")
            f.write("\n")

    def loadGrid(self):
        fileName = raw_input("Input file name to load: ")
        f = open(fileName, 'r')
        self.size = int(f.readline())
        self.sizeEntry.insert(0, str(self.size))
        self.cellWidth = (self.w - 20)/self.size
        self.cellHeight = (self.h - 20)/self.size
        self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            s = f.readline()
            for j in range(self.size):
                self.grid[i][j].top = int(s[j*5])
                self.grid[i][j].right = int(s[j*5+1])
                self.grid[i][j].bottom = int(s[j*5+2])
                self.grid[i][j].left = int(s[j*5+3])
        self.resetGrid()
        self.draw()

    def drawDeadend(self):
        for i in range(len(self.de)):
            r = self.de[i][0]
            c = self.de[i][1]
            self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='red', outline='red')

    def drawZone(self):
        if(self.marked != []):
            for r in range(self.size):
                for c in range(self.size):
                    if self.marked[r][c] == 1:
                        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#eb3849', outline='#eb3849')
                    elif self.marked[r][c] == 2:
                        self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='#1e5cdf', outline='#1e5cdf')


    def editWall(self, event, mode):
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
        #print(pos, r, c)
        if mode == "remove":
            action = 0
        else:
            action = 1
        if r > 0 and pos == 0:
            self.grid[r][c].top = action
            self.grid[r-1][c].bottom = action
        elif c < self.size - 1  and pos == 1:
            self.grid[r][c].right = action
            self.grid[r][c+1].left = action
        elif r<self.size-1 and pos == 2:
            self.grid[r][c].bottom = action
            self.grid[r+1][c].top = action
        elif c<self.size-1 and pos == 3:
            self.grid[r][c].left = action
            self.grid[r][c-1].right = action
        self.resetGrid()
        self.draw()

    def zoomIn(self):
        self.cellWidth+=1
        self.cellHeight+=1
        self.canvas.config(scrollregion=(0, 0, self.cellWidth*self.size + 20, self.cellHeight*self.size + 20))
        self.draw()


    def zoomOut(self):
        if self.cellWidth > 1 and self.cellHeight > 1:
            self.cellWidth-=1
            self.cellHeight-=1
            self.canvas.config(scrollregion=(0, 0, self.cellWidth*self.size + 20, self.cellHeight*self.size + 20))
            self.draw()

    def runBot(self):
        self.tempGrid = [[Cell(0) for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            self.tempGrid[0][i].top = 1
            self.tempGrid[self.size-1][i].bottom = 1
            self.tempGrid[i][0].left = 1
            self.tempGrid[i][self.size-1].right = 1
        self.canvas.delete(tk.ALL)

        no_bot = int(self.botEntry.get())
        bots = []
        paths = [[] for i in range(no_bot)]
        visisted = [[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(no_bot):
            r = ran.randint(0, self.size-1)
            c = ran.randint(0, self.size-1)
            while visisted[r][c]:
                r = ran.randint(0, self.size-1)
                c = ran.randint(0, self.size-1)
            bots.append(b.bot(self.canvas, 0, 0, self.size-1, self.size-1, 10+self.cellWidth*c+4, 10+self.cellHeight*r+4, 10+self.cellHeight*(c+1)-4, 10+self.cellHeight*(r+1)-4, fill='black'))
            paths[i].append([r,c,-1])
            visisted[r][c] = 1
            self.updateTempGrid(r, c)

        self.drawGrid(0)

        stop = False
        end = [False for i in range(no_bot)]
        overlap = self.overlapFlag.get()
        while not stop:
            stop = True
            for i in range(no_bot):
                if not end[i]:
                    r = paths[i][-1][0]
                    c = paths[i][-1][1]
                    move = False
                    if ((overlap and r>0) or (not overlap and r>bots[i].minr)) and self.tempGrid[r][c].top == 0 and visisted[r-1][c] == 0:
                        bots[i].move(0, -self.cellHeight)
                        r = r - 1
                        paths[i].append([r,c,2])
                        visisted[r][c] = 1
                        self.updateTempGrid(r, c)
                        move = True
                    elif ((overlap and r<self.size-1) or (not overlap and r<bots[i].maxr)) and self.tempGrid[r][c].bottom == 0 and visisted[r+1][c] == 0:
                        bots[i].move(0, self.cellHeight)
                        r = r + 1
                        paths[i].append([r,c,0])
                        visisted[r][c] = 1
                        self.updateTempGrid(r, c)
                        move = True
                    elif ((overlap and c>0) or (not overlap and c>bots[i].minc)) and self.tempGrid[r][c].left == 0 and visisted[r][c-1] == 0:
                        bots[i].move(-self.cellWidth, 0)
                        c = c - 1
                        paths[i].append([r,c,1])
                        visisted[r][c] = 1
                        self.updateTempGrid(r, c)
                        move = True
                    elif ((overlap and c<self.size-1) or (not overlap and c<bots[i].maxc)) and self.tempGrid[r][c].right == 0 and visisted[r][c+1] == 0:
                        bots[i].move(self.cellWidth, 0)
                        c = c + 1
                        paths[i].append([r,c,3])
                        visisted[r][c] = 1
                        self.updateTempGrid(r, c)
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
            self.master.update()
            self.master.after(100)

        for i in range(no_bot):
            print paths[i]
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if visisted[i][j]:
                    count += 1

        print('Explore completed')
        print('Cell explored: ' + str(count) + '/' + str(self.size*self.size))

    def updateTempGrid(self, r, c):
        self.tempGrid[r][c].top = self.grid[r][c].top
        self.tempGrid[r][c].bottom = self.grid[r][c].bottom
        self.tempGrid[r][c].left = self.grid[r][c].left
        self.tempGrid[r][c].right = self.grid[r][c].right
        if self.grid[r][c].top == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*r)
        if self.grid[r][c].right == 1:
            self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.grid[r][c].bottom == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*(r+1), 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1))
        if self.grid[r][c].left == 1:
            self.canvas.create_line(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*c, 10+self.cellHeight*(r+1))



