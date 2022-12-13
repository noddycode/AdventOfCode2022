from itertools import zip_longest
from functools import cmp_to_key


def parsePacket(packetString):
	packetString = packetString[1:-1]  # We know the first and last are brackets, so cut them off
	packetString = list(packetString)
	packet = []
	tempStack = []  # Stack characters here as we find them
	bracketCount = 0  # Keep track of our nested brackets
	while packetString:
		character = packetString.pop(0)
		tempStack.append(character)

		if character == '[':
			bracketCount += 1
		if character == ']':
			bracketCount -= 1

		if (character == ',' and bracketCount == 0) or not packetString:  # Only look at outermost commas | clean up last element
			elem = ''.join(tempStack).strip(',')
			if not elem.startswith('['):
				elem = int(elem)
			packet.append(elem)
			tempStack = []

	return packet

# This will be our test function
def processPacket(left, right):
	left = parsePacket(left)
	right = parsePacket(right)

	for leftElem, rightElem in zip_longest(left, right):
		# If one of these runs out before we return a value, handle it here
		if leftElem == None:
			return 1
		elif rightElem == None:
			return -1

		# print(rightElem, leftElem)
		if all(isinstance(e, int) for e in (leftElem, rightElem)):  # Both ints
			if leftElem < rightElem:
				return 1
			elif leftElem > rightElem:
				return -1
			else:
				continue  # Inconclusive

		else:
			# Convert single integers to lists (string in this case, since that's what this method expects)
			if isinstance(leftElem, int):
				leftElem = f'[{leftElem}]'
			if isinstance(rightElem, int):
				rightElem = f'[{rightElem}]'

			result = processPacket(leftElem, rightElem)
			if result == 0:
				continue
			else:
				return result


	return 0  # If we got here, every test was inconclusive

with open('bigInput.txt') as fin:
	packetString = fin.read()
	packetString += '\n[[2]]\n[[6]]'


# https://stackoverflow.com/questions/2531952/how-to-use-a-custom-comparison-function-in-python-3

packets = packetString.split()  # Don't need to worry about comparing them in pairs, sort will do that for us
packets = sorted(packets, key=cmp_to_key(processPacket), reverse=True)  # cmp_to_key is not ideal, but it's easy

firstIndex = packets.index('[[6]]') + 1
secondIndex = packets.index('[[2]]') + 1
print('\n'.join(packets))

print(firstIndex, secondIndex, firstIndex*secondIndex)