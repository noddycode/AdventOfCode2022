from math import sqrt

# Part 2 Should be simple, we just need to extend the logic
# Each knot will follow the one in front of it the same as the tail followed the head in Part 1

headPos = [0,0]
rope = [headPos] + [[0,0] for _ in range(9)]  # Keep the head as a list, so it updates correctly
tailPositions = set()

def getDist(leader, follower):
	return sqrt((leader[0]-follower[0])**2 + (leader[1]-follower[1])**2)

with open('bigInput.txt') as fin:
	for k, l in enumerate(fin):
		l = l.strip()
		direction, steps  = l.split()
		steps = int(steps)
		tailPositions.add(tuple(rope[-1]))# Store any visited coordinates
		for i in range(steps):
			if direction == 'R':
				headPos[0] += 1
			elif direction == 'L':
				headPos[0] -= 1
			elif direction == 'U':
				headPos[1] += 1
			elif direction == 'D':
				headPos[1] -= 1

			for j in range(1, len(rope)):
				# Can't quite figure out why we don't run into an issue with the first input
				# But the stipulation that it always runs horizontally to keep up is important
				if getDist(rope[j-1], rope[j]) >= 2:
					# This is vector related, but I can't quite figure out the math
					horizontalMovement = rope[j-1][0] - rope[j][0]
					verticalMovement = rope[j-1][1] - rope[j][1]
					if rope[j-1][0] < rope[j][0]:
						rope[j][0] -= 1
					elif rope[j-1][0] > rope[j][0]:
						rope[j][0] += 1
					if rope[j-1][1] < rope[j][1]:
						rope[j][1] -= 1
					elif rope[j-1][1] > rope[j][1]:
						rope[j][1] += 1

				tailPositions.add(tuple(rope[-1]))

		print(k, '|'.join(f'{i}:{r[0]},{r[1]}' for i, r in enumerate(rope)))

print(len(tailPositions))