import itertools

# Part 1: Get the crate inputs

crate_stacks = []

with open('bigInput.txt') as fin:
	crates = itertools.takewhile(lambda x: x.strip(), fin)  # Take lines until we reach the blank line
	crates = list(crates)
	crate_nums = [int(n.strip()) for n in crates.pop().split() if n.strip()]
	for i in range(crate_nums.pop()):
		crate_stacks.append([])  # Now we have a "stack" for each crate stack

	for l in crates:  # Now get each crate and add it to the appropriate stack
		crate_sections = [l[i:i+4].strip().strip('[]') for i in range(0, len(l), 4)]
		for i, c in enumerate(crate_sections):
			if c:
				crate_stacks[i].insert(0, c)

	# Now process the reest of the file
	for l in fin:
		parts = l.strip().split()
		num_moved = int(parts[1])
		from_stack = int(parts[3]) - 1  # Indecies are 0-based
		to_stack = int(parts[5]) - 1
		for i in range(num_moved):
			crate_stacks[to_stack].append(crate_stacks[from_stack].pop())

print(''.join(stack.pop() for stack in crate_stacks))