from itertools import zip_longest

# I smell recursion

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
def processPacket(left, right):
	left = parsePacket(left)
	right = parsePacket(right)

	for leftElem, rightElem in zip_longest(left, right):
		# If one of these runs out before we return a value, handle it here
		if leftElem == None:
			return True
		elif rightElem == None:
			return False

		# print(rightElem, leftElem)
		if all(isinstance(e, int) for e in (leftElem, rightElem)):  # Both ints
			if leftElem < rightElem:
				return True
			elif leftElem > rightElem:
				return False
			else:
				continue  # Inconclusive

		else:
			# Convert single integers to lists (string in this case, since that's what this method expects)
			if isinstance(leftElem, int):
				leftElem = f'[{leftElem}]'
			if isinstance(rightElem, int):
				rightElem = f'[{rightElem}]'

			result = processPacket(leftElem, rightElem)
			if result == "I dunno":
				continue
			else:
				return result


	return "I dunno"  # If we got here, every test was inconclusive

with open('bigInput.txt') as fin:
	packetStrings = fin.read()

correctPackets = 0	
for i, packetGroup in enumerate(packetStrings.split('\n\n')):
	packets = packetGroup.split()
	result = processPacket(*packets)
	if result == True:  # Don't want to include an inconclusive
		correctPackets += i+1  # Non-zero indeces, grr...
		print(i+1)

print(correctPackets)