__author__ = 'Khanh'
import graphic
import sys


size = 5
canvasWidth = 820
canvasHeight = 820
sys.setrecursionlimit(10000)

gui = graphic.GUI(820, 820, size)
gui.createWindow()
gui.run()

