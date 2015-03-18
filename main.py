__author__ = 'Khanh'
import graphic
import sys

if len(sys.argv) == 2:
    mazeSize = int(sys.argv[1])
else:
    mazeSize = 50

canvasWidth = 620
canvasHeight = 620
sys.setrecursionlimit(100000)

gui = graphic.GUI(canvasWidth, canvasHeight, mazeSize)
gui.createWindow()
gui.run()

