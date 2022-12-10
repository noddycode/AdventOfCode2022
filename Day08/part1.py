class Tree:
	def __init__(self, height):
		self.height = height
		self.visible = {
			'N': None,
			'E': None,
			'S': None,
			'W': None
		}

treeGrid = []

with open('bigInput.txt') as fin:
	for l in fin:
		treeGrid.append([Tree(int(c)) for c in l.strip()])

for row in range(len(treeGrid)):
	for column in range(len(treeGrid[row])):
		# Search each direction until a visible or taller tree is found
		
		tree = treeGrid[row][column]

		# North
		i = row
		while True:
			i -= 1
			if i < 0:  # Reached the edge without encountering any taller trees
				tree.visible['N'] = True
				break
			if treeGrid[i][column].height >= tree.height:  # Blocked by tree in this direction
				tree.visible['N'] = False
				break

		# South
		i = row
		while True:
			i += 1
			if i >= len(treeGrid):
				tree.visible['S'] = True
				break
			if treeGrid[i][column].height >= tree.height:
				tree.visible['S'] = False
				break

		# East
		i = column
		while True:
			i += 1
			if i >= len(treeGrid[row]):
				tree.visible['E'] = True
				break
			if treeGrid[row][i].height >= tree.height:
				tree.visible['E'] = False
				break

		# West
		i = column
		while True:
			i -= 1
			if i < 0:
				tree.visible['W'] = True
				break
			if treeGrid[row][i].height >= tree.height:
				tree.visible['W'] = False
				break


for row in treeGrid:
	treeRow = ''.join('T' if any(v.visible.values()) else 'F' for v in row)
	print(treeRow)

visibleTrees = len([t for row in treeGrid for t in row if any(t.visible.values())])
print(visibleTrees)
