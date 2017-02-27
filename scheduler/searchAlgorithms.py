from datetime import date, datetime, timedelta
from random import shuffle,randint

from scheduler.models import NextPass,TLE
import itertools
import sys

class HillClimbing():

	def simple(satList, usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""

		bestNextPassList=[]
		print(" Starting simple hillclimbing")
		maxIterations = 50
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]
		curOrder=satList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			j=0
			for n in generatorOfAllNeighboursIncItself:
				if j==10:
					break
				listOfNearestNeighboursAndItself.append(list(n))
				j+=1
			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldNeighbourScore=sys.maxsize
			for neighbour in listOfNearestNeighbours:
				newNeighbourScore,nextPassList  = _Helper.fitnessFunction(neighbour,usefulTime)
				if(newNeighbourScore < oldNeighbourScore):
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					break;

			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				bestNextPassList = list(nextPassList)
				i=0
			else:
				i+=1
			#print(newScore)

			if i%maxIterations/10:
				print(".")
				
		if i==maxIterations:
			print(" Simple HillClimbing finished with the order ")
			# for n in curOrder:
			# 	pass
			# 	print(n)
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return oldScore,bestNextPassList

	def simpleRR(satList,usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""
		bestNextPassList=[]
		print(" Starting simple hillclimbing")
		maxIterations = 50
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]
		curOrder=satList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			j=0
			for n in generatorOfAllNeighboursIncItself:
				if j==10:
					break
				listOfNearestNeighboursAndItself.append(list(n))
				j+=1
			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldNeighbourScore=sys.maxsize
			for neighbour in listOfNearestNeighbours:
				newNeighbourScore,nextPassList  = _Helper.fitnessFunction(neighbour,usefulTime)
				if(newNeighbourScore < oldNeighbourScore):
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					break;

			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				bestNextPassList = list(nextPassList)
				i=0
			else:
				i+=1
			#print(newScore)

			if i%maxIterations/10:
				print(".")
				
		if i==maxIterations:
			print(" Simple HillClimbing finished with the order ")
			# for n in curOrder:
			# 	pass
			# 	print(n)
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return bestOrder

	def stochastic(satList,usefulTime):
		""" does not examine any neighbors before deciding how to move. 
		Rather, it selects a neighbor at random, and moves to that one
		if it is better."""

		print(" Starting stochastic hillclimbing")
		maxIterations = 1000
		i=0
		oldScore = sys.maxsize  
		newOrder=[]
		bestNextPassList=[]
		curOrder=satList
		while i<maxIterations:
			
			#swap two random elements
			i1 = randint(0,len(curOrder)-1)
			i2 = randint(0,len(curOrder)-1)
			swap1 = curOrder[i1]
			swap2 = curOrder[i2]

			curOrder[i2]=swap1
			curOrder[i1]=swap2

			newScore,nextPassList = _Helper.fitnessFunction(curOrder,usefulTime)
			#blah = _Helper.fitnessFunction(curOrder)
			#Could make it so it only changes when it's a lot better or a little better
			if newScore < oldScore:
				#use that 
				oldScore=newScore
				bestOrder=list(curOrder)
				bestNextPassList=list(nextPassList)
				i=0
			else:
				i+=1
			
			if i%(maxIterations/10)==0:
				print(".")

		#if i==maxIterations:
		print(" Stochastic HillClimbing finished with the order ")
		# for n in curOrder:
		# 	print(n)
		#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
		print("And a score of {}".format(oldScore))
		# for n in bestOrder:
		# 	print(n)
		# if type(newOrder2) is list:
		# 	print("it's a tlist")
		# 	print(newOrder2)
		# 	print(len(newOrder2))
		return oldScore, bestNextPassList

	def steepest(satList,usefulTime):
		""" Looks at as many neighbours as it can and picks the best
		neighbour it finds"""

		print(" Starting steepest hillclimbing")
		maxIterations = 50
		i=0
		oldScore = sys.maxsize   #just a really big number
		newOrder=[]
		curOrder=satList
		bestNextPassList=[]
		while i<maxIterations:
			
			listOfNearestNeighboursAndItself=[]
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			j=0
			for n in generatorOfAllNeighboursIncItself:
				if j==50:
					break
				listOfNearestNeighboursAndItself.append(list(n))
				j+=1

			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldSteepestScore=sys.maxsize
			steepestNeighbour=[]
			for neighbour in listOfNearestNeighbours:
				newSteepestScore,nextPassList = _Helper.fitnessFunction(neighbour,usefulTime)
				if(newSteepestScore<oldSteepestScore):
					oldSteepestScore=newSteepestScore
					steepestNeighbour=neighbour

			#found the steepest neighbout which is the one wit the best score ie the smallest number
			newScore=oldSteepestScore

			# #Could change so it only/ changes when it's a lot better or a little better
			if newScore < oldScore:
				#use that 
				#print("New Order")
				curOrder=steepestNeighbour
				oldScore=newScore
				bestNextPassList=list(nextPassList)
				i=0
			else:
				#print("Keep Order")
				i+=1
			#print(i)

			if i%(maxIterations/10)==0:
				print(".")	

		if i==maxIterations:
			print(" Steepest HillClimbing Finished with the order ")
			# for n in curOrder:
			# 	print(" {}".format(n.tle))
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return oldScore,bestNextPassList

	def randomRestart(satList,usefulTime):
		print(" Starting hillclimbing with random restart")

		curOrder=satList
		i=0
		maxIterations = 50
		newScore=0
		oldScore=sys.maxsize
		bestNextPassList=[]
		#shuffle(curOrder)
		while i<maxIterations:
			shuffle(curOrder)									# find a different starting point
			hillclimbing = HillClimbing.simpleRR(curOrder,usefulTime)		# find best order you can
			newScore,nextPassList = _Helper.fitnessFunction(hillclimbing,usefulTime)	# get the number from that order

			if(newScore<oldScore):
				oldScore=newScore
				curOrder=list(hillclimbing)
				bestOrder=list(curOrder)
				bestNextPassList=list(nextPassList)
			i+=1

		if i==maxIterations:
			print(" Random Restart HillClimbing finished with the order ")
			# for n in curOrder:
			# 	print(" {}".format(n.tle))
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return oldScore, bestNextPassList

class _Helper():
	def fitnessFunction(satList,usefulTime):

		"""Calling all the necessary parts in order
			and checking the priority is in order
			ensuring the order of the list"""

		#is priority maintained function goes here
		# prevSat=highpriority
		# for sat in satList:
		# 	if sat.priority<prevSat:
		# 		#priority order is violated
		# 		return sys.maxima

		nextPassList=[]
		satListConflictGroups = _Helper.__findConflictingGroups(satList)

		if len(satListConflictGroups)==0:
			#no conflicts
			return 0

		mergedGroups = _Helper.__mergeLists(satListConflictGroups)

		reorderedConflictGroups=[]
		for group in mergedGroups:
			reordered= [x for x in satList if x in group]
			reorderedConflictGroups.append(reordered)

		score,nextPassList = _Helper.__findSchedulableSatellites(reorderedConflictGroups,usefulTime)

		#print(score)
		#print(nextPassList)
		return score,nextPassList

	def __findConflictingGroups(satList):
		""" Compares each satellite with each other to find the ones
			that conflict at all with each other. 
			eg. if sat1 and sat2 conflict they are added to conflicts
			and sat3 and sat4 conflicts they added to conflicts but in a 
			different list/group
		"""
		satListConflicts=[]
		
		for i in range(len(satList)):
			conflicts=[]
			for j in range(i+1, len(satList)):
				#print('{} riseTime & {} setTime conflicts with {} riseTime & {} setTime'.format(satList[i].riseTime,satList[i].setTime,satList[j].riseTime,satList[j].setTime))
				if satList[i].riseTime <= satList[j].setTime and satList[i].setTime >= satList[j].riseTime:
					#they conflict
					#print('{} conflicts with {}'.format(satList[i],satList[j]))
					if satList[i] and satList[j] not in conflicts:
						conflicts.append(satList[i])
						conflicts.append(satList[j])

			if len(conflicts)>0:
				satListConflicts.append(list(set(conflicts)))

		return satListConflicts

	def __mergeLists(satListConflicts):
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


	def __findSchedulableSatellites(satListConflictGroups,usefulTime):
		""" The groups are now correct and the order was reestablished before 
		being passed in here. This goes through each sat in each group to find where
		each satellite conflicts with each other satellite. Compares these gaps
		with the transactionTime to figure out if this time available is useful to
		us. Checks with the blacklist. ie. times that are in use. If the space of gap
		is enough and that time isn't in use/conflicts we can schedule a satellite here 
		and that time period is then 'blacklisted' ie in use. 
		"""

		transactionTime = timedelta(minutes=usefulTime)
		nextPassList = []
		unScheduledSats = []
		allScheduledSats=[]
		for group in satListConflictGroups:
			blackList=[]
			scheduledSats=[]
			unScheduledSatFromGroup = []
			newPasses=[]
			for sat in group:
				conflicts=False
				curSatRise = 0
				curSatSet = 0
				for time in blackList:
					if sat.riseTime < time[1] and sat.setTime > time[0]:
						endGap = sat.setTime - (time[0]+transactionTime)
						if endGap<timedelta(0):
							endGap = endGap*-1
						frontGap = time[0] - sat.riseTime
						if frontGap<timedelta(0):
							frontGap = frontGap*-1

						#TODO: if frontGap and endGap both >= tt and we can
						#fit in either, pick one at random
						if endGap>=transactionTime:
							#can be fit in end gap
							#TODO: fit in some random place in end gap
							curSatRise = sat.setTime-transactionTime
							curSatSet = sat.setTime
							conflicts=False
						elif frontGap >= transactionTime:
							#can be fit in start gap
							#TODO: fit in some random place in front gap
							#print("fit in front gap")
							conflicts=False
							curSatRise = sat.riseTime
							curSatSet = sat.riseTime + transactionTime
						else:
							#can't fit in and we need another pass
							#print("adding")
							#unScheduledSats.append(sat.name)
							conflicts=True
							break

					else:
						curSatRise = sat.riseTime
						curSatSet = sat.riseTime + transactionTime
						conflicts=False

				tempTime = []
				if len(blackList)==0:
					##For first satellite to be scheduled
					curSatRise=sat.riseTime
					curSatSet = sat.riseTime + transactionTime
					tempTime = [curSatRise,curSatSet]
					scheduledSats.append(sat)
					blackList.append(tempTime)
					
					sat.riseTime=curSatRise
					sat.setTime=curSatSet
					newPasses.append(sat)

				if conflicts is False:
					#Check satellite doesn't conflict with 'blacklisted' times
					#before adding it
				
					conflictBlack = False
					tempTime = [curSatRise,curSatSet]
					for time in blackList:
						if tempTime[0] < time[1] and tempTime[1] > time[0]:
							conflictBlack=True
							break
						else:
							conflictBlack=False

					if conflictBlack != True:
						scheduledSats.append(sat)
						blackList.append(tempTime)

						sat.riseTime=curSatRise
						sat.setTime=curSatSet
						newPasses.append(sat)	
			
			#Find unscheduled satellites from scheduled
			unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
			unScheduledSats.append(unScheduledSatFromGroup)
			allScheduledSats.extend(scheduledSats)
			nextPassList.extend(newPasses)

		score=0
		for satList in unScheduledSats:

			score +=len(satList)
		#print(score) # want lowest.
		return score,nextPassList

