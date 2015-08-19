import botHelper as bh
import Maze as m
from globalGroundTruth import globalGroundTruth as gg

no_bot = [2, 5, 10, 20]
mazeSize = [10, 20, 50, 100, 200, 500]
algo = ['Backtracker', 'Kruskal']
numberOfDrop = 1

maze = m.Maze()

for ms in [50]:
#     maze.load('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[0]) + '-' + str(0) + '.txt')
    for j in [5]:
        for i in range(numberOfDrop):
            bots = bh.botHelper(j, maze, 'Region')
            bots.runBot()

#     for j in range(2,8):
#         for i in range(numberOfDrop):
#             bots = bh.botHelper(j, maze, 'Random')
#             bots.runBot()

