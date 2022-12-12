import string
from math import inf, sqrt
from functools import total_ordering

# This immediately seems like a great fit for dijkstra's, which I totally remember and don't have to look up

# Don't actually need this because the distance between adjacent nodes will always be 1...
def getDistance(firstPoint, secondPoint):
	return sqrt((firstPoint[0]-secondPoint[0])**2 + (firstPoint[1]-secondPoint[1])**2)

# We'll work with numbers instead of letters cause it's easier

letterMap = {l:i for i, l in enumerate(string.ascii_lowercase)}
letterMap['S'] = 0
letterMap['E'] = 25

# Use this class to convert the input to a graph
@total_ordering
class Point(object):
	def __init__(self, x, y, elevation):
		self.x = x
		self.y = y
		self.elevation = elevation
		self.neighbors = []
		self.distance = inf

	def __eq__(self, other):  # Makes it easy to find our minimum distance
		return self.distance == other.distance

	def __lt__(self, other):
		return self.distance < other.distance

	def __str__(self):
		return f'({self.x},{self.y})'
		
graph = {}
width = 0
height = 0
start = None
end = None
with open('bigInput.txt') as fin:
	for i, l in enumerate(fin):
		l = l.strip()
		width = 0
		for j, letter in enumerate(l):
			point = Point(j, i, letterMap[letter])

			if letter == 'S':
				start = point
			elif letter == 'E':
				end = point
				point.distance = 0
				

			graph[(j,i)] = point
			width += 1
		height += 1



# Set connections between graph nodes
for y in range(height):
	for x in range(width):
		for point in (p for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))):
			if 0 <= point[0] < width and 0 <= point[1] < height:
				diff = graph[(x,y)].elevation - graph[point].elevation

				if diff <= 1: # Can traverse this edge
					# IMPORTANT: can go down as far as you want
					# Messed me up for way too long...
					# Kind of seems reversed cause we're going from the end to the beginning
					graph[(x, y)].neighbors.append(graph[point])
					


shortestPathTree = set()  # We'll use the coordinates to track these since the object is not hashable

current = None
while len(shortestPathTree) < len(graph.keys()):
	current = min(g[1] for g in graph.items() if g[0] not in shortestPathTree)

	shortestPathTree.add((current.x, current.y))
	for neighbor in current.neighbors:
		dist = 1 + current.distance
		neighbor.distance = min(neighbor.distance, dist)

# Just a small change here, we already know which nodes are at elevation a (0)

print(min(p for p in graph.values() if p.elevation == 0).distance)
