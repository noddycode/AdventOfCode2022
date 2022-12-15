import re

# Using the wiki link provided, we can pretty easily find the "radius" of the diamond around a sensor
# From there, we can construct the lines in either direction by subtracting 1 from the length of each
# Efficient enough for part 2? We'll see...

digitFinder = re.compile("-?\d+")

# For rendering purposes
sensorSet = set()
beaconSet = set()

class Sensor():

	def __init__(self, x, y, beaconX, beaconY):
		self.x = x
		self.y = y
		self.beaconX = beaconX
		self.beaconY = beaconY

	def __str__(self):
		lines = [
			f'Sensor: ({self.x},{self.y})',
			f'Beacon: ({self.beaconX},{self.beaconY})'
		]

		return '\n'.join(lines)



sensors = []
with open('input.txt') as fin:
	for l in fin:
		# Grab just the important stuff
		digits = [int(d) for d in digitFinder.findall(l)]
		sensor = Sensor(*digits)
		sensors.append(sensor)
		sensorSet.add((sensor.x, sensor.y))
		beaconSet.add((sensor.beaconX, sensor.beaconY))

coveredPoints = set()

for sensor in sensors:
	# From the linked wiki
	radius = abs(sensor.x - sensor.beaconX) + abs(sensor.y - sensor.beaconY)
	originalRadius = radius

	for y in range(sensor.y, sensor.y+radius+1):  # Get to bottom of covered area
		for x in range(sensor.x-radius, sensor.x+radius+1): # Width of covered area
			coveredPoints.add((x, y))
		radius -= 1

	radius = originalRadius
	for y in range(sensor.y, sensor.y-radius-1, -1):  # Now go to the top
		for x in range(sensor.x-radius, sensor.x+radius+1): # Width of covered area
			coveredPoints.add((x, y))
		radius -= 1


def renderCave():
	allPoints = coveredPoints.union(beaconSet, sensorSet)
	minX = min(p[0] for p in allPoints)
	minY = min(p[1] for p in allPoints)
	maxX = max(p[0] for p in allPoints)
	maxY = max(p[1] for p in allPoints)

	out = []
	out.append(f'{minX}\t' + ''.join(str(r)[-1] for r in range(minX, maxX+1)))

	for y in range(minY, maxY+1):
		line = f'{y}\t'
		for x in range(minX, maxX+1):
			point = (x,y)

			if point in sensorSet:
				line += 'S'
			elif point in beaconSet:
				line += 'B'
			elif point in coveredPoints:
				line += '#'
			else:
				line += '.'
		out.append(line)

	print('\n'.join(out))



# Count how many covered points are at level n
n = 10

renderCave()
print(sum(1 for p in coveredPoints if p not in beaconSet and p[1] == n))