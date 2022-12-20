import re
import random
from itertools import permutations
import json

# What if we combine our genetic algorithm with our simplified distance graph?
# We know there are only several nodes we need to care about, and we'll need to open at every one
# So we can cut down the number of options and eliminate opening as an option that needs to be considered
# Does this whittle things down enough to get an asnwer?

# Various tuning knobs
NUM_TRAVELERS = 1000
NUM_TOP_TRAVELERS = 100
NUM_ITERATIONS = 3000
NUM_REPEATS = 1
STARTING_MOVES = 15
REWARD_MULTIPLIER = 2
PUNISHMENT_MULTIPLIER = 0
MUTATION_RATE = 0.8  # How often we mutate the resultant movesets
MUTATION_INTESITY = 0.7  # How much we mutate when we hit the above rate

# Blessed be regex101
parseRegex = re.compile(r'Valve\s(?P<valve>\w\w)[^=]+=(?P<rate>\d+).+valve(s)?\s(?P<neighbors>.+)$')

valveMap = {}

class Valve():

	def __init__(self, name, flowRate, neighbors):
		self.name = name
		self.flowRate = flowRate
		self.neighbors = neighbors

# Parse
with open('bigInput.txt') as fin:
	for l in fin:
		valve, rate, neighbors = parseRegex.match(l).group('valve', 'rate', 'neighbors')
		neighbors = [n.strip() for n in neighbors.split(',')]
		valveMap[valve] = Valve(valve, int(rate), neighbors)
		print(valveMap[valve].name, valveMap[valve].flowRate, valveMap[valve].neighbors)

dijkstraCalculations = {}  # Store the result of the dijkstra calculations as we create them

# We meet again...
def dijkstra(startValve):
	# Initialize the distance map
	valveSet = set(valveMap.keys())
	distanceMap = {valve: float('inf') for valve in valveSet}
	distanceMap[startValve] = 0
	# Initialize the unvisited set
	unvisited = valveSet
	# While we have unvisited nodes
	while unvisited:
		# Get the unvisited node with the smallest distance
		currentValve = min(unvisited, key=lambda x: distanceMap[x])
		# Remove it from the unvisited set
		unvisited.remove(currentValve)
		# For each of its neighbors
		for neighbor in valveMap[currentValve].neighbors:
			# Calculate the distance to the neighbor
			neighborDistance = distanceMap[currentValve] + 1  # Still an unweighted graph
			# If the neighbor is closer than our current distance, update it
			distanceMap[neighbor] = min(distanceMap[neighbor], neighborDistance)

	return distanceMap

def getTravelCost(startValve, endValve):
	# Use our cached dijkstra calculations if we have them
	if startValve not in dijkstraCalculations:
		dijkstraCalculations[startValve] = dijkstra(startValve)
	return dijkstraCalculations[startValve][endValve]

# Our genetic learning class
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

		# if len(self.moves) < len(allValves):
		# 	self.flow = -50
		# 	return

		finishedMoves = []  # Keep track of how far we got for debugging purposes
		for move in self.moves:
			if self.currentTime <= 0 or self.done:
				self.moves = finishedMoves
				return  # Return once we run out of time
			else:
				self.openValve(move)
			finishedMoves.append(move)
			# print(self.currentTime)
	
	# We'll simply assume that we open every valve we visit
	def openValve(self, valve):
		newTime = self.currentTime - (getTravelCost(self.currentValve, valve) + 1)  # Add a minute for opening the valve

		# Don't let us go overtime
		if newTime < 0:
			done = True
			return

		self.currentTime = newTime
		self.currentValve = valve
		self.flow += valveMap[self.currentValve].flowRate * self.currentTime # Flow doesn't start until next minute
		self.openValves.add(valve)
		

	def getFitness(self):
		# Punish for leaving time on the clock
		return self.flow*REWARD_MULTIPLIER - self.currentTime*PUNISHMENT_MULTIPLIER  

	def __str__(self):
		lines = [
			f'{",".join(self.moves)}',
			f'Fitness: {self.getFitness()}',
			f'Flow: {self.flow}',
			f'Open Valves: {",".join(sorted(self.openValves))}',
		]

		return '\n'.join(lines)

# Grab only the important valves
allValves = [v for v in valveMap.keys() if valveMap[v].flowRate > 0]
startTravelers = [Traveler() for i in range(NUM_TRAVELERS)]

# Let the travelers find their own ways between valves
def generateInitialMoves(startTravelers):
	for traveler in startTravelers:
		traveler.moves = random.sample(allValves, len(allValves))
		# We already know it's pointless to visit the same valve twice
		# So just test permutations

# Generate new movesets
def breed(traveler1, traveler2):
	# Get a random split point
	# print(traveler1, traveler2)
	splitPoint = random.randint(0, len(traveler1.moves))
	# Since our moves use dijkstra, we can be sure that the entire moveset is valid
	tempMoves = traveler1.moves[:splitPoint] + traveler2.moves[splitPoint:]

	# Change some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(tempMoves)):
			if random.random() < MUTATION_INTESITY:
				tempMoves[i] = random.choice(allValves)

	# Delete some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(tempMoves)//2):
			if random.random() < MUTATION_INTESITY:
				tempMoves.pop(i)

	# Add some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(tempMoves)//2):
			if random.random() < MUTATION_INTESITY:
				tempMoves.insert(i, random.choice(allValves))

	newMoves = []
	[newMoves.append(m) for m in tempMoves if m not in newMoves]  # remove duplicates
	newTraveler = Traveler(newMoves)
	# print(newTraveler)

	return newTraveler


def runTests(travelers):
	bestFlow = None
	generateInitialMoves(startTravelers)
	travelers = startTravelers
	for i in range(NUM_ITERATIONS):
		for traveler in travelers:
			traveler.run()
		
		# Take the best ones we've got
		bestTravelers = sorted(travelers, key=lambda x: x.getFitness(), reverse=True)[:NUM_TOP_TRAVELERS]
		print(bestTravelers[0])
		bestFlow = bestTravelers[0]
		newTravelers = []
		
		# Breed 'em until we're back to our original number of travelers
		for j in range(NUM_TRAVELERS - NUM_TOP_TRAVELERS):
			newTravelers.append(breed(random.choice(bestTravelers), random.choice(bestTravelers)))
		
		travelers = bestTravelers + newTravelers

	return bestFlow

bestFlows = []
# We run this test a few times so that we can avoid any dead ends that lock us into a bad answer
for i in range(NUM_REPEATS):
	bestFlow = runTests(startTravelers)
	print(bestFlow)
	bestFlows.append(bestFlow)

print(max(bestFlows, key=lambda x: x.flow))