
class Pass():
	def __init__(self, name, start, end, duration):
		self.name = name
		self.start = start
		self.end = end
		self.duration = duration
	
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


def findNext(conflicting):
	print("There were : " + str(len(conflicting)) + " conflics found:")
	if(conflicting):
		temp = conflicting
		chosenNext = temp[0]
		#look for one that hasn't been picked before
		for i in range(len(temp)):
			print(temp[i].name)
			#if chosenNext[i] in order:
			#	print("")
			#	del chosenNext[i]
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
for i in range(len(passes)):
	j = i + 1
	print("i: " + str(i) + ", j: " + str(j))

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
		for x in range(len(conflicting)):
			print(conflicting[x].name + ": " + str(conflicting[x].start) + " -> " + str(conflicting[x].end))
		orderOfPasses.append(findNext(conflicting))
		i = j
	else:
		orderOfPasses.append(passes[i])

for i in range(len(orderOfPasses)):
	print(orderOfPasses[i].name + " : " +str(orderOfPasses[i].start) + " -> " + str(orderOfPasses[i].end))

	
