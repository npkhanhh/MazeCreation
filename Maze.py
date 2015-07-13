import Cell as c
import createAlgorithm as ca
import solveAlgorithm as sa
import sys

class Maze:
    def __init__(self, size):
        self.size = size
        # self.cellWidth = (w - 20)/size
        # self.cellHeight = (h - 20)/size
        self.de = []
        self.grid = [[c.Cell() for i in range(self.size)] for j in range(self.size)]
        self.no_path = 0
        self.path_list=[]
        self.marked=[]
        self.shortestPathLength = self.size*self.size+1
        self.start = [0, 0]
        self.end = [size-1, size-1]

    def create(self, algo, size):
        self.size = size
        self.grid = [[c.Cell() for i in range(self.size)] for j in range(self.size)]
        if algo == 'Recursive Backtracker':
            self.grid = ca.recursiveBacktracker(self.grid, self.size)
        elif algo == 'Backtracker':
            self.grid = ca.backtracker(self.grid, self.size)
        elif algo == 'Kruskal':
            self.grid = ca.kruskal(self.grid, self.size)
        self.resetGrid()

    def resetGrid(self):
        self.no_path = 0
        self.shortestPathLength = self.size*self.size+1
        self.de = []
        self.deadEndCount()
        self.path_list=[]

    def deadEndCount(self):
        self.no_de = 0
        for i in range(self.size):
            for j in range(self.size):
                temp = self.grid[i][j]
                if temp.top + temp.right + temp.bottom + temp.left == 3:
                    if (i!=0 or j!=0) and (i!=self.size-1 or j!=self.size-1):
                        self.no_de += 1
                        self.de.append([i, j])


    def solve(self):
        self.path_list = sa.dfs(self.grid, self.size)
        self.no_path = len(self.path_list)
        for i in range(len(self.path_list)):
            if len(self.path_list[i]) < self.shortestPathLength:
                self.shortestPathLength = len(self.path_list[i])

    def divide(self):
        self.marked = sa.dfsMarker(self.grid, self.size)

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

    def save(self, filename):
        f = open(filename, 'w')
        f.write(str(self.size) + "\n")
        for i in range(self.size):
            for j in range(self.size):
                f.write(str(self.grid[i][j].top))
                f.write(str(self.grid[i][j].right))
                f.write(str(self.grid[i][j].bottom))
                f.write(str(self.grid[i][j].left))
                f.write(" ")
            f.write("\n")

    def load(self, filename):
        f = open(filename, 'r')
        self.size = int(f.readline())
        self.grid = [[c.Cell() for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            s = f.readline()
            for j in range(self.size):
                self.grid[i][j].top = int(s[j*5])
                self.grid[i][j].right = int(s[j*5+1])
                self.grid[i][j].bottom = int(s[j*5+2])
                self.grid[i][j].left = int(s[j*5+3])
        self.resetGrid()
