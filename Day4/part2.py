total = 0
with open('bigInput.txt') as fin:
	for l in fin:
		pairs = l.strip().split(',')
		ranges = [set(range(int(r.split('-')[0]), int(r.split('-')[1])+1)) for r in pairs]
		if ranges[0].intersection(ranges[1]):
			total+= 1

print(total)