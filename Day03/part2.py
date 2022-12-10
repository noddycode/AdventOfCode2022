import string

valueDict = {letter:i+1 for i, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase)}

total = 0
with open('bigInput.txt') as fin:
	lines = fin.read().split()
	for i in range(0, len(lines), 3):
		line_sets = [set(line) for line in lines[i: i+3]]
		common = line_sets[0].intersection(*line_sets[1:]).pop()
		total += valueDict[common]

print(total)