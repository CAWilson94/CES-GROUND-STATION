
class Pass():
	def __init__(self, name, start, end, duration):
		self.name = name
		self.start = start
		self.end = end
		self.duration = duration

	def passAsStr(self):
		return self.name + ": " +str(self.start) + " -> " + str(self.end)
	
passes = [
	Pass("a", 10, 12, 2), Pass("a", 22, 24, 2), Pass("a", 34, 36, 2), 
	Pass("b", 0, 1, 1), Pass("b", 4, 5, 1), Pass("b", 7, 8, 1), 
	Pass("c", 4, 6, 2), Pass("c", 16, 18, 2), Pass("c", 28, 30, 2), 
	Pass("d", 2, 5, 3), Pass("d", 14, 17, 3), Pass("d", 26, 29, 3), 
]

orderOfPasses = []

def conflicts(periodStart, periodEnd, passToCheck):
	if(passToCheck.start>periodStart and passToCheck.start < periodEnd):
		return True
	else:
		return False

aPass = passes[3];
try:
	print(str(passes.index(aPass)))
except ValueError:
	print("not found")
"""
	Rules for filtering the list of conflicts down to one satellite. 
		1. Highest Priority first
		2. The one that hasn't been looked at at all
		3. The one hasn't been looked at in the longest time
		4. The one that comes first chronologically
		5. Randomly chosen

	
	Rule 1: Filter by priority
		if only one is found with a higher priority
			add to order
		if more than one are found of the higher priority
			apply rule 2
		if none are found
			apply rule 2
	Rule 2: Filter by whether it has been picked at all. 
		if only one hasn't been picked before
			add it to order
		if more than one is found that hasn't been picked before
			apply rule 4
		if none are found that weren't picked before
			apply rule 3
	Rule 3: Find the largest index for each conflict
		sort the list by the index, choose the one with the smallest index. 

"""
"""
def findNext(conflicting):
	print("There were : " + str(len(conflicting)) + " conflics found:")
	if(conflicting):
		# Rule 1
		temp = conflicting
		chosenNext = temp[0]
		# Rule 2 look for one that hasn't been picked before
		for i in range(len(temp)):
			print(temp[i].name)
			# Remove the ones that have been seen before
			if chosenNext[i] in order:
				print(chosenNext[i].passAsStr() + " has been seen before, removing it.")
				del chosenNext[i]
			if(temp):
				if(len(temp) == 1):
					return temp[0]
				else:
					# more than one left, next rule
	return conflicting[1]

print("Initial list")
for aPass in passes: 
	print(str(aPass.start) + ",")

passes.sort(key=lambda x: x.start, reverse=False)

print("Sorted list")
for aPass in passes: 
	print(str(aPass.start) + ",")

i = 0
print("passes: " + str(len(passes)))
while(i < len(passes)):
	j = i + 1
	print("i: " + str(i) + ", j: " + str(j) + ", passes[i] is: " + passes[i].passAsStr())

	conflicting = []
	periodStart = passes[i].start
	periodEnd = passes[i].end

	while(j<len(passes)):
		if(conflicts(periodStart, periodEnd, passes[j])):
			conflicting.append(passes[j])
			if(passes[j].end > periodEnd):
				periodEnd = passes[j].end
			j += 1
		else:
			break
	if(conflicting):
		conflicting.append(passes[i])
		conflicting.sort(key=lambda x: x.start, reverse=False)
		print("Conflicts")
		for x in range(len(conflicting)):
			print(conflicting[x].name + ": " + str(conflicting[x].start) + " -> " + str(conflicting[x].end))
		nextPass = findNext(conflicting)
		print("Added: " + nextPass.passAsStr() + " from conflict res.")
		orderOfPasses.append(nextPass)
		i = j
	else:
		print("Added: " + passes[i].passAsStr())
		orderOfPasses.append(passes[i])
		i+=1

for i in range(len(orderOfPasses)):
	print(orderOfPasses[i].name + " : " +str(orderOfPasses[i].start) + " -> " + str(orderOfPasses[i].end))

"""

