__author__ = 'Khanh'
import graphic as g
import newgraphic as ng
import Maze as m
import sys

if len(sys.argv) == 2:
    mazeSize = int(sys.argv[1])
else:
    mazeSize = 50

canvasWidth = 820
canvasHeight = 820
sys.setrecursionlimit(100000)

maze = m.Maze(mazeSize)
gui = ng.GUI(canvasWidth, canvasHeight, maze)
#gui = g.GUI(canvasWidth, canvasHeight, mazeSize)

gui.createWindow()
gui.run()

