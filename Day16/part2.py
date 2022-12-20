import re
import random
from itertools import permutations
import json


# What if we combine our genetic algorithm with our simplified distance graph?
# We know there are only several nodes we need to care about, and we'll need to open at every one
# So we can cut down the number of options and eliminate opening as an option that needs to be considered
# Does this whittle things down enough to get an asnwer?

# Various tuning knobs
NUM_TRAVELER_PAIRS = 2000
NUM_TOP_TRAVELER_PAIRS = 50
NUM_ITERATIONS = 10000
NUM_REPEATS = 10
STARTING_MOVES = 15
REWARD_MULTIPLIER = 2
PUNISHMENT_MULTIPLIER = 0
MUTATION_RATE = 0.8  # How often we mutate the resultant movesets
MUTATION_INTESITY = 0.8  # How much we mutate when we hit the above rate

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

# Global tracker for our open valves
openValves = set()

# New class that will keep track of us and our elephant
class TravelerPair():

	def __init__(self, ourTraveler, elephantTraveler):
		self.us = ourTraveler
		self.elephant = elephantTraveler
		self.openValves = set()

	def run(self):
		self.flow = 0
		self.openValves = set()

		self.us.reset()
		self.elephant.reset()

		# We have to do this carefully, so
		# We can keep our movelist, but we'll need to be sure that we reslove the right move first
		# We can do this by figuring out who will complete their move first
		# They should (hopefully) be able to breed the pair of movesets that doesn't overlap too much

		# No point in continuing if all of the important valves are open
		while self.elephant.moves or self.us.moves or (len(self.openValves) < len(allValves)):
			# Resolve the move that will finish first
			unitToMove = None
			# Resolve us first in a tie for consistency
			if self.elephant.getNextTime() == self.us.getNextTime():
				unitToMove = self.us
			else:
				unitToMove = max(self.elephant, self.us, key=lambda x: x.getNextTime())
			
			if unitToMove.getNextTime() == float('inf'):
				break  # Each has finished all viable moves

			valve, flow = unitToMove.openValve(self.openValves)
			self.flow += flow
			self.openValves.add(valve)

	def __str__(self):
		lines = [
			f'Us: {self.us}',
			f'Elephant: {self.elephant}',
			f'Flow	: {self.flow}',
		]

		return '\n'.join(lines)


# Our genetic learning class
class Traveler():

	def __init__(self, moves=[]):
		self.currentValve = 'AA'
		self.currentTime = 26
		self.moves = moves # Initial moveset is generated randomly, subsequent ones will be passed in
		self.originalMoves = moves.copy()
		self.finishedMoves = []

	# Reset our stuff for the next round
	def reset(self):
		self.currentValve = 'AA'
		self.currentTime = 26
		self.moves = self.originalMoves.copy()
		self.finishedMoves = []

	def getNextTime(self):
		# Figure out how long it will take us to get to the next valve
		if not self.moves:
			return float('inf')
		nextTime = self.currentTime - getTravelCost(self.currentValve, self.moves[0])
		if nextTime+1 < 0:
			return float('inf')
		else: 
			return nextTime
	
	# We'll simply assume that we open every valve we visit
	def openValve(self, openValves):

		# Will have traveled to the valve regardless of if it's open or not
		valve = self.moves.pop(0)
		newTime = self.currentTime - (getTravelCost(self.currentValve, valve))  # Add a minute for opening the valve
		self.currentValve = valve
		self.finishedMoves.append(valve)

		flow = 0
		if not valve in openValves:
			newTime -= 1  # Remove minute for opening the valve
			flow = valveMap[self.currentValve].flowRate * newTime # Flow doesn't start until next minute

		self.currentTime = newTime
		return valve, flow

	def __str__(self):
		lines = [
			f'{",".join(self.finishedMoves)}'
		]

		return '\n'.join(lines)

# Grab only the important valves
allValves = [v for v in valveMap.keys() if valveMap[v].flowRate > 0]
startTravelerPairs = []

# Let the travelers find their own ways between valves
def generateInitialMoves(startTravelerPairs):
	for i in range(NUM_TRAVELER_PAIRS):
		us = Traveler(random.sample(allValves, len(allValves)))
		elephant = Traveler(random.sample(allValves, len(allValves)))

		startTravelerPairs.append(TravelerPair(us, elephant))

# Generate new movesets
def breed(travelerPair1, travelerPair2):

	newTravelers = []
	for traveler1, traveler2 in [(travelerPair1.us, travelerPair2.us), (travelerPair2.elephant, travelerPair1.elephant)]:
		# Get a random split point
		# print(traveler1, traveler2)
		splitPoint = random.randint(0, len(traveler1.originalMoves))
		# Since our moves use dijkstra, we can be sure that the entire moveset is valid
		tempMoves = traveler1.originalMoves[:splitPoint] + traveler2.originalMoves[splitPoint:]

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

		# Remove any moves in elephant moveset that are already in our moveset
		if newTravelers:
			newMoves = [m for m in newMoves if m not in newTravelers[0].originalMoves]

		newTravelers.append(Traveler(newMoves))

	return TravelerPair(*newTravelers)

# Rather than change our class, we'll just consider our travelers in pairs
def runTests(travelers):
	bestFlow = None
	startTravelerPairs = []
	generateInitialMoves(startTravelerPairs)
	travelerPairs = startTravelerPairs
	for i in range(NUM_ITERATIONS):
		for travelerPair in travelerPairs:
			travelerPair.run()
		
		# Take the best ones we've got
		bestTravelerPairs = sorted(travelerPairs, key=lambda x: x.flow, reverse=True)[:NUM_TOP_TRAVELER_PAIRS]
		# print(bestTravelerPairs[0])
		bestFlow = bestTravelerPairs[0]
		newTravelerPairs = []
		
		# Breed 'em until we're back to our original number of travelers
		for j in range(NUM_TRAVELER_PAIRS - NUM_TOP_TRAVELER_PAIRS):
			newTravelerPairs.append(breed(random.choice(bestTravelerPairs), random.choice(bestTravelerPairs)))
		
		travelerPairs = bestTravelerPairs + newTravelerPairs

	return bestFlow

bestFlows = []
# We run this test a few times so that we can avoid any dead ends that lock us into a bad answer
for i in range(NUM_REPEATS):
	bestFlow = runTests(startTravelerPairs)
	print(bestFlow)
	bestFlows.append(bestFlow)

print(max(bestFlows, key=lambda x: x.flow))