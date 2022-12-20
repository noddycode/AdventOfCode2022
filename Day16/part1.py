import re
from itertools import permutations
import json

# Alright so that didn't really pan out
# Still, all is not lost. We have some good puzzle pieces here. Let's try to do some smart brute forcing
# Looking at the input data, MOST of the valves have a flow rate of 0, so we can safely ignore those in terms of opening
# Ideally we get as many open valves as possible in as few moves as possible
# So let's organize the valves by flow rate and try out a few combos, selecting the best one

# Blessed be regex101
parseRegex = re.compile(r'Valve\s(?P<valve>\w\w)[^=]+=(?P<rate>\d+).+valve(s)?\s(?P<neighbors>.+)$')

valveMap = {}

class Valve():

	def __init__(self, name, flowRate, neighbors):
		self.name = name
		self.flowRate = flowRate
		self.neighbors = neighbors

# Parse
with open('input.txt') as fin:
	for l in fin:
		valve, rate, neighbors = parseRegex.match(l).group('valve', 'rate', 'neighbors')
		neighbors = [n.strip() for n in neighbors.split(',')]
		valveMap[valve] = Valve(valve, int(rate), neighbors)
		print(valveMap[valve].name, valveMap[valve].flowRate, valveMap[valve].neighbors)

dijkstraCalculations = {}  # Store the result of the dijkstra calculations as we create them

# We meet again...
# Wait a second, can we reconfigure our distance here to take the lost flow into consideration?
def dijkstra(startValve):
	# Initialize the distance map
	distanceMap = {valve: float('inf') for valve in allValves}
	distanceMap[startValve] = 0
	# Initialize the unvisited set
	unvisited = set(allValves)
	# While we have unvisited nodes
	while unvisited:
		# Get the unvisited node with the smallest distance
		currentValve = min(unvisited, key=lambda x: distanceMap[x])
		# Remove it from the unvisited set
		unvisited.remove(currentValve)
		# For each of its neighbors
		for neighbor in valveMap[currentValve].neighbors:
			# Calculate the distance to the neighbor
			# This time, calculate how much flow is lost in traveling 
			neighborDistance = (distanceMap[currentValve] + 1)
			# If the neighbor is closer than our current distance, update it
			distanceMap[neighbor] = min(distanceMap[neighbor], neighborDistance)

	return distanceMap

def getTravelCost(startValve, endValve):
	# Use our cached dijkstra calculations if we have them
	if startValve not in dijkstraCalculations:
		dijkstraCalculations[startValve] = dijkstra(startValve)
	return dijkstraCalculations[startValve][endValve]

# We'll keep this guy and use it to run our moves
class Traveler():

	def __init__(self, moves=[]):
		self.currentValve = 'AA'
		self.flow = 0
		self.currentTime = 30
		self.moves = moves # Initial moveset is generated randomly, subsequent ones will be passed in
		self.openValves = set()
		self.done = False

	def run(self):
		# Reset values for the travelers that didn't get chopped
		self.currentValve = 'AA'
		self.flow = 0
		self.currentTime = 30
		self.openValves = set()
		self.done = False

		finishedMoves = []  # Keep track of how far we got for debugging purposes
		for move in self.moves:
			if self.currentTime <= 0 or self.done:
				self.moves = finishedMoves
				return  # Return once we run out of time
			if move == 'O':
				self.openValve()
			else:
				self.moveToValve(move)
			finishedMoves.append(move)

	def moveToValve(self, valve):
		if valve == self.currentValve:
			return

		# Don't let us go overtime
		if self.currentTime - getTravelCost(self.currentValve, valve) < 0:
			done = True
			return
		self.currentTime -= getTravelCost(self.currentValve, valve)
		self.currentValve = valve
		
	def openValve(self):
		if self.currentValve in self.openValves:
			return
		self.currentTime -= 1
		self.flow += valveMap[self.currentValve].flowRate * self.currentTime # Flow doesn't start until next minute
		self.openValves.add(self.currentValve)


	def __str__(self):
		lines = [
			f'{",".join(self.moves)}',
			f'Flow: {self.flow}',
			f'Open Valves: {",".join(sorted(self.openValves))}',
		]

		return '\n'.join(lines)

allValves = list(valveMap.keys())

# Here's where we get the new stuff
# Let's get all the of the highest output valves in order

sortedValves = sorted((v for v in allValves if valveMap[v].flowRate > 0), key=lambda x: valveMap[x].flowRate, reverse=True)

# So these are the only valves we care about, the rest is just travel distance
# So we could really re-make the graph and find every notable valves distance from every other notable valve
# Is there something we could do with that?

# Now, this is a set that grows exponentially
# So how do we narrow down which permutations we try?
# Let's start by opening the valves in descending order
# Then, we'll slowly move each valve to the end of the line

# Wait... 
# This feels like a sum of some sort, right?
# Because the cost of moving is a simple negative number
# But the benefit of opening a valve is multiplies
# So the cost of moving will be overshadowed by the increase in flow almost certainly, right?
# Does that mean if the start of one path is worse than a previous one, we can skip testing it?

# Thought of another way, each minute lost to traveling is exponentially more impactful than the minute spent opening the valve
# So... let's try organizing things in order of shortest travel distance?
# We'll still just concentrate on the valves that actually have flow rates
# There's got to be some way to calculate the tradeoff of valve to travel

# Let's see how close we get just ordering it by distance
# Spoiler: it was a bust

# What we basically have is a complete, undirected, weighted graph. So  maybe we can bfs this?

currentValve = 'AA'
travelValves = set(sortedValves)
travelOrder = []


while travelValves:

	nextValve = min(travelValves, key = lambda v: getTravelCost(currentValve, v)*valveMap[v].flowRate)
	travelValves.discard(nextValve)
	travelOrder.append(nextValve)
	travelOrder.append('O')
	currentValve = nextValve

traveler = Traveler(travelOrder)
traveler.run()

print(traveler)