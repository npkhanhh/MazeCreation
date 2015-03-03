__author__ = 'Khanh'
import graphic
import sys


mazeSize = 50
canvasWidth = 820
canvasHeight = 820
sys.setrecursionlimit(10000)

gui = graphic.GUI(820, 820, mazeSize)
gui.createWindow()
gui.run()

