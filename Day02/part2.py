point_dict = {
	'A': 1,
	'B': 2,
	'C': 3
}

lose_dict = {
	'A': 'C',
	'B': 'A',
	'C': 'B'
}

win_dict = {value: key for key, value in lose_dict.items()}


total = 0
with open('bigInput.txt') as fin:
	for l in fin:
		theirs, condition = l.strip().split()
		mine = ''
		if condition == 'X':  # Lose
			mine = lose_dict[theirs]  # Choose the one that lets them win
		elif condition == 'Y':  # Draw
			mine = theirs
			total += 3
		else:  # Win
			mine = win_dict[theirs]
			total += 6

		total += point_dict[mine] 
		


print(total)

