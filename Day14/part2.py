
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

# We need to make some general observations about how the sand piles up
# If we observe the visualization for our sample input, we can see that the sand forms an inverse
# triangle under any rock overhangs

# Let's make some test input of our own to see how it deals with enclosed spaces

# Other observations:
# - The one point gap in the large input doesn't seem to affect the shape of the triangle under an overhang
# - Enclosed spaces cut the inverted triangle in half
# - Upward spikes don't seem to affect things

# Can we create a giant triangle of sand and simply subtract sand from the overhangs?
# We need to 1) find all overhangs, 2) "fill" any gaps, and 3) detect enclosed areas


# If we store lines as lines, they'll be easier to use later
verticalCaveRanges = set()
horizontalCaveRanges = set()
with open('input.txt') as fin:
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

			if fromX == toX:  # Vertical line
				for j in range(startPoint[1], endPoint[1]+1):  # Range is non-inclusive of end
					cavePathPoints.add((fromX, j))
				verticalCaveRanges.add((startPoint, endPoint))
			else:  # Horizontal line
				for j in range(startPoint[0], endPoint[0]+1):
					cavePathPoints.add((j, fromY))
				horizontalCaveRanges.add((startPoint, endPoint))



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

for i in range(source[1], maxY):
	# Fill in our triangle completely
	midX = source[0]  # The central X coordinate that all lines will extend from
	grainPoints = grainPoints.union((x, i) for x in range(midX-i, midX+i+1))  # Source is at y=0, so this works

# Now, let's find all of our overhangs
# That is, any continuous line >= 2 units long

# First, let's combine all horizontal ranges that have 1 point gaps
# We can do this by simply combining any range that has a start point that is 1 unit away from the end point of another range
while True:
	changed = False
	for firstRange in horizontalCaveRanges:
		for secondRange in horizontalCaveRanges:
			if firstRange == secondRange:
				continue

			if firstRange[0][0] == r2[1][0]+2:  # Compare r's start point to r2's end point + 2
				# Combine them
				newRange = ((r2[0][0], r[0][1]), (r[1][0], r[1][1]))
				horizontalCaveRanges.remove(r)
				horizontalCaveRanges.remove(r2)
				horizontalCaveRanges.add(newRange)
				changed = True
				break

		if changed:
			break

	if not changed:
		break

setBounds(max(grainPoints, key=lambda p: p[0]))
setBounds(min(grainPoints, key=lambda p: p[0]))

renderCave()
print(grainCount)