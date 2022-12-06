from collections import deque

# Deques have a size limit, letting us automatically create a sliding window

def getPacketStart(inputString):
	inputString = inputString.strip()
	window = deque(maxlen=14)
	for i, l in enumerate(inputString):
		window.append(l)
		if len(set(window)) == 14:  # Deques just make life simpler
			print(i+1)  # Should give us the index after the last indicator character
			break

with open('bigInput.txt') as fin:
	for l in fin:  # Final input only has one line, buit this makes for easier testing of the test inputs
		getPacketStart(l)  
