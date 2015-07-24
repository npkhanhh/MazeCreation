import botHelper as bh
import Maze as m

no_bot = [2, 5, 10, 20]
algo = ['Backtracker', 'Kruskal']
numberOfFile = 5

maze = m.Maze()
maze.load('TestMazes\\test' + '-' + str(100) + '-' + str(algo[0]) + '-' + str(0) + '.txt')

for nb in no_bot:
    for i in range(numberOfFile):
        bots = bh.botHelper(nb, maze, 'Region')
        bots.runBot()

        bots = bh.botHelper(nb, maze, 'Random')
        bots.runBot()

