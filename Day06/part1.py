from collections import deque

# Deques have a size limit, letting us automatically create a sliding window

def getPacketStart(inputString):
	inputString = inputString.strip()
	window = deque(maxlen=4)
	for i, l in enumerate(inputString):
		window.append(l)
		if len(set(window)) == 4:  # Every item of a set has to be unique, so it will only be length 4 if all letters are unique
			print(i+1)  # Should give us the index after the last indicator character
			break

with open('bigInput.txt') as fin:
	for l in fin:  # Final input only has one line, buit this makes for easier testing of the test inputs
		getPacketStart(l)  
