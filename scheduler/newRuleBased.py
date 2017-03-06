from random import randint
import time 

CONFLICT_PADDING = 1 # mins added to the end of the conflict period
MIN_SUB_PASS_LEN = 3 # minimum lengh of pass to fill in the conflict window once a sat is chosen. 

	# 6 hrs = 360
	# 1 day = 1440
	# 2 days = 2880
	# 3 days = 4320
TIMEFRAME_MINS = 240 # total timeframe for passes
PASS_LEN_MAX = 8 # the longest a pass will be
PASS_LEN_MIN = 2  # the shortest a pass will be 
PRIORITY_MAX = 2 # The highest priority given to sats (commented out)
NUM_OF_PASSES = 25 # Max number of passes in initial array

DEBUG = False

DEBUG_LEVEL = 2

orderOfPasses = []

satelliteNames = ["a", "b", "c", "d", "e", "f", "g"]

priorities = [1, 1, 1, 0, 0, 1, 2]


class Pass():
	def __init__(self, name, start, end, duration, priority):
		self.name = name
		self.start = start
		self.end = end
		self.duration = duration
		self.priority = priority

	def passAsStr(self):
		return self.name + " (" + str(self.priority) + "): " +str(self.start) + " -> " + str(self.end )

#for i in range(len(satelliteNames)):
#	priorities.append(randint(0, PRIORITY_MAX))

def generatePass():
	satIndex = randint(0, len(satelliteNames)-1)
	name = satelliteNames[satIndex]
	duration = randint(0, PASS_LEN_MAX)
	while(duration < PASS_LEN_MIN):
		duration = randint(0, PASS_LEN_MAX)
	startTime = randint(0, TIMEFRAME_MINS) 
	endTime = startTime+duration
	priority = priorities[satIndex]
	return Pass(name, startTime, endTime, duration, priority)

def generatePasses():
	passes = []
	previousPass = generatePass()
	passes.append(previousPass)
	for i in range(NUM_OF_PASSES):
		newPass = generatePass()
		while(newPass == previousPass):
			newPass = generatePass()
		passes.append(newPass)

	return passes
	
	# passes = [
	#  	Pass("a", 10, 12, 2, 1), Pass("a", 22, 24, 1, 1), Pass("a", 34, 36, 2, 1), 
	#  	Pass("b", 0, 1, 1, 1), Pass("b", 4, 5, 1, 1), Pass("b", 7, 8, 1, 1), 
	#  	Pass("c", 4, 6, 2, 1), Pass("c", 16, 18, 2, 1), Pass("c", 28, 30, 2, 1), 
	#  	Pass("d", 2, 5, 3, 1), Pass("d", 14, 17, 3, 1), Pass("d", 26, 29, 3, 1), 
	# ]

	# aPass = passes[3];
	# try:
	# 	print(str(passes.index(aPass)))
	# 	print(passes[passes.index(aPass)].passAsStr())
	# except ValueError:
	# 	print("not found")

def lastIndex(list, value):
	# list[::-1] # reverses list
	# index finds the index from the reversed list
	# take this away from the lenght to get last index
	#return len(list) - list[::-1].index(value)
	index = 0
	temp = orderOfPasses[::-1]
	while(index < len(temp)):
		if(temp[index].name == value.name):
			return len(temp) - index
		index += 1
	return -1

# General checking if the pass is within conflicting time period
def conflicts(periodStart, periodEnd, passToCheck):
	if(passToCheck.start>=periodStart and passToCheck.start <= periodEnd):
		return True
	else:
		return False

# Rule 1
# Filter out low priority 
def filterPriority(conflicting):
	if(conflicting):
		highestPriority = conflicting[0].priority
		#print("Highest Priority: " + str(highestPriority))
		filtered = []

		for sat in conflicting:
			if(sat.priority == highestPriority):
				filtered.append(sat)
				#print("Added " + sat.passAsStr())
				
			if(sat.priority > highestPriority):
				filtered = []
				highestPriority = sat.priority
				filtered.append(sat)
				#print("Found new highest: " + str())

		if(filtered):
			return filtered

	return conflicting

# Rule 2
# Pick ones which haven't been picked yet
def filterByUnpicked(conflicting):
	if(conflicting):
		neverPicked = []
		for sat in conflicting:
			unpicked = True
			for aPass in orderOfPasses:
				if(aPass.name == sat.name):
					unpicked = False

			if(unpicked):
				#print("Not picked: " + sat.passAsStr())
				neverPicked.append(sat)
		if(neverPicked):
			return neverPicked

	return None

# Rule 3
# Pick the oldest one
def filterByOldest(conflicting):
	if(conflicting):
		oldestPass = conflicting[0]
		oldest = [oldestPass]
		oldestLastIndex = lastIndex(orderOfPasses, oldestPass)

		index = 0
		while(index < len(conflicting)):
			current = conflicting[index]
			currentLastIndex = lastIndex(orderOfPasses, current)
			if(currentLastIndex < oldestLastIndex):
				oldest = [conflicting[index]] # reset oldest list
				oldestPass = current
				oldestLastIndex = currentLastIndex
			elif(currentLastIndex == oldestLastIndex):
				oldest.append(conflicting[index])
			index += 1


		return oldest
	return None



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
	Rule 3: Find one which hasn't been picked in the longest time. 
		add it to the order
	Rule 4: Choose a radom one
		add it to the order

	Later change Rule 4 to:
	Rule 4.1: Find the one which leaves the lagest gap between the 
			  start or the end of the pass
		if one found
			add it to the order
		else 
			apply original Rule 4
		
"""

def findNext(conflicting, startTime, endTime):
	#print("There were : " + str(len(conflicting)) + " conflicts found:")
	if(conflicting):
		temp = conflicting
		chosen = temp[0]

		# Rule 1
		temp = filterPriority(temp)

		if(len(temp) == 1):
			if(DEBUG and DEBUG_LEVEL >= 3):
				print("Only one found with highest priority, returning: " + temp[0].passAsStr())
			return temp[0]

		unpicked = filterByUnpicked(temp)

		if(unpicked is not None):
			if(len(unpicked) == 1):
				if(DEBUG and DEBUG_LEVEL >= 3):
					print("Only one found which wasn't picked before, returning: " + unpicked[0].passAsStr())
				return unpicked[0]
			elif(len(unpicked) > 1):

				if(DEBUG and DEBUG_LEVEL >= 4):
					print("Unpicked:")
					for sat in unpicked:
						print(sat.passAsStr())

				returning = unpicked[randint(0, len(unpicked)-1)]
				if(DEBUG and DEBUG_LEVEL >= 3):
					print("Multiple not picked before, reurning random one: " + returning.passAsStr())
				return returning
				# Implement this when dealing with partial conflicts too. 
				# return filterByTimeSaved(temp, startTime, endTime)
			else: 
				print("No unpicked found")

		oldest = filterByOldest(temp)
		if(len(oldest) == 1):
			if(DEBUG and DEBUG_LEVEL >= 3):
				print("One oldest found, returning it: " + oldest[0].passAsStr())
			return oldest[0]
		elif(len(oldest) > 1):

			if(DEBUG and DEBUG_LEVEL >= 4):
				print("Oldest:")
				for sat in oldest:
					print(sat.passAsStr())


			returning = oldest[randint(0, len(oldest)-1)]
			if(DEBUG and DEBUG_LEVEL >= 3):
				print("Multiple oldest found, returning random one: " + returning.passAsStr())
			return returning
			# Implement this when dealing with partial conflicts too. 
			# return filterByTimeSaved(temp, startTime, endTime)

		# filter by most time saved
		# if multiple are found with similar times, 
		# 	 pick randomly
		# else if one is found
		# 	 return it

		# Work out largest gap from picked sat
		# Make a list of satellites which have more than MIN_PASS_LEN left in that gap
		# 

		
	if(DEBUG and DEBUG_LEVEL >= 3):
		print("*** Returning first item in conflicts ***")
	return conflicting[0]


			
def findNextRandomly(conflicts):
	return conflicts[randint(0, len(conflicts)-1)]


def fillBeforeChosen(conflicts, chosen):
	if(chosen in conflicts):
		del conflicts[conflicts.index(chosen)]

	conflicts.sort(key=lambda x: x.start, reverse=False)

	startTime = conflicts[0].start
	endTime = chosen.start - CONFLICT_PADDING

	counter = 0
	for sat in conflicts:
		if(sat.start > endTime):
			del conflicts[conflicts.index(sat)]
		counter += 1

	if(conflicts):
		bestFit = conflicts[0]
		bestTime = 0
		if(bestFit.end < endTime): 
			bestTime = bestFit.end - bestFit.start
		else: 
			bestTime = endTime - bestFit.start

		for sat in conflicts:
			satPeriod = 0 
			if(sat.end < endTime): 
				satPeriod = sat.end - sat.start
			else: 
				satPeriod = endTime - sat.start

			if(satPeriod > bestTime):
				bestTime = satPeriod
				bestFit = sat


		if(bestTime > MIN_SUB_PASS_LEN):
			start = bestFit.start
			end = bestFit.start + bestTime
			duration = end - start
			return Pass(bestFit.name, start, end, duration , bestFit.priority)
		else: 
			if(DEBUG and DEBUG_LEVEL >= 2):
				print("Nothing found before")
			return None
	else: 
		if(DEBUG and DEBUG_LEVEL >= 2):
			print("Nothing found before")
		return None

def fillAfterChosen(conflicts, chosen):

	if(chosen in conflicts):
		del conflicts[conflicts.index(chosen)]

	conflicts.sort(key=lambda x: x.start, reverse=False)

	startTime = chosen.end + CONFLICT_PADDING
	endTime = conflicts[len(conflicts)-1].end

	counter = 0
	for sat in conflicts:
		if(sat.end > startTime):
			del conflicts[conflicts.index(sat)]
		counter += 1

	if(conflicts):
		bestFit = conflicts[0]
		bestTime = 0
		if(bestFit.start > startTime): 
			bestTime = bestFit.end - bestFit.start
		else: 
			bestTime = bestFit.end - startTime

		for sat in conflicts:
			satPeriod = 0 
			if(bestFit.start > startTime): 
				satPeriod = sat.end - sat.start
			else: 
				satPeriod = sat.end - startTime

			if(satPeriod > bestTime):
				bestTime = satPeriod
				bestFit = sat

		if(bestTime > MIN_SUB_PASS_LEN):
			start = bestFit.end - bestTime
			end = bestFit.end
			duration = end - start
			return Pass(bestFit.name, start, end, duration , bestFit.priority)
		else: 
			if(DEBUG and DEBUG_LEVEL >= 2):
				print("Nothing found after")
			return None
	else: 
		if(DEBUG and DEBUG_LEVEL >= 2):
			print("Nothing found after")
		return None

def fillConflictWindow(conflicts, chosen):
	localSchedule = []
	localSchedule.append(chosen)

	satBefore = fillBeforeChosen(conflicts[:], chosen)
	if(satBefore is not None):
		localSchedule.append(satBefore)

	satAfter = fillAfterChosen(conflicts[:], chosen)
	if(satAfter is not None):
		localSchedule.append(satAfter)

	localSchedule.sort(key=lambda x: x.start, reverse=False)

	return localSchedule



def getOrderedList(passes):
	# Sort from earliest first
	passes.sort(key=lambda x: x.start, reverse=False)

	if(DEBUG and DEBUG_LEVEL >= 2):
		print("Passes: " + str(len(passes)))
		print("Sorted list")
		for aPass in passes: 
			print(aPass.passAsStr())

	if(DEBUG and DEBUG_LEVEL >= 1):
		print("")

	i = 0
	conflictsNum = 0

	#for each satellites
	while(i < len(passes)):
		j = i + 1
		# find time window of conflic
		conflicting = []
		periodStart = passes[i].start 
		periodEnd = passes[i].end + CONFLICT_PADDING

		while(j<len(passes)):
			# find all satellites which start in the time window.
			if(conflicts(periodStart, periodEnd, passes[j])):
				conflicting.append(passes[j])
				if(passes[j].end > periodEnd):
					periodEnd = passes[j].end + CONFLICT_PADDING
				j += 1
			else:
				break
		# if any were found
		if(conflicting):
			conflicting.append(passes[i])
			conflicting.sort(key=lambda x: x.start, reverse=False)

			if(DEBUG and DEBUG_LEVEL >= 2):
				print("Conflicts")
				for x in range(len(conflicting)):
					print(conflicting[x].passAsStr())
				print("---------")

			# resolve the conflict
			nextPass = findNext(conflicting, periodStart, periodEnd)

			filledWindow = fillConflictWindow(conflicting, nextPass)
			#nextPass = findNextRandomly(conflicting)
			if(DEBUG and DEBUG_LEVEL >= 1):
				for sat in filledWindow: 
					print("Added: " + sat.passAsStr() + " from conflict res.")
			# append to the order
			for sat in filledWindow:
				orderOfPasses.append(sat)
			conflictsNum += 1
			# skip alland DEBUG_LEVEL >= 1 sats which were conflicting
			# change this to find conflicts from end of sat selected to end of conflict window for sats > 4 mins
			i = j
		else:
			# no conflicts add and move on to next sat
			if(DEBUG and DEBUG_LEVEL >= 1):
				print("Added: " + passes[i].passAsStr())
			orderOfPasses.append(passes[i])

			i = i+ 1

	if(DEBUG and DEBUG_LEVEL >= 1):
		print("Num of conflicts resolved: " + str(conflictsNum))

	return orderOfPasses


timeStart = time.clock()
orderOfPasses = getOrderedList(generatePasses())
timeEnd = time.clock()

print("Order: ")
print(orderOfPasses[0].passAsStr())	
a = 1
errors  = 0
while(a < len(orderOfPasses)):
	if(orderOfPasses[a].start < orderOfPasses[a-1].end):
		print("This one starts before the previous one ends")
		errors += 1
	print(orderOfPasses[a].passAsStr())	
	a+= 1
print("---------------")
print("Num of passes: " + str(NUM_OF_PASSES))
print("Num of passes ordered: " + str(len(orderOfPasses)))
print("Num of Errors: " + str(errors))
print("Time taken: %s seconds" % (timeEnd - timeStart))

print("\n\n")
numOfIterations = 100000
totalPasses = 0
for i in range(numOfIterations):
	orderOfPasses = []
	timeStart = time.clock()
	orderOfPasses = getOrderedList(generatePasses())
	timeEnd = time.clock()
	print("Num of passes ordered: " + str(len(orderOfPasses)))
	totalPasses += len(orderOfPasses)
	print("Time taken: %s seconds" % (timeEnd - timeStart))
	print("---------------")

print("On average found: " + str(totalPasses/numOfIterations))
# passes = generatePasses()
# for i in range(50):
# 	chromo = []
# 	chromo = getOrderedList(passes)
# 	chromoStr = ""
# 	for thing in chromo:
# 		chromoStr = chromoStr + thing.passAsStr() + ", "
# 	print(chromoStr)
# 	orderOfPasses = []

