import Maze as m

mazeSize = [10, 20, 50, 100, 200, 500]
numberOfFile = 5
algo = ['Backtracker', 'Kruskal']

for ms in mazeSize:
    for i in range(numberOfFile):
        maze = m.Maze(ms, algo[0])
        maze.save('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[0]) + '-' + str(i) + '.txt')

        maze = m.Maze(ms, algo[1])
        maze.save('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[1]) + '-' + str(i) + '.txt')

print('Create completed')

