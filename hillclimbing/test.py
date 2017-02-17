#!usr/bin/env python  
from datetime import date, datetime, timedelta
from random import shuffle

class satellite(object):
	"Just an object I made to avoid importing an actual object"
	name=""
	AOS=None
	LOS=None

	def __init__(self,name,AOS,LOS):
		self.name = name
		self.AOS = AOS
		self.LOS = LOS

	def __str__(self):
		return self.name

	def __repr__(self):
		return str(self)

#class FitnessFunction():
		
def fitnessFunction(satList):

	"""Calling all the necessary parts in order
		and checking the priority is in order
		ensuring the order of the list"""

	#is priority maintained function goes here

	satListConflictGroups = findConflictingGroups(satList)

	mergedGroups = mergeLists(satListConflictGroups)

	reorderedConflictGroups=[]
	for group in mergedGroups:
		#print("sdfsd")
		reordered= [x for x in satList if x in group]
		reorderedConflictGroups.append(reordered)

	score = findSchedulableSatellites(reorderedConflictGroups)

	print(score)
	return score

def findConflictingGroups(satList):
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
			if satList[i].AOS <= satList[j].LOS and satList[i].LOS >= satList[j].AOS:
				#they conflict
				#print('{} conflicts with {}'.format(satList[i],satList[j]))
				if satList[i] and satList[j] not in conflicts:
					conflicts.append(satList[i])
					conflicts.append(satList[j])

		if len(conflicts)>0:
			satListConflicts.append(list(set(conflicts)))

	#print(satListConflicts) 
	#blah = mergeLists(satListConflicts)

	return satListConflicts

def mergeLists(satListConflicts):
	""" findConflictingGroups work isn't finished, it is continued here. 
		If any list shares one or more element with another list then 
		they should really be one list/group
		eg. if sat1 and sat2 conflict, and sat2 and sat3 conflict,
		findConflictingGroups would put them in two different lists but
		merge lists combines them into a group even though sat1 and 
		sat3 don't conflict 
	"""
	#def finalListConflicts():
	#what happens if 2nd list is bigger than the first
	# satListConflicts = [['sat1', 'sat4', 'sat2', 'sat6'], ['sat6', 'sat7', 'sat4', 'sat2', 'sat5'],
	# 				   ['sat3', 'sat11', 'sat10'], ['sat6', 'sat7', 'sat4'], ['sat6', 'sat7'], ['sat9', 'sat8'],
	# 				   ['sat11', 'sat10']]
	# satListConflicts = [['sat2', 'sat1', 'sat6', 'sat7', 'sat8', 'sat9', 'sat4'], 
	# 					['sat2', 'sat6', 'sat7', 'sat5', 'sat8', 'sat9', 'sat4'], 
	# 					['sat11', 'sat3', 'sat10'], ['sat8', 'sat6', 'sat7', 'sat9', 'sat4'], 
	# 					['sat7', 'sat8', 'sat9', 'sat6'], ['sat8', 'sat9', 'sat7'], 
	# 					['sat8', 'sat9'], ['sat11', 'sat10']]
	#print(satListConflictssatListConflicts)
	prevSatConlicts = []
	while len(satListConflicts) != len(prevSatConlicts):
		finaListsConflictsTrimmed=[]
		finaListsConflicts = []

		for i in range(len(satListConflicts)):
			subList = satListConflicts[i]
			#c2 = satListConflicts
			#c3 = [list(filter(lambda x: x in c1, sublist)) for sublist in c2]
			#function = lambda x: x in c1
			#iterable = satListConflicts[j] (list)
			
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


def findSchedulableSatellites(satListConflictGroups):
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
			tempTime = []
			conflicts=False
			curSatRise,curSatRise,conflicts,blackList = findUsableTime(sat, blackList, transactionTime,conflicts)
			#Find a time to fit it in

			if len(blackList)==0:
				curSatRise=sat.AOS 				
				curSatSet = sat.AOS + transactionTime 				
				tempTime = [curSatRise,curSatSet] 				
				scheduledSats.append(sat) 				
				blackList.append(tempTime)

			if conflicts is False:
				#Check satellite doesn't conflict with 'blacklisted' times
				#before adding it
				tempTime = [curSatRise,curSatSet]
				for time in blackList:
					if tempTime[0] < time[1] and tempTime[1] > time[0]:
						conflictBlack=True
						break
					else:
						conflictBlack=False

				if conflictBlack != True:
				#if tempTime is not blackList:
					scheduledSats.append(sat)
					blackList.append(tempTime)			
		
		print(blackList)
		#Find unscheduled satellites from scheduled
		unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
		unScheduledSats.append(unScheduledSatFromGroup)
		nextPassList.append(scheduledSats)

	print("nextpasslist")
	print(nextPassList)
	print("unScheduledSats")
	print(unScheduledSats)

	#Count number of unscheduled
	score=0
	for satList in unScheduledSats:
		score +=len(satList)
	print(score) # want lowest.
	return score

def findUsableTime(sat, blackList, transactionTime,conflicts):

	curSatRise = 0
	curSatSet = 0
	
	for time in blackList:
		if sat.AOS < time[1] and sat.LOS > time[0]:
			#print('{} conflicts with {} {}'.format(sat.name,time[0],time[1]))
			#sat conflicts with one of the times in blackList
			#in i=1 sat is sat2 and blacklist is sat 1
			endGap = sat.LOS - (time[0]+transactionTime)
			if endGap<timedelta(0):
				endGap = endGap*-1
			frontGap = time[0] - sat.AOS
			if frontGap<timedelta(0):
				frontGap = frontGap*-1
			#TODO: if frontGap and endGap both >= tt and we can
			#fit in either, pick one at random
			if endGap>=transactionTime:
				#can be fit in end gap
				#TODO: fit in some random place in end gap
				#print("fit in end gap")
				curSatRise = sat.LOS-transactionTime
				curSatSet = sat.LOS
				conflicts=False
			elif frontGap >= transactionTime:
				#can be fit in start gap
				#TODO: fit in some random place in front gap
				#print("fit in front gap")
				conflicts=False
				curSatRise = sat.AOS
				curSatSet = sat.AOS + transactionTime
			else:
				#can't fit in and we need another pass
				#print("adding")
				#unScheduledSats.append(sat.name)
				conflicts=True
				return 0,0,conflicts,blackList
				
		else:
			curSatRise = sat.AOS
			curSatSet = sat.AOS + transactionTime
			conflicts=False

	#tempTime = [curSatRise,curSatRise]

	# if len(blackList)==0:
	# 	##For first satellite to be scheduled
	# 	curSatRise=sat.AOS
	# 	curSatSet = sat.AOS + transactionTime
	# 	tempTime = [curSatRise,curSatSet]
	# 	print("leeeed")
				
	
	return curSatRise,curSatRise, conflicts, blackList


def test_findSchedulableSatellites_many_real_sats():

	catAOS = datetime(2017,1,25,0,52,59)
	catLOS = datetime(2017,1,25,1,04,28)
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
	exoLOS = datetime(2017,1,25,1,05,27)
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

	#09 

	cat = satellite("cat",catAOS, catLOS)
	sixtysevenC = satellite("sixtysevenC",sixtysevenCAOS, sixtysevenCLOS)
	sixtysevenD = satellite("sixtysevenD",sixtysevenDAOS, sixtysevenDLOS)
	aist = satellite("aist",aistAOS, aistLOS)
	beesat = satellite("beesat",beesatAOS, beesatLOS)
	brite = satellite("brite",briteAOS, briteLOS)
	cubebug = satellite("cubebug",cubebugAOS, cubebugLOS)
	sail = satellite("sail",sailAOS, sailLOS)
	eagle = satellite("eagle",eagleAOS, eagleLOS)
	exo = satellite("exo",exoAOS,exoLOS)
	fcone = satellite("fcone",fconeAOS,fconeLOS)
	fcthree = satellite("fcthree",fcthreeAOS, fcthreeLOS)
	fcfive = satellite("fcfive",fcfiveAOS, fcfiveLOS)
	fceight = satellite("fceight",fceightAOS,fceightLOS)
	fcnine = satellite("fcnine",fcnineAOS,fcnineLOS)
	fcten = satellite("fcten",fctenAOS, fctenLOS)
	fceleven = satellite("fceleven",fcelevenAOS, fcelevenLOS)
	fethirteen = satellite("fethirteen",fethirteenAOS,fethirteenLOS)
	fefourteen = satellite("fefourteen",fefourteenAOS,fefourteenLOS)
	itup = satellite("itup",itupAOS, itupLOS)




	#satList=[sat1,sat2,sat3,sat5]
	satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail,eagle,
	exo,fcone,fcthree,fcfive,fcfive,fceight,fcnine,fcten,fceleven,fethirteen,fefourteen,
	itup]
		#self.assertIs(shouldBe == ,)

	#findSchedulableSatellites([[sixtysevenC,sixtysevenD,brite,fcone,fcthree,fcfive,fefourteen,itup]])
	#findSchedulableSatellites([[sixtysevenD,sixtysevenC,brite,fcone,fcthree,fcfive,fefourteen,itup]])
	#findSchedulableSatellites([[sixtysevenD,sixtysevenC,fcone,brite,fcthree,fcfive,fefourteen,itup]])
	fitnessFunction(satList)

# clas = fit.FitnessFunction()
# clas.test_findSchedulableSatellites_many_sats()


def test_findSchedulableSatellites_many_fake_sats():

	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,11,57,0)
	sat8LOS = datetime(2017,1,25,12,4,0)
	sat9AOS = datetime(2017,1,25,13,0,0)
	sat9LOS = datetime(2017,1,25,13,4,0)
	sat10AOS = datetime(2017,1,25,12,27,0)
	sat10LOS = datetime(2017,1,25,12,31,0)
	sat11AOS = datetime(2017,1,25,12,28,0)
	sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	sat10 = satellite("sat10",sat10AOS,sat10LOS)
	sat11 = satellite("sat11",sat11AOS,sat11LOS)

	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]

	fitnessFunction(satList)

def test_findSchedulableSatellites_many_fake_sats_but_diff():

	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,12,59,0)
	sat8LOS = datetime(2017,1,25,13,3,0)
	sat9AOS = datetime(2017,1,25,13,0,0)
	sat9LOS = datetime(2017,1,25,13,4,0)
	sat10AOS = datetime(2017,1,25,12,27,0)
	sat10LOS = datetime(2017,1,25,12,31,0)
	sat11AOS = datetime(2017,1,25,12,28,0)
	sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	sat10 = satellite("sat10",sat10AOS,sat10LOS)
	sat11 = satellite("sat11",sat11AOS,sat11LOS)

	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]

	fitnessFunction(satList)



#check we don't lose a sat during processing
#check against a varied set of sats
# test_findSchedulableSatellites_many_real_sats()
# test_findSchedulableSatellites_many_fake_sats_but_diff()
# test_findSchedulableSatellites_many_fake_sats()


def hillclimbing(satList):
	""" Actual algorithm which isn't quite hillclimbing cause it 
		shuffles the list rather than moving one step from 
		current position"""
	""" Shuffle the list at least 100 times, if better list comes from
		shuffling reset maxIterations and shuffle. If no better list
		comes, then that could be it"""

	maxIterations = 100
	i=0
	oldUnscheduled = max   #just a really big number
	newOrder=[]
	curOrder=satList
	while i<maxIterations:
		shuffle(curOrder) 
		#shuffling can make it find different solutions
		#shuffling count as hc with random restart kinda?
		newUnscheduled = fitnessFunction(curOrder)
		if newUnscheduled < oldUnscheduled:
			#use that 
			print("New Order")
			#curOrder=newOrder
			oldUnscheduled=newUnscheduled
			i=0
		else:
			print("Keep Order")
			i+=1
			
	if i==100:
		print("{} curOrder could be global maxima".format(curOrder))		
		return curOrder


def test_hillclimbing_many_real_sats():
	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,11,57,0)
	sat8LOS = datetime(2017,1,25,12,4,0)
	sat9AOS = datetime(2017,1,25,13,0,0)
	sat9LOS = datetime(2017,1,25,13,4,0)
	sat10AOS = datetime(2017,1,25,12,27,0)
	sat10LOS = datetime(2017,1,25,12,31,0)
	sat11AOS = datetime(2017,1,25,12,28,0)
	sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	sat10 = satellite("sat10",sat10AOS,sat10LOS)
	sat11 = satellite("sat11",sat11AOS,sat11LOS)

	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]

	hillclimbing(satList)

def test_hillclimbing_many_fake_sats():

	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,11,57,0)
	sat8LOS = datetime(2017,1,25,12,4,0)
	sat9AOS = datetime(2017,1,25,11,57,0)
	sat9LOS = datetime(2017,1,25,12,4,0)
	# sat10AOS = datetime(2017,1,25,12,27,0)
	# sat10LOS = datetime(2017,1,25,12,31,0)
	# sat11AOS = datetime(2017,1,25,12,28,0)
	# sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	# sat10 = satellite("sat10",sat10AOS,sat10LOS)
	# sat11 = satellite("sat11",sat11AOS,sat11LOS)

	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9]#,sat10,sat11]

	hillclimbing(satList)

def test_hillclimbing_many_fake_sats_but_diff():

	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,12,59,0)
	sat8LOS = datetime(2017,1,25,13,3,0)
	sat9AOS = datetime(2017,1,25,13,0,0)
	sat9LOS = datetime(2017,1,25,13,4,0)
	sat10AOS = datetime(2017,1,25,12,27,0)
	sat10LOS = datetime(2017,1,25,12,31,0)
	sat11AOS = datetime(2017,1,25,12,28,0)
	sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	sat10 = satellite("sat10",sat10AOS,sat10LOS)
	sat11 = satellite("sat11",sat11AOS,sat11LOS)

	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]

	hillclimbing(satList)


test_hillclimbing_many_fake_sats()
#test_findSchedulableSatellites_many_fake_sats()

# def swap(satList):
# 	int x1=0
# 	int x2=0
# 	while x1==x2:
# 		x1 = satList
# 	swap two random elements?


