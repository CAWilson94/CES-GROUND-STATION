from datetime import date, datetime, timedelta
from random import shuffle,randint
from ..services import Services
from ..models import NextPass
import sys

class _Helper():


	def fitnessFunction(self, missionList,usefulTime):
		"""Calling all the necessary parts in order
			and checking the priority is in order
			ensuring the order of the list"""

		#print("missionlist")
		#print(missionList)
		nextPassList=[]
		try:
			prevMission=missionList[0]
		except IndexError  as e:
			#print("return this {} list with this {} score".format([],0))
			return [0,[]]

		for mission in missionList:
			if mission.priority > prevMission.priority:
				print ("bad priority")
				return [sys.maxsize,[]]
			else:
				prevMission = mission

		print("nextPasses")
		for mission in missionList:
			nextPass = Services.getNextPass(self, mission.TLE.name ,mission, datetime(2017,3,27,16,0,0))
			
			print(nextPass)
			nextPassList.append(nextPass)
	 
	 	#put in priority groups!
			
		# sat1 = NextPass(riseTime=datetime(2017, 3, 25, 22, 39, 3), setTime=datetime(2017, 3, 25, 22, 48, 39), duration=timedelta(0, 576), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat1")
		# sat2 = NextPass(riseTime=datetime(2017, 3, 26, 5, 1, 12), setTime=datetime(2017, 3, 26, 5, 13, 53), duration=timedelta(0, 761), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat2")
		# sat3 = NextPass(riseTime=datetime(2017, 3, 26, 2, 6, 51), setTime=datetime(2017, 3, 26, 2, 19, 33), duration=timedelta(0, 762), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat3")
		# sat4 = NextPass(riseTime=datetime(2017, 3, 25, 23, 57, 18), setTime=datetime(2017, 3, 25, 0, 7, 10), duration=timedelta(0,608), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat4")
		# sat5 = NextPass(riseTime=datetime(2017, 3, 26, 4, 29, 32), setTime=datetime(2017, 3, 26, 4, 39, 40), duration=timedelta(0, 608), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat5")
		# sat6 = NextPass(riseTime=datetime(2017, 3, 25, 23, 24, 42), setTime=datetime(2017, 3, 25, 23, 26, 9), duration=timedelta(0, 87), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat6")
		# sat7 = NextPass(riseTime=datetime(2017, 3, 25, 22, 36, 45), setTime=datetime(2017, 3, 25, 22, 47, 4), duration=timedelta(0, 619), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat7")

		# nextPassList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7]
		#print("nextpasslist")
		#print(nextPassList)

		conflictGroups,nonConflictGroups = _Helper._findConflictingGroups(nextPassList)

		# print("conflictGroups")
		# print(conflictGroups)
		# print("nonconflictgroups")
		# print(nonConflictGroups)
		
		
		if len(conflictGroups)==0:
			#no conflicts
			print("no conflicts")
			#print(nextPassList)
			#print("return this {} list with this {} score".format(nextPassList,0))
			return [0,nextPassList]

		mergedGroups = _Helper._mergeLists(conflictGroups)

		reorderedConflictGroups=[]
		for group in mergedGroups:
			reordered= [x for x in nextPassList if x in group]
			reorderedConflictGroups.append(reordered)

		print("reorderedConflictGroups")
		print(mergedGroups)

		processedNextPassList=[]
		
		score,processedNextPassList = _Helper._findSchedulableSatellites(reorderedConflictGroups,usefulTime)



		noConflictList=[]
		for Pass in nextPassList:
			notInGroup=True
			for group in mergedGroups:
				if Pass in group:
					notInGroup=False
			if notInGroup:
				noConflictList.append(Pass)

		for sat in noConflictList:
			#print(sat)
			processedNextPassList.append(sat)
				
		processedNextPassList=set(processedNextPassList)
		#print("nextpassprolist")
		#print(processedNextPassList)
		#score=len(processedNextPassList)
		score = len(nextPassList)-len(processedNextPassList)
		#print(score)
		#print(nextPassList)
		#print("return this {} list with this {} score".format(processedNextPassList,score))
		return [score,processedNextPassList]

	def _findConflictingGroups(satList):
		""" Compares each satellite with each other to find the ones
			that conflict at all with each other. 
			eg. if sat1 and sat2 conflict they are added to conflicts
			and sat3 and sat4 conflicts they added to conflicts but in a 
			different list/group
		"""
		satListConflicts=[]
		satListNoConflicts=[]
		#print("liiiiiist")
		#print(len(satList))

		for i in range(len(satList)):
			conflicts=[]
			noConflicts=[]
			for j in range(i+1, len(satList)):
				#print('{} riseTime & {} setTime compared with {} riseTime & {} setTime'.format(satList[i].riseTime,satList[i].setTime,satList[j].riseTime,satList[j].setTime))
				if satList[i].riseTime < satList[j].setTime and satList[i].setTime > satList[j].riseTime:
					#they conflict
					print("conflicts")
					#print('{} conflicts with {}'.format(satList[i],satList[j]))
					if satList[i] and satList[j] not in conflicts:
						conflicts.append(satList[i])
						conflicts.append(satList[j])
				else:
					for group in satListConflicts:
						if satList[i] not in group:
							print("no conflict")
							noConflicts.append(satList[i])	
					#print("This sat {} doesn't conflict with any other".format(satList[i]))	

			if len(conflicts)>0:
				satListConflicts.append(list(set(conflicts)))
			if len(noConflicts)>0:
				satListNoConflicts.extend(list(set(noConflicts)))

		return satListConflicts, satListNoConflicts

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


	def _findSchedulableSatellites(satListConflictGroups,usefulTime):
		""" The groups are now correct and the order was reestablished before 
		being passed in here. This goes through each sat in each group to find where
		each satellite conflicts with each other satellite. Compares these gaps
		with the transactionTime to figure out if this time available is useful to
		us. Checks with the blacklist. ie. times that are in use. If the space of gap
		is enough and that time isn't in use/conflicts we can schedule a satellite here 
		and that time period is then 'blacklisted' ie in use. 
		"""


		#print("conflict groups")
		#print(satListConflictGroups)

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
				curSatRise=0
				curSatSet=0
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
							#get conflcit time and work fom there instead of set time
							#can be fit in end gap
							#TODO: fit in some random place in end gap
							curSatRise = sat.setTime-transactionTime
							curSatSet = sat.setTime
							#curSatRise = time[1]+transactionTime
							#curSatSet = time[1]
							conflicts=False
						elif frontGap >= transactionTime:
							#can be fit in start gap
							#TODO: fit in some random place in front gap
							#print("fit in front gap")
							conflicts=False
							curSatRise = sat.riseTime
							curSatSet = sat.riseTime + transactionTime
							#curSatSet=time[0]-transactionTime
							#curSatRise=time[0]
						else:
							#can't fit in and we need another pass
							#print("adding")
							#unScheduledSats.append(sat.name)
							conflicts=True
							break

					else:
						curSatRise = sat.riseTime
						curSatSet = sat.riseTime + transactionTime
						#curSatRise = time[1]
						#curSatSet = time[1]+transactionTime
						conflicts=False

				tempTime = []
				if len(blackList)==0:
					##For first satellite to be scheduled
					curSatRise=sat.riseTime
					curSatSet=sat.setTime#sat.riseTime + transactionTime
					#curSatRise=time
					tempTime = [curSatRise,curSatSet]
					scheduledSats.append(sat)
					blackList.append(tempTime)
					
					#sat.riseTime=curSatRise
					#sat.setTime=curSatSet
					#sat.duration=transactionTime
					newPasses.append(sat)

				if conflicts is False:
					#Check satellite doesn't conflict with 'blacklisted' times
					#before adding it
				
					conflictBlack = False
					tempTime = [curSatRise,curSatSet]
					for time in blackList:
						# print("tempTime")
						# print(tempTime[0])
						# print("time")
						# print(time[1])
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
						sat.duration=transactionTime
						newPasses.append(sat)	
			
			#Find unscheduled satellites from scheduled
			unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
			unScheduledSats.append(unScheduledSatFromGroup)
			allScheduledSats.extend(scheduledSats)
			nextPassList.extend(newPasses)

		score=0

		#print("scheduled sats")
		#print(unScheduledSats)
		for satList in unScheduledSats:
			score +=len(satList)
		#print(score) # want lowest.
		return score,nextPassList