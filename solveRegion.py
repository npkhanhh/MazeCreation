'''
Created on Apr 27, 2015

@author: ldhuy
'''

import numpy as np
# ################################################# Algorithm #################################################
# 
# def solveRegion
# 	pairs = [[[]]]
# 	for each row in region
# 		for each column in region
# 			if cell has entrance
# 				for each direction except entrance
# 					if there's connected neighbor
# 						entranceCellList = findPath(neighbor, direction of neighbor cell to the current cell, new [])
# 						addResults(entranceCellList, pairs)




# entranceCellList: list of cells that has entrance
# def findPath(cell, dir, entranceCellList)
# 	if cell has entrance
# 		entranceCellList.append(cell)
# 	for each direction except dir
# 		if there's connected neighbor
# 			subEntranceCell = findPath(neighbor, direction of neighbor cell to the current cell, new [])
# 			entraceCellList.append(subEntranceCell)
# 	return entranceCellList

############################################################################################################# 



# Check if this cell has entrance
# A cell has entrance only if it lies at the boundary and has a missing border
# Params:
#	grid: the whole maze
#	row, col: coordinate of the current cell
#	directions: a list to store the directions of the entrance wrt this cell, this can be use as an additional result
#					(a cell can have more than one entrance if it is at the corner of the region
# Return: True if the cell has entrance, False if not
def hasEntrance(grid, top, left, right, bottom, row, col, directions):
	result = False
	if row == top and grid[row][col].top == 0:
		result = True
		directions.append('top')
	if row == bottom - 1 and grid[row][col].bottom == 0:
		result = True
		directions.append('bottom')
	if col == left and grid[row][col].left == 0:
		result = True
		directions.append('left')
	if col == right - 1 and grid[row][col].right == 0:
		result = True
		directions.append('right')
	return result



# Params:
#	grid: the whole maze
#	row, col: coordinate of the current cell
#	direction: the direction of the current cell with respect to the previous cell
# Return: list of cells that has entrance
def findPath(grid, top, left, right, bottom, row, col, direction):
	entranceCellList = []		# entranceCellList is a 2D array stores coordinates of cells that have entrance(s)
	# Check if this cell has entrance
	entranceAt = []	# list of directions of the entrance of this cell
	if hasEntrance(grid, top, left, right, bottom, row, col, entranceAt):
		#entranceCellList = entranceCellList + [row, col]
		entranceCellList.append([row, col])
	
	if direction != 'right' and 'left' not in entranceAt and col > left and grid[row][col].left == 0:	# check left cell
		entranceCells = findPath(grid, top, left, right, bottom, row, col - 1, 'left')
		entranceCellList = entranceCellList + entranceCells
	if direction != 'top' and 'bottom' not in entranceAt and row < bottom - 1 and grid[row][col].bottom == 0:	# check bottom cell
		entranceCells = findPath(grid, top, left, right, bottom, row + 1, col, 'bottom')
		entranceCellList = entranceCellList + entranceCells
	if direction != 'left' and 'right' not in entranceAt and col < right - 1 and grid[row][col].right == 0:	# check right cell
		entranceCells = findPath(grid, top, left, right, bottom, row, col + 1, 'right')
		entranceCellList = entranceCellList + entranceCells
	if direction != 'bottom' and 'top' not in entranceAt and row > top and grid[row][col].top == 0:	# check top cell
		entranceCells = findPath(grid, top, left, right, bottom, row - 1, col, 'top')
		entranceCellList = entranceCellList + entranceCells
		
	return entranceCellList



# Find pairs of connected entrances of the regions
# Params:
#	grid: the matrix represent the whole maze
#	top, left, right, bottom:	co-ordinate of the top left and right bottom corners of the region
#								(the 'right' column and 'bottom' row are exclusive)
#	size: the size of the big maze
# Return: list of pairs of cells that has entrance(s) and connected
def sovleRegion(grid, top, left, right, bottom, size):
	entrancePairList = []	# entrancePairList is a 3D array stores pairs of cells that have entrance(s) and connected 
								# format: [[[entrance1X, entrance1Y], [entrance2X, entrance2Y]], [[entrance2X, entrance2Y], [entrance3X, entrance3Y]], ...]
	#marked = [[0 for i in range(size)] for i in range(size)]	# used to track whether the cell is already traversed
	for c in  range(left, right):
		for r in range(top, bottom):
			if (c == left or c == right - 1) and (r == top or r == bottom - 1):	# Only examine cells at the boundary
				entranceList = []	# list of entrance of this cell
				if hasEntrance(grid, top, left, right, bottom, r, c, entranceList):	# check if there is entrance to the left of this cell
					for i in range(len(entranceList)):
						if entranceList[i] != 'right' and c + 1 < right and grid[r][c].right == 0:
							foundEntrances = []	# list of entrances found by findPath method 
							foundEntrances = findPath(grid, top, left, right, bottom, r, c + 1, 'right')
							if np.shape(foundEntrances)[0] > 0:
								if np.shape(foundEntrances[0])[0] != 0:
									for j in range(np.shape(foundEntrances)[0]):	# add pairs to entrancePairList
										entrancePairList.append([[r, c], [foundEntrances[j][0], foundEntrances[j][1]]])
						if entranceList[i] != 'bottom' and r + 1 < bottom and grid[r][c].bottom == 0:
							foundEntrances = []	# list of entrances found by findPath method 
							foundEntrances = findPath(grid, top, left, right, bottom, r + 1, c, 'bottom')
							if np.shape(foundEntrances)[0] > 0:
								if np.shape(foundEntrances[0])[0] != 0:
									for j in range(np.shape(foundEntrances)[0]):	# add pairs to entrancePairList
										entrancePairList.append([[r, c], [foundEntrances[j][0], foundEntrances[j][1]]])
						if entranceList[i] != 'left' and c - 1 >= left and grid[r][c].left == 0:
							foundEntrances = []	# list of entrances found by findPath method 
							foundEntrances = findPath(grid, top, left, right, bottom, r, c - 1, 'left')
							if np.shape(foundEntrances)[0] > 0:
								if np.shape(foundEntrances[0])[0] != 0:
									for j in range(np.shape(foundEntrances)[0]):	# add pairs to entrancePairList
										entrancePairList.append([[r, c], [foundEntrances[j][0], foundEntrances[j][1]]])
						if entranceList[i] != 'top' and r - 1 >= top and grid[r][c].top == 0:
							foundEntrances = []	# list of entrances found by findPath method 
							foundEntrances = findPath(grid, top, left, right, bottom, r - 1, c, 'top')
							if np.shape(foundEntrances)[0] > 0:
								if np.shape(foundEntrances[0])[0] != 0:
									for j in range(np.shape(foundEntrances)[0]):	# add pairs to entrancePairList
										entrancePairList.append([[r, c], [foundEntrances[j][0], foundEntrances[j][1]]])
	
	# Remove redundant cells
	for i in range(len(entrancePairList)):
		for i2 in range(len(entrancePairList)):
			if i2 != i:
				if	(entrancePairList[i][0] == entrancePairList[i2][1] and entrancePairList[i][1] == entrancePairList[i2][0]) or \
					(entrancePairList[i][0] == entrancePairList[i2][0] and entrancePairList[i][1] == entrancePairList[i2][1]): 
						entrancePairList.pop(i2)

	return entrancePairList




	

