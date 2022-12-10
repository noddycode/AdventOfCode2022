point_dict = {
	'X': 1,
	'Y': 2,
	'Z': 3
}

equivalence_dict = {
	'A': 'X',
	'B': 'Y',
	'C': 'Z'
}

win_dict = {
	'A': 'Z',
	'B': 'X',
	'C': 'Y'
}


total = 0
with open('bigInput.txt') as fin:
	for l in fin:
		theirs, mine = l.strip().split()
		total += point_dict[mine]  # Points for shape
		if equivalence_dict[theirs] == mine:  # Draw
			total += 3
		elif win_dict[theirs] == mine:  # Lose
			continue
		else:  # Win
			total += 6


print(total)

