__author__ = 'Khanh'
import Tkinter as tk
import createAlgorithm as ca
import solveAlgorithm as sa
import sys

#### Some global variables
noPathString = 'Number of paths: '
noDEString = 'Number of deadends: '
shortestPathString = 'Shortest path length: '

class Cell:
    def __init__(self):
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
        self.num_de = 0
        self.no_path = 0
        self.shortestPathLength = sys.maxint
        self.algoName = tk.StringVar()
        self.algoName.set('Recursive Backtracker')
        self.noPath = tk.StringVar()
        self.noPath.set(noPathString)
        self.noDE = tk.StringVar()
        self.noDE.set(noDEString)
        self.shortestPath = tk.StringVar()
        self.shortestPath.set(shortestPathString)
        self.choices = ['Recursive Backtracker', 'Kruskal']
        self.gridcon = 1
        self.solutioncon = 1

    def createWindow(self):
        self.canvas = tk.Canvas(self.master, width=self.w, height=self.h)
        self.menu = tk.OptionMenu(self.master, self.algoName, *self.choices)
        self.createButton = tk.Button(self.master, text="Create", command=self.createMaze)
        self.solveButton = tk.Button(self.master, text="Solve", command=self.solveMaze)
        self.saveButton = tk.Button(self.master, text="Save", command=self.saveGrid)
        self.loadButton = tk.Button(self.master, text="Load", command=self.loadGrid)
        self.gridButton = tk.Button(self.master, text="Grid", command=self.gridControl)
        self.solutionButton = tk.Button(self.master, text="Solution", command=self.solutionControl)
        self.pathText = tk.Label(self.master, textvariable=self.noPath)
        self.deadEndText = tk.Label(self.master, textvariable=self.noDE)
        self.shortestPathText = tk.Label(self.master, textvariable=self.shortestPath)

        self.canvas.grid(row=0, column=0, rowspan=25)
        self.deadEndText.grid(row=0, column=1)
        self.pathText.grid(row=1, column=1)
        self.shortestPathText.grid(row=2, column=1)
        self.createButton.grid(row=3, column=1)
        self.menu.grid(row=4, column=1)
        self.solveButton.grid(row=5, column=1)
        self.saveButton.grid(row=6, column=1)
        self.loadButton.grid(row=7, column=1)
        self.gridButton.grid(row=8, column =1)
        self.solutionButton.grid(row=9, column =1)


    def createMaze(self):
        algo = self.algoName.get()
        self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
        self.num_de = 0
        self.no_path = 0
        self.shortestPathLength = sys.maxint
        if algo == 'Recursive Backtracker':
            self.grid = ca.recursiveBacktracker(self.grid, self.size)
        elif algo == 'Kruskal':
            self.grid = ca.kruskal(self.grid, self.size)
        self.canvas.delete(tk.ALL)
        self.deadEndCount()
        self.noDE.set(noDEString + str(self.num_de))
        self.noPath.set(noPathString)
        self.shortestPath.set(shortestPathString)
        self.drawGrid()

    def solveMaze(self):
        self.path_list = sa.dfs(self.grid, self.size)
        self.drawSolution()
        self.drawGrid()
        self.no_path = len(self.path_list)
        for i in range(len(self.path_list)):
            if len(self.path_list[i]) < self.shortestPathLength  :
                self.shortestPathLength = len(self.path_list[i])
        self.noPath.set(noPathString + str(self.no_path))
        if self.no_path != 0:
            self.shortestPath.set(shortestPathString + str(self.shortestPathLength))
        else:
             self.shortestPath.set(shortestPathString)
        #print self.path_list

    def drawGrid(self):
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

    def drawSolution(self):
        for i in range(len(self.path_list)):
            path = self.path_list[i]
            for j in range(len(path)):
                r = path[j][0]
                c = path[j][1]
                self.canvas.create_rectangle(10+self.cellWidth*c, 10+self.cellHeight*r, 10+self.cellWidth*(c+1), 10+self.cellHeight*(r+1), fill='green', outline='green')

    #function to help with debugging
    def printGrid(self):
        for i in range(self.size):
            for j in range(self.size):
                sys.stdout.write(str(self.grid[i][j].top))
                sys.stdout.write(str(self.grid[i][j].right))
                sys.stdout.write(str(self.grid[i][j].bottom))
                sys.stdout.write(str(self.grid[i][j].left))
                sys.stdout.write(" ")
            print

    def run(self):
        self.master.mainloop()

    def deadEndCount(self):
        for i in range(self.size):
            for j in range(self.size):
                temp = self.grid[i][j]
                if temp.top + temp.right + temp.bottom + temp.left == 3:
                    if (i!=0 or j!=0) and (i!=self.size-1 or j!=self.size-1):
                        self.num_de += 1

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
        self.canvas.delete(tk.ALL)
        self.deadEndCount()
        self.noDE.set(noDEString + str(self.num_de))
        self.noPath.set(noPathString)
        self.shortestPath.set(shortestPathString)
        self.drawGrid()

    def gridControl(self):
        self.canvas.delete(tk.ALL)
        if self.solutioncon == 1:
            self.drawSolution()
        if self.gridcon == 1:
            self.gridcon = 0
        else:
            self.drawGrid()
            self.gridcon = 1


    def solutionControl(self):
        self.canvas.delete(tk.ALL)
        if self.solutioncon == 1:
            self.solutioncon = 0
        else:
            self.drawSolution()
            self.solutioncon = 1
        if self.gridcon == 1:
            self.drawGrid()

