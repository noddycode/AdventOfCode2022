calories = []  # In case we have duplicates

with open('bigInput.txt') as fin:
	total = 0
	for l in fin:
		l = l.strip()

		if not l:
			calories.append(total)
			total = 0
			continue

		total += (int(l))

	calories.append(total) # Clean up last input

grand_total = 0
for i in range(3):
	cal = max(calories)
	grand_total += cal
	calories.remove(cal)

print(grand_total)