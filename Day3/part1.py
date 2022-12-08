import string

valueDict = {letter:i+1 for i, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase)}

total = 0
with open('bigInput.txt') as fin:
	for l in fin:
		l = l.strip()
		numItems = len(l)
		first_half = set(l[:numItems//2])
		second_half = set(l[numItems//2:])  # Inclusive first index, exclusive second index
		common = first_half.intersection(second_half).pop()
		total += valueDict[common]

print(total)