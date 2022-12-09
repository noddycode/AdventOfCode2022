from math import sqrt

# Time for vector math?

headPos = [0,0]
tailPos = (0,0)  # We don't modify the tail position directly, so it's a tuple
tailPositions = set()

def getDist():
	return sqrt((headPos[0]-tailPos[0])**2 + (headPos[1]-tailPos[1])**2)

def getMovement():  # Don't actually need this, but it's cool so I'll keep it
	# First create a vector for tail to head
	vector = [headPos[0]-tailPos[0],headPos[1]-tailPos[1]]
	# Then move the tail in the required position
	# We subtract one since the tail needs to be behind it, but we don't want to go below 0
	return [max((0, vector[0]-1)), max((0, vector[1]-1))]

with open('bigInput.txt') as fin:
	lastPos = tuple(headPos)  # When T moves, it should be to the last place H was
	# Just kinda how the movement works out? Like snake
	for l in fin:
		l = l.strip()
		direction, steps  = l.split()
		steps = int(steps)
		for i in range(steps):
			tailPositions.add(tuple(tailPos))  # Store any visited coordinates

			if direction == 'R':
				headPos[0] += 1
			elif direction == 'L':
				headPos[0] -= 1
			elif direction == 'U':
				headPos[1] += 1
			elif direction == 'D':
				headPos[1] -= 1

			if getDist() >= 2:
				tailPos = lastPos

			lastPos = tuple(headPos)

			print(headPos, tailPos)

print(len(tailPositions))