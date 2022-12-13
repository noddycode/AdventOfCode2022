# As the worry levels get exponentially larger, our program slows down
# The examples given are surely trying to give us a hint about what to look for
# We are certainly removing a level of impercision by getting rid of the integer division
# What is it that they want us to figure out about the math involved here
# It said "you'll need tofind another way to keep your worry levels manageable"
# That must be a hint that we can do something else to the worry level to keep the results consistent

# Looking at their examples, the number of items inspected by each monkey increases at a fairly consistent rate
# The rate of increase seems unrelated to how many items they started with

# If we look at the number of items processed each round for each monkey, it ALMOST increases in a consistent pattern
# Do these numbers bear any relation to the monkey's divisor?

# Maybe there's some integer division at play here to explain the inconsistency
# Let's see if we can make any links between their divisor and/or operation

# An observation: the size of the increase is roughly proportional to the size of the divisor

import math

class Monkey():

	monkeyDict = {}
	commonMultiple = 0

	def __init__(self, inputText):
		lines = (l.strip() for l in inputText.split('\n'))  # Use a generator cause I'm lazy

		self.number = int(next(lines).split()[1].strip(':'))
		self.items = [int(i.strip()) for i in next(lines).split(':')[-1].split(',')]  # Gettin crazy with these one-liners
		self.operation, self.inputNumber = next(lines).split()[-2:]
		
		try:  # Handle values of "old"
			self.inputNumber = int(self.inputNumber)
		except ValueError:
			self.inputNumber = None

		self.divisor = int(next(lines).split()[-1])
		self.ifTrue = int(next(lines).split()[-1])
		self.ifFalse = int(next(lines).split()[-1])

		self.itemsProcessed = 0

		Monkey.monkeyDict[self.number] = self  # Let the monkey class keep track of its mates
		# Probably not great practice but... whatever

	def getNewWorryLevel(self, worryLevel):

		inputNumber = self.inputNumber
		if not inputNumber:
			inputNumber = worryLevel

		if self.operation == '*':
			worryLevel *= inputNumber
		elif self.operation == '+':
			worryLevel += inputNumber

		# Okay this works, but like... WHY?!
		worryLevel %= Monkey.commonMultiple

		return worryLevel

	def processItems(self):
		while self.items:
			item = self.items.pop(0)
			worryLevel = self.getNewWorryLevel(item)

			if worryLevel%self.divisor == 0:
				Monkey.monkeyDict[self.ifTrue].items.append(worryLevel)
			else:
				Monkey.monkeyDict[self.ifFalse].items.append(worryLevel)

			self.itemsProcessed += 1

	def __str__(self):
		lines = [
			f'Monkey: {self.number}',
			f'Divisor: {self.divisor}',
			f'Num Items: {len(self.items)}',
			f'Processed: {self.itemsProcessed}'
		]

		return '\n'.join(lines) 



with open('input.txt') as fin:
	monkeys = fin.read().split('\n\n')

for monkey in monkeys:
	Monkey(monkey)

# If we find a common multiple between all of our monkeys	
# Then dividing the worry level by it won't affect any checks
lestCommonMultiple = math.lcm(*(m.divisor for m in Monkey.monkeyDict.values()))
Monkey.commonMultiple = lestCommonMultiple

for i in range(10000):
	if i%100 == 0:
		print(i)

	for monkeyNumber, monkey in sorted(Monkey.monkeyDict.items()):
		# print('~~~~~~~~~~~~')
		# print(monkey)
		monkey.processItems()
		
	# print('\n\n')
		


print('\n'.join(f'Items processed by Monkey #{m.number}: {m.itemsProcessed}' for m in Monkey.monkeyDict.values()))

valueList = sorted((m.itemsProcessed for m in Monkey.monkeyDict.values()))

print(valueList[-1]*valueList[-2])