calories = set()

with open('bigInput.txt') as fin:
	total = 0
	for l in fin:
		l = l.strip()

		if not l:
			calories.add(total)
			total = 0
			continue

		total += (int(l))

print(max(calories))