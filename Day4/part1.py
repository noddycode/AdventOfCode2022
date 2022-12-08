# We could solve this with sets, but is there a logical way to do it with math?


# Take 1-4 and 2-3. If the first set contains the second, then 1-2 = -1 and 4-3 = 1.
# If we try the other way, 2-1 = 1 and 3-4 = -1
# Can we say, then, that if the signs are different, that one range contains the other?
# Let's try with overlapping sets
# 1-4 and 2-5. 1-2 = -1, 4-5 = -1. Both negative, does that mean they overlap?
# Now two sets that don't overlap at all
# 1-3 and 4-6. 1-4 = -3, 3-6 = -3. Hmm, also both negative.
# In this case we only need care about one set containing the other, let's focus on the rest in part 2

# How to handle sums that are 0?
# 1-4, 2-4, 1-2 = -1, 4-4 = 0. Included
# 1-4, 1-3, 1-1 = 0, 4-3 = 1. Also included...
# Hm, if we leave it 0, that would also fulfill our requirement of it not matching either sign
# But, we could have something like 1-4, 4-6, where the signs don't match but we still have a 0

# I give up, lets use sets

# total = 0
# with open('input.txt') as fin:
# 	for l in fin:
# 		pairs = l.strip().split(',')
# 		first_range = [int(n) for n in pairs[0].split('-')]
# 		second_range = [int(n) for n in pairs[1].split('-')]
# 		sums = [first_range[i]-second_range[i] for i in range(2)]
# 		signs = [n/abs(n) if n != 0 else 0 for n in sums]   # Get -1, +1, or 0
# 		if signs[0] != signs[1]:
# 			total += 1

# print(total)

total = 0
with open('bigInput.txt') as fin:
	for l in fin:
		pairs = l.strip().split(',')
		ranges = [set(range(int(r.split('-')[0]), int(r.split('-')[1])+1)) for r in pairs]
		if ranges[0].issubset(ranges[1]) or ranges[1].issubset(ranges[0]):
			total+= 1

print(total)