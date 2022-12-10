class Tree:
	def __init__(self, height):
		self.height = height
		self.distance = {
			'N': 0,
			'E': 0,
			'S': 0,
			'W': 0
		}
		self.score = 0


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
				break
			tree.distance['N'] += 1  # We count the tree that blocks the view, so increment here
			if treeGrid[i][column].height >= tree.height:  # Blocked by tree in this direction
				break
			

		# South
		i = row
		while True:
			i += 1
			if i >= len(treeGrid):
				break
			tree.distance['S'] += 1
			if treeGrid[i][column].height >= tree.height:
				break
			

		# East
		i = column
		while True:
			i += 1
			if i >= len(treeGrid[row]):
				break
			tree.distance['E'] += 1
			if treeGrid[row][i].height >= tree.height:
				break
			

		# West
		i = column
		while True:
			i -= 1
			if i < 0:
				break
			tree.distance['W'] += 1
			if treeGrid[row][i].height >= tree.height:
				break

			



flattened = [tree for row in treeGrid for tree in row]
for t in flattened:
	t.score = t.distance['N'] * t.distance['E'] * t.distance['S'] * t.distance['W']

print(max(flattened, key=lambda t: t.score).score)