import re
import random
import json

# Let's get weird with it
# Let's build a simple genetic AI


# Various tuning knobs
NUM_TRAVELERS = 3000
NUM_TOP_TRAVELERS = 300
NUM_ITERATIONS = 5000
NUM_REPEATS = 10
STARTING_MOVES = 30
REWARD_MULTIPLIER = 2
PUNISHMENT_MULTIPLIER = 1
MUTATION_RATE = 0.9  # How often we mutate the resultant movesets
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

allValves = list(valveMap.keys())
startTravelers = [Traveler() for i in range(NUM_TRAVELERS)]

# Let the travelers find their own ways between valves
def generateInitialMoves(startTravelers):
	for traveler in startTravelers:
		traveler.moves = [random.choice(['O'] + allValves) for i in range(STARTING_MOVES)]



# Generate new movesets
def breed(traveler1, traveler2):
	# Get a random split point
	# print(traveler1, traveler2)
	splitPoint = random.randint(0, len(traveler1.moves))
	# Since our moves use dijkstra, we can be sure that the entire moveset is valid
	newMoves = traveler1.moves[:splitPoint] + traveler2.moves[splitPoint:]

	# Change some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(newMoves)):
			if random.random() < MUTATION_INTESITY:
				newMoves[i] = random.choice(['O'] + allValves)

	# Delete some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(newMoves)//2):
			if random.random() < MUTATION_INTESITY:
				newMoves.pop(i)

	# Add some random moves
	if random.random() < MUTATION_RATE:
		for i in range(len(newMoves)//2):
			if random.random() < MUTATION_INTESITY:
				newMoves.insert(i, random.choice(['O'] + allValves))

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
		# print(bestTravelers[0])
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