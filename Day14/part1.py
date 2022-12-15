
source = (500,0)

minX = minY = 10000  # Arbitraily large value
maxX = maxY = 0  # Keep track of how big our cave is as we parse the file

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

done = False
grainCount = 0
grainPoints = set()
print(cavePathPoints)
while not done:
	grainPos = source
	while not done:
		if (grainPos[0], grainPos[1]+1) not in cavePathPoints.union(grainPoints):  # Fall down
			grainPos = (grainPos[0], grainPos[1]+1)
		elif (grainPos[0]-1, grainPos[1]+1) not in cavePathPoints.union(grainPoints): # Fall to the left
			grainPos = (grainPos[0]-1, grainPos[1]+1)
		elif (grainPos[0]+1, grainPos[1]+1) not in cavePathPoints.union(grainPoints):  # Fall to the right
			grainPos = (grainPos[0]+1, grainPos[1]+1)
		else:  # Criss-cross! (grain has come to rest)
			grainCount += 1
			grainPoints.add(grainPos)
			break
		if grainPos[0] < minX or grainPos[0] > maxX or grainPos[1] > maxY:
			done = True


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
		else:
			line += '.'

	out.append(line)

print('\n'.join(out))
print(grainCount)