with open('bigInput.txt') as fin:
	instructions = [l for l in fin.readlines()] + [""]  # Poison pill
	instructions = (l for l in instructions)  # Use a generator so we don't have to keep track of where we are



cycle = 1  # Not 0 indexed :(
x = 1
currentInstruction = next(instructions)
instructionCycle = 0  # Keep track of how many cycles we've been processing each instruction
done = False
signalSum = 0

while True:
	# Do this check here, as register only changes AFTER the cycle
	if cycle == 20 or (cycle-20)%40 == 0:  # Remainder is 0, so must be multiple of 40
		signal = x * cycle
		signalSum += signal
		print(f'Signal Strength: {signal}\nSum: {signalSum}\nCurrent X: {x}\nCurrent Cycle: {cycle}\n')


	if done:
		done = False
		instructionCycle = 0
		currentInstruction = next(instructions)

	args = currentInstruction.split()
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

		

