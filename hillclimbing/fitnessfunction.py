#!usr/bin/env python  
from datetime import date, datetime, timedelta

class satellite(object):
	name=""
	AOS=None
	LOS=None

	def __init__(self,name,AOS,LOS):
		self.name = name
		self.AOS = AOS
		self.LOS = LOS

	def __str__(self):
		return self.name

def findNumberOfPasses():
	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	
	#sats=[sat1AOS,sat1LOS,sat2AOS,sat2LOS]
	#sats=[sat2AOS,sat2LOS,sat1AOS,sat1LOS,]

	transactionTime = timedelta(minutes = 3)
	numberOfPasses=0
	#delta time maybe?
	
	#get satellites in list that conflict with
	#each other
	#sat1, sat2, sat3 .... all have to conflict with
	#each other
	
	if (sat1LOS - sat1AOS)>=transactionTime:
		#can be fit in there
		pass
	else:
		numberOfPasses+=1


	if (sat2LOS - (sat1AOS+transactionTime))>=transactionTime or (sat1AOS - sat2AOS) >= transactionTime:
		pass
		#can be fit in end gap									or can be fit in start gap
	else:
		numberOfPasses+=1

	print(numberOfPasses)


def findNumberOfPasses1(satPrimary,satListConflicts):
	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	
	#sats=[sat1AOS,sat1LOS,sat2AOS,sat2LOS]
	#sats=[sat2AOS,sat2LOS,sat1AOS,sat1LOS,]

	transactionTime = timedelta(minutes = 3)
	numberOfPasses=0
	#delta time maybe?
	
	#get satellites in list that conflict with
	#each other
	#sat1, sat2, sat3 .... all have to conflict with
	#each other
	


	# if (sat1LOS - sat1AOS)>=transactionTime:
	# 	#can be fit in there
	# 	pass
	# else:
	# 	numberOfPasses+=1

	i=0
	for i in range(len(satListConflicts)):
		#for j in range(i+1, len(satListConflicts)):
		print('Compare {} with {}'.format(satListConflicts[i],satPrimary))
		if (satListConflicts[i].AOS - (satPrimary.AOS+transactionTime))>=transactionTime or (satPrimary.AOS - satListConflicts[i].AOS) >= transactionTime:
			pass
			#can be fit in end gap									or can be fit in start gap
		else:
			numberOfPasses+=1

		
	print(numberOfPasses)


def findConflictingGroups(satList):

	satListConflicts=[]
	for i in range(len(satList)):
		#Does it conflict with sat
		# print("gello")
		# print(satPrimary.AOS)
		# print(sat.LOS)
		# print(satPrimary.LOS)
		# print(sat.AOS)
		conflicts=[]
		for j in range(i+1, len(satList)):
			if satList[i].AOS <= satList[j].LOS and satList[i].LOS >= satList[j].AOS:
				#they conflict
				print('{} conflicts with {}'.format(satList[i],satList[j]))
				if satList[i] and satList[j] not in conflicts:
					conflicts.append(satList[i].name)
					conflicts.append(satList[j].name)
				# if satList[i] not in conflicts:
				# 	conflicts.append(satList[i].name)
				# if satList[j] not in conflicts:
				# 	conflicts.append(satList[j].name)
		

		if len(conflicts)>0:
			satListConflicts.append(list(set(conflicts)))

	print(satListConflicts)
	# for lis1,lis2 in satListConflicts:
	# 	print lis1, lis2
	# 	for ele in lis1:
	# 		if ele in lis2:
	# 			lis3 = lis1+lis2
	# 			print(lis3)
	# 			satListConflicts.append(lis)
	finalConflicts=[]
	for k in range(len(satListConflicts)):
		for l in range(k+1,len(satListConflicts)):
			#list vs list
			print('{} compared with {}'.format(satListConflicts[k],satListConflicts[l]))
			mergedList = mergeLists(satListConflicts[k],satListConflicts[l])
			
			if mergedList is not None and mergedList not in finalConflicts:
				print('merged to give {}'.format(mergedList))
				finalConflicts.append(mergedList)

	print(finalConflicts)
	finalConflicts1=[]
	for m in range(len(finalConflicts)):
		for n in range(m+1,len(finalConflicts)):
			#list vs list
			print('{} compared with {}'.format(finalConflicts[m],finalConflicts[n]))
			mergedList = mergeLists(finalConflicts[m],finalConflicts[n])
			if mergedList is not None and mergedList not in finalConflicts1:
				print('merged to give {}'.format(mergedList))
				finalConflicts1.append(mergedList)

	print(finalConflicts1)
	# final=[]
	# for m in range(len(finalConflicts)):
	# 	for n in range(m+1,len(finalConflicts)):
	# 		if(set(finalConflicts[m]).issuperset(finalConflicts[n])):
	# 			print('{} is super set of {}'.format(finalConflicts[m],finalConflicts[n]))
	# 			final.append(finalConflicts[m])

	# for x in satListConflicts:
	# 	print("[")
	# 	for b in x:
	# 		print(b.name)

	#print(satListConflicts)
	return satListConflicts

def mergeLists(list1,list2):
	# list1=["sat1","sat2","sat3","sat4"]
	# list2=["sat2","sat3","sat4","sat5"]

	list3=[]
	for ele in list1:
		if ele in list2:
			list3=list1+list2
			return list(set(list3))

def findConflictingSats(satPrimary,satList):

	satListConflicts=[]
	
	for sat in satList:
		#Does it conflict with sat
		# print("gello")
		# print(satPrimary.AOS)
		# print(sat.LOS)
		# print(satPrimary.LOS)
		# print(sat.AOS)
		#if sat1.AOS <= sat2.LOS and sat1.LOS >= sat2.AOS:
		if satPrimary.AOS <= sat.LOS and satPrimary.LOS >= sat.AOS:
			#they conflict
			#print("conflict")
			satListConflicts.append(sat)

	if len(satListConflicts) == 1:
		#no conflicts
		satListConflicts.remove(satPrimary)
	#for x in satListConflicts:
		#print (x.name)
	#print(satListConflicts)
	return satListConflicts

sat1AOS = datetime(2017,1,25,12,2,0)
sat1LOS = datetime(2017,1,25,12,5,0)
sat2AOS = datetime(2017,1,25,12,0,0)
sat2LOS = datetime(2017,1,25,12,8,0)
sat3AOS = datetime(2017,1,25,12,25,0)
sat3LOS = datetime(2017,1,25,12,30,0)
sat4AOS = datetime(2017,1,25,11,57,0)
sat4LOS = datetime(2017,1,25,12,03,0)
sat5AOS = datetime(2017,1,25,12,07,0)
sat5LOS = datetime(2017,1,25,12,10,0)
sat6AOS = datetime(2017,1,25,11,57,0)
sat6LOS = datetime(2017,1,25,12,04,0)
sat7AOS = datetime(2017,1,25,11,57,0)
sat7LOS = datetime(2017,1,25,12,04,0)
sat8AOS = datetime(2017,1,25,12,59,0)
sat8LOS = datetime(2017,1,25,13,03,0)
sat9AOS = datetime(2017,1,25,13,00,0)
sat9LOS = datetime(2017,1,25,13,04,0)
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

satListConflicts = findConflictingGroups(satList)#findConflictingSats(sat1,satList)

# for x in satListConflicts:
# 	print(x)

#reordered= [x for x in satList if x in satListConflicts]

# for x in reordered:
# 	print(x)
#findNumberOfPasses1(sat1,satListConflicts)
