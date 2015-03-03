__author__ = 'Khanh'
import Tkinter as tk
import createAlgorithm as ca
import solveAlgorithm as sa
import sys
#def renderGrid(canvas, width, height, grid):

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
        self.var = tk.StringVar(self.master)
        self.var.set('Recursive Backtracker')
        self.choices = ['Recursive Backtracker', 'Kruskal']

    def createWindow(self):
        self.canvas = tk.Canvas(self.master, width=self.w, height=self.h)
        self.menu = tk.OptionMenu(self.master, self.var, *self.choices)
        self.createButton = tk.Button(self.master, text="Create", command=self.createMaze)
        self.solveButton = tk.Button(self.master, text="Solve", command=self.solveMaze)
        self.canvas.pack()
        self.createButton.pack()
        self.menu.pack()
        self.solveButton.pack()

    def createMaze(self):
        algo = self.var.get()
        self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
        if algo == 'Recursive Backtracker':
            grid = ca.recursiveBacktracker(self.grid, self.size)
        elif algo == 'Kruskal':
            grid = ca.kruskal(self.grid, self.size)
        self.canvas.delete(tk.ALL)
        self.drawGrid()

    def solveMaze(self):
        path_list = sa.bfs(self.grid, self.size)
        print path_list

    def drawGrid(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c].top == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellWidth*r, 10+self.cellWidth*(c+1), 10+self.cellWidth*r)
                if self.grid[r][c].right == 1:
                    self.canvas.create_line(10+self.cellWidth*(c+1), 10+self.cellWidth*r, 10+self.cellWidth*(c+1), 10+self.cellWidth*(r+1))
                if self.grid[r][c].bottom == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellWidth*(r+1), 10+self.cellWidth*(c+1), 10+self.cellWidth*(r+1))
                if self.grid[r][c].left == 1:
                    self.canvas.create_line(10+self.cellWidth*c, 10+self.cellWidth*r, 10+self.cellWidth*c, 10+self.cellWidth*(r+1))

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
        num_de = 0
        for i in range(self.size):
            for j in range(self.size):
                temp = self.grid[i][j]
                if temp.top + temp.right + temp.bottom + temp.left == 3:
                    if (i!=0 or j!=0) and (i!=self.size-1 or j!=self.size-1):
                        num_de += 1
        return num_de
