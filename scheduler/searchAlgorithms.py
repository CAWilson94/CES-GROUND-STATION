from datetime import date, datetime, timedelta
from random import shuffle,randint

from scheduler.models import NextPass,TLE
import itertools
import sys

class HillClimbing():

	def simple(satList):
		""" In simple hill climbing, the first closer node is chosen"""

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
				newNeighbourScore  = _Helper.fitnessFunction(neighbour)
				if(newNeighbourScore < oldNeighbourScore):
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					break;

			if newScore < oldScore:
				oldScore=newScore
				bestOrder = curOrder
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

	def stochastic(satList):
		""" does not examine any neighbors before deciding how to move. 
		Rather, it selects a neighbor at random, and moves to that one
		if it is better."""

		print(" Starting stochastic hillclimbing")
		maxIterations = 1000
		i=0
		oldScore = sys.maxsize  
		newOrder=[]
		curOrder=satList
		while i<maxIterations:
			
			#swap two random elements
			i1 = randint(0,len(curOrder)-1)
			i2 = randint(0,len(curOrder)-1)
			swap1 = curOrder[i1]
			swap2 = curOrder[i2]

			curOrder[i2]=swap1
			curOrder[i1]=swap2

			newScore = _Helper.fitnessFunction(curOrder)
			
			#Could make it so it only changes when it's a lot better or a little better
			if newScore < oldScore:
				#use that 
				oldScore=newScore
				bestOrder=list(curOrder)
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
		return bestOrder

	def steepest(satList):
		""" Looks at as many neighbours as it can and picks the best
		neighbour it finds"""

		print(" Starting steepest hillclimbing")
		maxIterations = 50
		i=0
		oldScore = sys.maxsize   #just a really big number
		newOrder=[]
		curOrder=satList
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
				newSteepestScore = _Helper.fitnessFunction(neighbour)
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
			return curOrder

	def randomRestart(satList):
		print(" Starting hillclimbing with random restart")

		curOrder=satList
		i=0
		maxIterations = 50
		newScore=0
		oldScore=sys.maxsize

		#shuffle(curOrder)
		while i<maxIterations:
			shuffle(curOrder)									# find a different starting point
			hillclimbing = HillClimbing.simple(curOrder)		# find best order you can
			newScore = _Helper.fitnessFunction(hillclimbing)	# get the number from that order

			if(newScore<oldScore):
				oldScore=newScore
				curOrder=list(hillclimbing)
				bestOrder=list(curOrder)
			i+=1

		if i==maxIterations:
			print(" Random Restart HillClimbing finished with the order ")
			# for n in curOrder:
			# 	print(" {}".format(n.tle))
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return bestOrder

class _Helper():
	def fitnessFunction(satList):

		"""Calling all the necessary parts in order
			and checking the priority is in order
			ensuring the order of the list"""

		#is priority maintained function goes here
		# prevSat=highpriority
		# for sat in satList:
		# 	if sat.priority<prevSat:
		# 		#priority order is violated
		# 		return sys.maxima
			
		satListConflictGroups = _Helper.__findConflictingGroups(satList)

		if len(satListConflictGroups)==0:
			return 0

		mergedGroups = _Helper.__mergeLists(satListConflictGroups)

		reorderedConflictGroups=[]
		for group in mergedGroups:
			reordered= [x for x in satList if x in group]
			reorderedConflictGroups.append(reordered)

		score = _Helper.__findSchedulableSatellites(reorderedConflictGroups)

		#print(score)
		return score

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


	def __findSchedulableSatellites(satListConflictGroups):
		""" The groups are now correct and the order was reestablished before 
		being passed in here. This goes through each sat in each group to find where
		each satellite conflicts with each other satellite. Compares these gaps
		with the transactionTime to figure out if this time available is useful to
		us. Checks with the blacklist. ie. times that are in use. If the space of gap
		is enough and that time isn't in use/conflicts we can schedule a satellite here 
		and that time period is then 'blacklisted' ie in use. 

		"""
		transactionTime = timedelta(minutes=3)
		nextPassList = []
		unScheduledSats = []
		for group in satListConflictGroups:
			blackList=[]
			scheduledSats=[]
			unScheduledSatFromGroup = []
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
			
			#Find unscheduled satellites from scheduled
			unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
			unScheduledSats.append(unScheduledSatFromGroup)
			nextPassList.append(scheduledSats)

		#Count number of unscheduled
		score=0
		for satList in unScheduledSats:
			score +=len(satList)
		#print(score) # want lowest.
		return score

class blah():

	def test_findSchedulableSatellites_many_real_sats():


		catAOS = datetime(2017,1,25,0,52,59)
		catLOS = datetime(2017,1,25,1,4,28)
		sixtysevenCAOS = datetime(2017,1,25,0,6,52)
		sixtysevenCLOS = datetime(2017,1,25,0,14,42)
		sixtysevenDAOS = datetime(2017,1,25,0,8,37)
		sixtysevenDLOS = datetime(2017,1,25,0,16,18)
		aistAOS = datetime(2017,1,25,0,35,21)
		aistLOS = datetime(2017,1,25,0,48,8)
		beesatAOS = datetime(2017,1,25,0,46,48)
		beesatLOS = datetime(2017,1,25,1,0,4) 
		briteAOS = datetime(2017,1,25,0,19,39)
		briteLOS = datetime(2017,1,25,0,30,4)
		cubebugAOS = datetime(2017,1,25,0,41,54)
		cubebugLOS = datetime(2017,1,25,0,52,49)
		sailAOS = datetime(2017,1,25,0,41,17)
		sailLOS = datetime(2017,1,25,0,53,28)
		eagleAOS = datetime(2017,1,25,0,53,13)
		eagleLOS = datetime(2017,1,25,1,2,56)	
		exoAOS = datetime(2017,1,25,0,57,27)
		exoLOS = datetime(2017,1,25,1,5,27)
		fconeAOS = datetime(2017,1,25,0,17,14)
		fconeLOS = datetime(2017,1,25,0,30,6)
		fcthreeAOS = datetime(2017,1,25,0,11,3)
		fcthreeLOS = datetime(2017,1,25,0,23,54)
		fcfiveAOS = datetime(2017,1,25,0,8,47)
		fcfiveLOS = datetime(2017,1,25,0,21,37)
		fceightAOS = datetime(2017,1,25,0,52,35)
		fceightLOS = datetime(2017,1,25,1,5,21)
		fcnineAOS = datetime(2017,1,25,0,50,43)
		fcnineLOS = datetime(2017,1,25,1,3,31)
		fctenAOS = datetime(2017,1,25,0,53,57)
		fctenLOS = datetime(2017,1,25,1,6,40)
		fcelevenAOS = datetime(2017,1,25,0,59,45)
		fcelevenLOS = datetime(2017,1,25,1,12,25)	
		fethirteenAOS = datetime(2017,1,25,1,7,32)
		fethirteenLOS = datetime(2017,1,25,1,15,6)	
		fefourteenAOS = datetime(2017,1,25,0,0,33)
		fefourteenLOS = datetime(2017,1,25,0,8,13)	
		itupAOS = datetime(2017,1,25,0,22,12)
		itupLOS = datetime(2017,1,25,0,34,49)	

		catTLE = TLE(0,"cat","line1","line2")
		sixtysevenCTLE = TLE(1,"sixtysevenC","line1","line2")
		sixtysevenDTLE= TLE(1,"sixtysevenD","line1","line2")
		aistTLE= TLE(1,"aist","line1","line2")
		beesatTLE= TLE(1,"beesat","line1","line2")
		briteTLE= TLE(1,"brite","line1","line2")
		cubebugTLE= TLE(1,"cubebug","line1","line2")
		sailTLE= TLE(1,"sail","line1","line2")
		eagleTLE= TLE(1,"eagle","line1","line2")
		exoTLE= TLE(1,"exo","line1","line2")
		fconeTLE= TLE(1,"fcone","line1","line2")
		fcthreeTLE= TLE(1,"fcthree","line1","line2")
		fcfiveTLE= TLE(1,"fcfive","line1","line2")
		fceightTLE	= TLE(1,"fceight","line1","line2")
		fcnineTLE= TLE(1,"fcnine","line1","line2")
		fctenTLE= TLE(1,"fcten","line1","line2")
		fcelevenTLE= TLE(1,"fceleven","line1","line2")
		fethirteenTLE= TLE(1,"fethirteen","line1","line2")
		fefourteenTLE= TLE(1,"fefourteen","line1","line2")
		itupTLE= TLE(1,"itup","line1","line2")

		date1 = datetime(2017, 1, 1, 12, 0, 0)
			# id, tle, riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
		cat = NextPass(0,catTLE, catAOS, catLOS, 0,0,0,0)
		sixtysevenC = NextPass(1,sixtysevenCTLE,sixtysevenCAOS, sixtysevenCLOS,date1,date1,date1,date1)
		sixtysevenD = NextPass(2,sixtysevenDTLE,sixtysevenDAOS, sixtysevenDLOS,date1,date1,date1,date1)
		aist = NextPass(3,aistTLE,aistAOS, aistLOS,date1,date1,date1,date1)
		beesat = NextPass(4,beesatTLE,beesatAOS, beesatLOS,date1,date1,date1,date1)
		brite = NextPass(5,briteTLE,briteAOS, briteLOS,date1,date1,date1,date1)
		cubebug = NextPass(6,cubebugTLE,cubebugAOS, cubebugLOS,date1,date1,date1,date1)
		sail = NextPass(7,sailTLE,sailAOS, sailLOS,date1,date1,date1,date1)
		eagle = NextPass(8,eagleTLE,eagleAOS, eagleLOS,date1,date1,date1,date1)
		exo = NextPass(9,exoTLE,exoAOS,exoLOS,date1,date1,date1,date1)
		fcone = NextPass(10,fconeTLE,fconeAOS,fconeLOS,date1,date1,date1,date1)
		fcthree = NextPass(11,fcthreeTLE,fcthreeAOS, fcthreeLOS,date1,date1,date1,date1)
		fcfive = NextPass(12,fcfiveTLE,fcfiveAOS, fcfiveLOS,date1,date1,date1,date1)
		fceight = NextPass(13,fceightTLE,fceightAOS,fceightLOS,date1,date1,date1,date1)
		fcnine = NextPass(14,fcnineTLE,fcnineAOS,fcnineLOS,date1,date1,date1,date1)
		fcten = NextPass(15,fctenTLE,fctenAOS, fctenLOS,date1,date1,date1,date1)
		fceleven = NextPass(16,fcelevenTLE,fcelevenAOS, fcelevenLOS,date1,date1,date1,date1)
		fethirteen = NextPass(17,fethirteenTLE,fethirteenAOS,fethirteenLOS,date1,date1,date1,date1)
		fefourteen = NextPass(18,fefourteenTLE,fefourteenAOS,fefourteenLOS,date1,date1,date1,date1)
		itup = NextPass(19,itupTLE,itupAOS, itupLOS,date1,date1,date1,date1)		

		# satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail,eagle,
		# exo,fcone,fcthree,fcfive,fcfive,fceight,fcnine,fcten,fceleven,fethirteen,fefourteen,
		# itup]
		satList=[brite,fceight,eagle,fefourteen,sixtysevenC,fethirteen,itup,sail,sixtysevenD,exo,beesat,
		fceleven,fcfive,fcnine,fcten,fcone,cat,fcthree,cubebug,aist]
			#self.assertIs(shouldBe == ,)

		#findSchedulableSatellites([[sixtysevenC,sixtysevenD,brite,fcone,fcthree,fcfive,fefourteen,itup]])
		#findSchedulableSatellites([[sixtysevenD,sixtysevenC,brite,fcone,fcthree,fcfive,fefourteen,itup]])
		#findSchedulableSatellites([[sixtysevenD,sixtysevenC,fcone,brite,fcthree,fcfive,fefourteen,itup]])
		score=_Helper.fitnessFunction(satList)
		print(score)
		#HillClimbing.simple(satList)
#test_findSchedulableSatellites_many_real_sats()