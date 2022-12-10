import itertools

with open('bigInput.txt') as fin:
	instructions = [l for l in fin.readlines()] + [""]  # Poison pill
	instructions = (l for l in instructions)  # Use a generator so we don't have to keep track of where we are


pixels = ['.' for _ in range(240)]  # Keep it a simple array, we'll split it into lines later

cycle = 1  # Not 0 indexed :(
x = 1
currentInstruction = next(instructions)
instructionCycle = 0  # Keep track of how many cycles we've been processing each instruction
done = False

while True:

	if done:
		done = False
		instructionCycle = 0
		currentInstruction = next(instructions)

	args = currentInstruction.split()  # Move this up so we don't end up past end of screen

	posOnRow = (cycle-1)%40 # Will tell us how far into the row the CRT is
	if x-1 <= posOnRow <= x+1:  # Check if CRT is drawing on x's position
		pixels[cycle-1] = '#'

	if not args:
		break
	if args[0] == "noop":
		done = True
	else:
		if instructionCycle == 1:
			value = int(args[1])
			x += value
			done = True

	cycle += 1
	instructionCycle += 1

# Split each line at 40 pixels
for line, pixelGroup in itertools.groupby(enumerate(pixels), lambda x: x[0]//40):

	drawPixels = [x[1] for x in pixelGroup]
	print(''.join(drawPixels))


