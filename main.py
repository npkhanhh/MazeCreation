__author__ = 'Khanh'
import graphicgame as gg
import graphic as g
import sys

if len(sys.argv) == 2:
    mazeSize = int(sys.argv[1])
else:
    mazeSize = 50

canvasWidth = 820
canvasHeight = 820
sys.setrecursionlimit(100000)

gui = g.GUI(canvasWidth, canvasHeight, mazeSize)
gui.createWindow()
gui.run()

