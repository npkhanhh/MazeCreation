import Maze as m

mazeSize = [10, 20, 50, 100, 200, 500]
numberOfFile = 5
algo = ['Backtracker', 'Kruskal']

# for ms in mazeSize:
#     for i in range(numberOfFile):
#         maze = m.Maze(ms, algo[0])
#         maze.save('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[0]) + '-' + str(i) + '.txt')
#
#     for i in range(numberOfFile):
#         maze = m.Maze(ms, algo[1])
#         maze.save('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[1]) + '-' + str(i) + '.txt')

#print('Create completed')

f = open('solutionlength.txt', 'a')
maze = m.Maze()
maze.load('TestMazes\\test' + '-' + str(10) + '-' + str(algo[1]) + '-' + str(1) + '.txt')
maze.solve()
for ms in mazeSize:
    for i in range(numberOfFile):
        #maze = m.Maze(ms, algo[0])
        maze.load('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[0]) + '-' + str(i) + '.txt')
        maze.solve()
        f.write('Backtracker ' + str(i) + ' ' + str(maze.shortestPathLength) + '\n')

    for i in range(numberOfFile):
        #maze = m.Maze(ms, algo[1])
        maze.load('TestMazes\\test' + '-' + str(ms) + '-' + str(algo[1]) + '-' + str(i) + '.txt')
        maze.solve()
        f.write('Kruskal ' + str(i) + ' ' + str(maze.shortestPathLength) + '\n')

