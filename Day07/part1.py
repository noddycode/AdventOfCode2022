import itertools

# Different recursion, this time with depth-first search
# Time to remember how graphs work

with open('bigInput.txt') as fin:
	commands = [l.split() for l in fin.readlines()]  # Pre-emptively split each command into parts for easier processing
	commands.append('done')  # Add a poison pill to signal the end of processing
	commands.append(None)  # Poison pill for the poison pill?

class Directory:
	def __init__(self, dirName, parent):
		self.dirName = dirName
		self.parent = parent
		self.childDirectories = []
		self.childFiles = []
		self.totalSize = 0

	def __str__(self):
		output = [
			f'Name: {self.dirName}',
			f'Parent: {self.parent.dirName if self.parent else "None"}',  # Handle root parent
			f'Children: {",".join(d.dirName for d in self.childDirectories)}',
			f'Files: {",".join(f.fileName for f in self.childFiles)}',
			f'Total Size: {self.totalSize}'
		]

		return '\n'.join(output)


class File:  # Doesn't really matter what the file is called, but we'll keep it anyway
	def __init__(self, fileName, size):
		self.fileName = fileName
		self.size = size

# Time to build our graph
commandGenerator = (c for c in commands)  # Use a generator so we don't have to keep track of our position

commandList = None
rootDir = Directory('root', None)
currentDir = rootDir # We already know our first node
next(commandGenerator)  # Skip the first two lines
next(commandGenerator)

done = False

while not done:
	# We will break at the ls since we don't really need it
	# That way we can capture the preceding cd command and get the directory
	commandList = itertools.takewhile(lambda c: c and c[1] != 'ls', commandGenerator) 
	for command in commandList:
		if command == 'done':
			done = True
			break
		if command[0] == 'dir':
			newDir = Directory(command[1], currentDir)
			currentDir.childDirectories.append(newDir)
		elif command[1] == 'cd':
			if command[2] == '..':
				if currentDir.parent:
					currentDir = currentDir.parent  # Go up a node
			else:  # should signal the end of our command list
				# We have duplicate directory names, so make sure we go to one that's actually a child
				currentDir = [d for d in currentDir.childDirectories if d.dirName == command[2]][0]
		else: # Must be a file
			fileSize = int(command[0])
			currentDir.childFiles.append(File(command[1], fileSize))


# Finally, let's depth this search! (first)

visited = set()
allNodes = []
def getDirectorySize(directory):
	visited.add(directory.dirName)
	total = 0

	for child in directory.childDirectories:
		getDirectorySize(child)
		total += child.totalSize


	total += sum(f.size for f in directory.childFiles)
	directory.totalSize = total
	allNodes.append(directory)

getDirectorySize(rootDir)

output = sum(d.totalSize for d in allNodes if d.totalSize <= 100000)

print('\n\n'.join(str(d) for d in allNodes))

print(output)