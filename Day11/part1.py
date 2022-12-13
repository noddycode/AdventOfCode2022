


class Monkey():

	monkeyDict = {}

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

		worryLevel = worryLevel//3  # Integer divison automatically rounds down to the nearest integer

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



with open('bigInput.txt') as fin:
	monkeys = fin.read().split('\n\n')

for monkey in monkeys:
	Monkey(monkey)  # Don't need to assign it to anything cause it'll assign itself

for i in range(20):
	for monkeyNumber, monkey in sorted(Monkey.monkeyDict.items()):
		monkey.processItems()

print('\n'.join(f'Items processed by Monkey #{m.number}: {m.itemsProcessed}' for m in Monkey.monkeyDict.values()))

valueList = sorted((m.itemsProcessed for m in Monkey.monkeyDict.values()))

print(valueList[-1]*valueList[-2])