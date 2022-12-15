import re

# For part 2, we need not worry about how many covered spaces there are, only where there are gaps in ranges
# This should make it somewhat easier to record just the ranges of x coorinates and find gaps therein

digitFinder = re.compile("-?\d+")

maxPoint = 4000000


objectSet = set()

class Sensor():

	def __init__(self, x, y, beaconX, beaconY):
		self.x = x
		self.y = y
		self.beaconX = beaconX
		self.beaconY = beaconY
		self.radius = 0

	def __str__(self):
		lines = [
			f'Sensor: ({self.x},{self.y})',
			f'Beacon: ({self.beaconX},{self.beaconY})'
		]

		return '\n'.join(lines)



sensors = []
with open('bigInput.txt') as fin:
	for l in fin:
		# Grab just the important stuff
		digits = [int(d) for d in digitFinder.findall(l)]
		sensor = Sensor(*digits)
		radius = abs(sensor.x - sensor.beaconX) + abs(sensor.y - sensor.beaconY)
		sensor.radius = radius
		sensors.append(sensor)
		objectSet.add((sensor.x, sensor.y))
		objectSet.add((sensor.beaconX, sensor.beaconY))

# We use this to combine all of our ranges
# Anything with more than one range at the end must have a gap
def combineRanges(ranges):
	outputRanges = []
	testRanges = []
	for start, end in ranges:
		# Clip ranges to our search bounds
		start = max(start, 0)
		end = min(end, maxPoint)

		# Throw out any ranges that are completely outside of our bounds
		if end < start:
			continue
		else:
			testRanges.append((start, end))

	if not testRanges:
		return []

	testRanges = sorted(testRanges)  # Ordering should prevent need to re-check ranges... I think

	outputRanges.append(testRanges[0])
	for i in range(1,len(testRanges)):
		for j in range(len(outputRanges)):
			start, end = testRanges[i]
			outStart, outEnd = outputRanges[j]
			if start <= outEnd and end >= outStart:  # Ranges overlap
				outputRanges[j] = (min(start, outStart), max(end, outEnd))
				break
		else:
			# Reached this point without hitting any overlapping
			outputRanges.append((start,end))

	return outputRanges


allCombined = {}
for i in range(maxPoint):
	ranges = []

	for sensor in (s for s in sensors if s.y-s.radius <= i <= s.y+s.radius):  # Get all sensor zones that extend into this line

		# Okay, let's math out how to get the number of covered points on a line
		# So for every point of distance n is from the sensor, that will be a radius of one less
		# Then each x will be +- that radius about a central y
		radiusAtLine = sensor.radius - abs(sensor.y - i)

		sensorRange = (sensor.x-radiusAtLine, sensor.x+radiusAtLine)
		ranges.append(sensorRange)

	ranges.extend([(x,x) for x,y in objectSet if y == i])  # Add any objects on this line
	# I don't know why this isn't working like I expect but I'm tired

	combined = combineRanges(ranges)
	if len(combined) >1:
		# print(i, combined)
		allCombined[i] = combined  # Every line that has at least one gap


# Now we just have to figure out
# 1) Where the gap is and
# 2) If there is a sensor or beacon there

for line, combined in allCombined.items():
	for i in range(len(combined)-1):
		gap = combined[i+1][0] - combined[i][1]
		# Just in case we have a gap spanning multiple spaces
		# I honestly don't know why there's "gaps" that are 1 unit apart but like... whatever
		for j in range(combined[i][1]+1, combined[i][1]+gap):
			if (j, line) not in objectSet:
				print(line, j, line)
				print(j*maxPoint+line)