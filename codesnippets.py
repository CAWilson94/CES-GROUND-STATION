Simple

currentSolution = startingSolution
oldScore = -INF
loop do 
	neighbours = getNeighbours(currentSoution)
	for n in neighbours
		newScore = getFitness(n)
		if(newScore > oldScore)
			nextSolution = n
			oldScore = newScore
			exit for loop
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


Steepest

currentSolution = startingSolution
oldScore = -INF
loop do 
	neighbours = getNeighbours(currentSoution)
	for n in neighbours
		newScore = getFitness(n)
		if(newScore > oldScore)
			nextSolution = n
			oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


stochastic

currentSolution = startingSolution
oldScore = -INF
loop do 
		j = getRandomInt()
		k = getRandomInt()

		swap1=currentSolution[k]
		swap2=currentSolution[j]

		currentSolution[j]=swap1
		currentSolution[k]=swap2

		newScore = getFitness(currentSolution)

		if(newScore > oldScore)
			bestSolution = currentSolution
			oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


RR

currentSoution = startingSolution
oldScore = - INF
loop do 
	shuffle(currentSolution)
	newSolution = simpleHC(currentSolution)
	newScore = getFitness(bestSolution)
	if(newScore > oldScore)
		bestSolution =  newSolution
		oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution




class PriceStrategy():
	def cost(baseCost):
		pass

class NormalPrice(PriceStrategy):
	def cost(baseCost):
		return baseCost

class SalePrice(PriceStrategy):
	def cost(baseCost):
		return baseCost*.8

priceStrategy = NormalPrice()

price = priceStrategy.cost(10)
price = 10

priceStrategy = SalePrice()

price = priceStrategy.cost(10)
price = 8


class MissionView(APIView):

	def get(self, request):
			...
		serializer = MissionSerializer(missionList, many=True)         
		return Response(serializer.data)

	def post(self, request):
			...
		return Response({'Creation Successful': request.data.get("name")} ,status=status.HTTP_201_CREATED)

	def delete(self, request):
			...
		return Response({'Deleted Successful':deleted},status=status.HTTP_200_OK)


scheduler = MOTSimpleHC()
scheduler = MOTSteepestHC()
scheduler = MOTStochasticHC()
scheduler = MOTRandomRestartHC()
scheduler = MOTRuleBased()
scheduler = MOTGA()








from datetime import date, datetime, timedelta
from random import shuffle,randint
from ..services import Services
from ..models import  TLE, Mission, NextPass
import sys

class _Helper():


	def fitnessFunction(self, nextPassList,usefulTime):
		"""Calling all the necessary parts in order
			and checking the priority is in order
			ensuring the order of the list"""

		conflictGroups = _Helper._findConflictingGroups(nextPassList)

		if len(conflictGroups)==0:
			#no conflicts
			return [0,nextPassList]



		mergedGroups = _Helper._mergeLists(conflictGroups)
		
		#print("mergegroups")
		#print (mergedGroups)

		reorderedConflictGroups=[]
		for group in mergedGroups:
			reordered= [x for x in nextPassList if x in group]
			reorderedConflictGroups.append(reordered)

		scheduledNextPassList=[]
		
		scheduledNextPassList = _Helper._findSchedulableSatellites(reorderedConflictGroups,usefulTime)

		#print("processedNextPassList")
		#print(processedNextPassList)

		#add in satellites that don't conflict with any
		noConflictList=[]
		for Pass in nextPassList:
			notInGroup=True
			for group in mergedGroups:
				if Pass in group:
					notInGroup=False
			if notInGroup:
				noConflictList.append(Pass)
		noConflictList=set(noConflictList)
		#print("noConflictList")
		#print(noConflictList)
		for sat in noConflictList:
			scheduledNextPassList.append(sat)
				
		scheduledNextPassList=set(scheduledNextPassList)


		#print("final score = {} - {}".format(len(nextPassList),len(processedNextPassList)))
		score = len(nextPassList)-len(scheduledNextPassList)
		return [score,scheduledNextPassList]



	def getPassesFromMissions(self, missions):

		TIME_HOURS = 72
		
		passes = []

		dateNow = datetime.utcnow()

		print("Total missions: " + str(len(missions)))
		i = 0
		for m in missions:
			i += 1

			tleEntry = m.TLE
			try:
				nextPass = Services.getNextPass(self, tleEntry, m, dateNow)
				passes.append(nextPass)
			
				while(nextPass.setTime < (dateNow + timedelta(hours=TIME_HOURS))):
					time = nextPass.setTime + timedelta(minutes=1)
					try:
						nextPass = Services.getNextPass(self, tleEntry, m, time)
						passes.append(nextPass)
						
					except ValueError: 
						break

				print("Finding passes for the next " + str(TIME_HOURS) + " hours, found: " + str(len(passes)) + ", now looking at " + str(i) + " : " + m.TLE.name)
			except ValueError: 
					print("No pass was found for " + tleEntry.name + " over groundstation in the next 36 hours.")
		return passes


	def getNextPass(self,missionList):
		"""Gets a single pass for each mission"""
		nextPassListStart=[]
		for mission in missionList:
			nextPass = Services.getNextPass(self, mission.TLE ,mission, datetime.utcnow())
			#print(nextPass)
			dur=nextPass.setTime - nextPass.riseTime
			if(dur<timedelta(0)):
				print(nextPass.tle.name)
			nextPassListStart.append(nextPass)

		return nextPassListStart


	def _findConflictingGroups(satList):
		""" Compares each satellite with each other to find the ones
			that conflict at all with each other. 
			eg. if sat1 and sat2 conflict they are added to conflicts
			and sat3 and sat4 conflicts they added to conflicts but in a 
			different list/group
		"""
		satListConflicts=[]

		for i in range(len(satList)):
			conflicts=[]
			noConflicts=[]
			for j in range(i+1, len(satList)):
				#print('{} riseTime & {} setTime compared with {} riseTime & {} setTime'.format(satList[i].riseTime,satList[i].setTime,satList[j].riseTime,satList[j].setTime))
				if satList[i].riseTime < satList[j].setTime and satList[i].setTime > satList[j].riseTime:
					#they conflict
					#print('{} conflicts with {}'.format(satList[i],satList[j]))
					if satList[i] and satList[j] not in conflicts:
						# print(satList[i])
						# print(satList[i].mission)
						# print(satList[i].mission.priority)
						if satList[i].mission.priority >  satList[j].mission.priority:
							conflicts.append(satList[i])
						elif satList[i].mission.priority <  satList[j].mission.priority:
							conflicts.append(satList[j])
						else:
							conflicts.append(satList[i])
							conflicts.append(satList[j])
						# conflicts.append(satList[i])
						# conflicts.append(satList[j])
			if len(conflicts)>0:
				satListConflicts.append(list(set(conflicts)))

		return satListConflicts

	def _mergeLists(satListConflicts):
		""" findConflictingGroups work isn't finished, it is continued here. 
			If any list shares one or more element with another list then 
			they should really be one list/group
			eg. if sat1 and sat2 conflict, and sat2 and sat3 conflict,
			findConflictingGroups would put them in two different lists but
			merge lists combines them into a group even though sat1 and 
			sat3 don't conflict 
		"""

		prevSatConlicts = []
		while len(satListConflicts) != len(prevSatConlicts):
			finaListsConflictsTrimmed=[]
			finaListsConflicts = []

			for i in range(len(satListConflicts)):
				subList = satListConflicts[i]
				
				"Gets all the lists that share elements with subList"
				c3 = [list(filter(lambda x: x in subList, satListConflicts[subListIndex])) for subListIndex in range(len(satListConflicts))]
				
				#return an iterator from the elements of iterable where function return true
				#http://stackoverflow.com/questions/642763/python-intersection-of-two-lists
				
				"Combines those lists into one list"
				c4 = []
				for z in range(len(c3)):
					if (c3[z] != []):
						c4 = list(set(satListConflicts[z]) | set(subList))
						subList = c4
				finaListsConflicts.append(subList)

			"Gets rid of duplicate lists"
			for i in finaListsConflicts:
				if i not in finaListsConflictsTrimmed:
					finaListsConflictsTrimmed.append(i)
			#prev                 #new
			prevSatConlicts = satListConflicts
			satListConflicts =  finaListsConflictsTrimmed

		return finaListsConflictsTrimmed


	# def _dropRandom(satListConflictGroups):


	# 	transactionTime = timedelta(minutes=usefulTime)
	# 	nextPassList = []
	# 	unScheduledSats = []
	# 	allScheduledSats=[]
	# 	for group in satListConflictGroups:
	# 		blackList=[]
	# 		scheduledSats=[]
	# 		unScheduledSatFromGroup = []
	# 		newPasses=[]
	# 		for sat in group:
	# 			conflicts=False
	# 			curSatRise=0
	# 			curSatSet=0
	# 			setWhen=""
				

	# def _findSchedulableSatellites(satListConflictGroups,usefulTime):
	# 	""" The groups are now correct and the order was reestablished before 
	# 	being passed in here. This goes through each sat in each group to find where
	# 	each satellite conflicts with each other satellite. Compares these gaps
	# 	with the transactionTime to figure out if this time available is useful to
	# 	us. Checks with the blacklist. ie. times that are in use. If the space of gap
	# 	is enough and that time isn't in use/conflicts we can schedule a satellite here 
	# 	and that time period is then 'blacklisted' ie in use. 
	# 	"""

	# 	transactionTime = timedelta(minutes=usefulTime)
	# 	nextPassList = []
	# 	unScheduledSats = []
	# 	allScheduledSats=[]
	# 	for group in satListConflictGroups:
	# 		blackList=[]
	# 		scheduledSats=[]
	# 		unScheduledSatFromGroup = []
	# 		newPasses=[]
	# 		for sat in group:
	# 			conflicts=False
	# 			curSatRise=0
	# 			curSatSet=0
	# 			setWhen=""
	# 			for time in blackList:


					if sat.riseTime < time[1] and sat.setTime > time[0]:
						
						endGap = sat.setTime - (time[0]+transactionTime)
						if endGap<timedelta(0):
							endGap = endGap*-1

						frontGap = time[0] - sat.riseTime
						if frontGap<timedelta(0):
							frontGap = frontGap*-1

						if endGap>=transactionTime:
							curSatRise = sat.setTime-transactionTime
							curSatSet = sat.setTime
							conflicts=False
						elif frontGap >= transactionTime:

							curSatRise = sat.riseTime
							curSatSet = sat.riseTime + transactionTime
							conflicts=False
						else:
							conflicts=True
							break

					else:
						curSatRise = sat.riseTime
						curSatSet = sat.riseTime + transactionTime
						conflicts=False

						...

				# if conflicts is False:

				# 	conflictBlack = False
				# 	tempTime = [curSatRise,curSatSet]
				# 	for time in blackList:
				# 		if tempTime[0] < time[1] and tempTime[1] > time[0]:
				# 			conflictBlack=True
				# 			break
				# 		else:
				# 			conflictBlack=False

				# 	if conflictBlack != True:
				# 		scheduledSats.append(sat)
				# 		blackList.append(tempTime)

				# 		sat.riseTime=curSatRise
				# 		sat.setTime=curSatSet
				# 		sat.duration=transactionTime
				# 		sat.maxElevation=setWhen
				# 		newPasses.append(sat)	
			
			#Find unscheduled satellites from scheduled
			unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
			unScheduledSats.append(unScheduledSatFromGroup)
			allScheduledSats.extend(scheduledSats)
			nextPassList.extend(newPasses)

		# score=0
		# for satList in unScheduledSats:
		# 	score +=len(satList)
		return nextPassList




		tempTime = []
				if len(blackList)==0:
					curSatRise=sat.riseTime
					curSatSet=sat.setTime
					tempTime = [curSatRise,curSatSet]
					scheduledSats.append(sat)
					blackList.append(tempTime)
					newPasses.append(sat)
