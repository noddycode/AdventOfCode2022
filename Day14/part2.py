
source = (500,0)

minX = minY = 10000  # Arbitraily large value
maxX = maxY = 0

# Keep track of these for rendering purposes
def setBounds(point):
	global minX, minY, maxX, maxY

	minX = min(point[0], minX)
	minY = min(point[1], minY)
	maxX = max(point[0], maxX)
	maxY = max(point[1], maxY)


setBounds(source)

cavePathPoints = set()

with open('bigInput.txt') as fin:
	for l in fin:
		lines = [x.strip() for x in l.split('->')]
		for i in range(len(lines)-1):
			fromX, fromY = [int(p) for p in lines[i].split(',')]
			toX, toY = [int(p) for p in lines[i+1].split(',')]
			setBounds((fromX, fromY))
			setBounds((toX, toY))

			# Handle lines that go from right to left/down to up
			startPoint = endPoint = None

			if fromX > toX or fromY > toY:
				startPoint = (toX, toY)
				endPoint = (fromX, fromY)
			else:
				startPoint = (fromX, fromY)
				endPoint = (toX, toY)

			if fromX == toX:
				for j in range(startPoint[1], endPoint[1]+1):  # Range is non-inclusive of end
					cavePathPoints.add((fromX, j))
			else:
				for j in range(startPoint[0], endPoint[0]+1):
					cavePathPoints.add((j, fromY))



maxY += 2

def renderCave():
	out = []
	for i in range(minY, maxY+1):
		line = ''
		for j in range(minX, maxX+1):
			if (j,i) == source:
				line += '+'
			elif (j,i) in cavePathPoints:
				line += '#'
			elif (j,i) in grainPoints:
				line += 'o'
			elif i == maxY:
				line += '#'  # Render the infnite floor
			else:
				line += '.'

		out.append(line)

	print('\n'.join(out))

done = False
grainCount = 0
grainPoints = set()

# We need a more efficient way to simulate this
# Let's use our render function to make some observations about how this works
# The end result is roughly a triangle with the source as its tip
# Blank spots appear when there is more than one unit of overhang above some sand
# Does this hold true enough for us to simply build the triangle from the ground up?
# It'll be hard to tell until we try, so let's give it a bit of thought
# I think the thought is that sand will always be able to pile below an overhange IF it has more than one block of space to tumble down
# Let's use our original code real quick and see if we can't simulate some of our output and test this

# Hmm, looking at our test output, we run into some interesting cases that don't fit quite so neatly, especially with enclosed spaces
# Let's try to just make our original code more efficient


grainPos = lastImpact = source
impacted = False
while not done:
	grainPos = (lastImpact[0], lastImpact[1]-1) # Save the last place we hit, then continue calculating from there
	impacted = False
	# renderCave()
	while not done:
		if grainPos[1]+1 >= maxY:
			grainCount += 1
			grainPoints.add(grainPos)
			break

		if ((grainPos[0], grainPos[1]+1) in cavePathPoints.union(grainPoints) or grainPos[1]+1 >= maxY) and not impacted:
			lastImpact = grainPos
			impacted = True

		if (grainPos[0], grainPos[1]+1) not in cavePathPoints.union(grainPoints):  # Fall down
			grainPos = (grainPos[0], grainPos[1]+1)
		elif (grainPos[0]-1, grainPos[1]+1) not in cavePathPoints.union(grainPoints): # Fall to the left
			grainPos = (grainPos[0]-1, grainPos[1]+1)
		elif (grainPos[0]+1, grainPos[1]+1) not in cavePathPoints.union(grainPoints):  # Fall to the right
			grainPos = (grainPos[0]+1, grainPos[1]+1)
		else:
			grainCount += 1
			grainPoints.add(grainPos)
			break

	setBounds(grainPos)
	if grainPos == source:
		done = True

renderCave()
print(grainCount)