import re

# Using the wiki link provided, we can pretty easily find the "radius" of the diamond around a sensor
# From there, we can construct the lines in either direction by subtracting 1 from the length of each
# Efficient enough for part 2? We'll see...

digitFinder = re.compile("-?\d+")


# What if we only worry about the sensors that overlap this line
n = 2000000

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
with open('bigInput.txt') as fin:
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
	radius

	if not (sensor.y-radius <= n <= sensor.y+radius):
		continue  # Skip any sensor areas that don't go through the target line

	# Okay, let's math out how to get the number of covered points on a line
	# So for every point of distance n is from the sensor, that will be a radius of one less
	# Then each x will be +- that radius about a central y
	radiusAtLine = radius - abs(sensor.y - n)

	# We don't really need to save each point, just the range of points
	# coveredRanges.append((sensor.x-radiusAtLine, sensor.x+radiusAtLine))

	# This brings up an issue with double counting a range
	# Let's try saving all the covered numbers and see how it goes
	covered = set(range(sensor.x-radiusAtLine, sensor.x+radiusAtLine+1))
	covered -= {p[0] for p in beaconSet.union(sensorSet) if p[1] == n}  # Remove any beacons or sensors that happent to be in the set
	coveredPoints = coveredPoints.union(covered)

print(sum(1 for p in coveredPoints))