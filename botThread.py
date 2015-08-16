

import threading

class bot(threading.Thread):
    def __init__(self, startRow, startCol, lock, groundTruth, maze, visited):
        super(bot,self).__init__()
        self.startRow = startRow
        self.startCol = startCol
        self.lock = lock
        self.groundTruth = groundTruth
        self.maze = maze
        self.visited = visited
        self.path = [[startRow, startCol]]

    def run(self):
        r = self.path[-1][0]
        c = self.path[-1][1]
        while self.path:
            move = False
            if self.groundTruth.grid[r][c].top == 0 and self.visited[r-1][c] != 1:
                self.path.append([r-1, c])
                move = True
                r = r - 1
                self.lock.acquire()
                self.visited[r][c] = 1
                self.updateTempMaze(r,c)
                self.lock.release()
            elif self.groundTruth.grid[r][c].right == 0 and self.visited[r][c+1] != 1:
                self.path.append([r, c+1])
                move = True
                c = c + 1
                self.lock.acquire()
                self.visited[r][c] = 1
                self.updateTempMaze(r,c)
                self.lock.release()
            elif self.groundTruth.grid[r][c].bottom == 0 and self.visited[r+1][c] != 1:
                self.path.append([r+1, c])
                move = True
                r = r + 1
                self.lock.acquire()
                self.visited[r][c] = 1
                self.updateTempMaze(r,c)
                self.lock.release()
            elif self.groundTruth.grid[r][c].left == 0 and self.visited[r][c-1] != 1:
                self.path.append([r, c-1])
                move = True
                c = c - 1
                self.lock.acquire()
                self.visited[r][c] = 1
                self.updateTempMaze(r,c)
                self.lock.release()
            if not move:
                del self.path[-1]
                if self.path:
                    r = self.path[-1][0]
                    c = self.path[-1][1]

    def updateTempMaze(self, r, c):
        self.maze.grid[r][c].top = self.groundTruth.grid[r][c].top
        self.maze.grid[r][c].bottom = self.groundTruth.grid[r][c].bottom
        self.maze.grid[r][c].left = self.groundTruth.grid[r][c].left
        self.maze.grid[r][c].right = self.groundTruth.grid[r][c].right