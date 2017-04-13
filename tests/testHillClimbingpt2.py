from datetime import date,datetime
from scheduler.models import TLE, NextPass,Mission
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT._MOTHelper import _Helper
from django.test import TestCase


class FitnessFunctionTests(TestCase):


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
	exoAOS=datetime(2017,1,26,0,53,0)
	exoLOS = datetime(2017,1,26,1,1,0)

	catTLE = TLE(name="cat",line1="line1",line2="line2")
	sixtysevenCTLE = TLE(name="sixtysevenC",line1="line1",line2="line2")
	sixtysevenDTLE= TLE(name="sixtysevenD",line1="line1",line2="line2")
	aistTLE= TLE(name="aist",line1="line1",line2="line2")
	beesatTLE= TLE(name="beesat",line1="line1",line2="line2")
	briteTLE= TLE(name="brite",line1="line1",line2="line2")
	cubebugTLE= TLE(name="cubebug",line1="line1",line2="line2")
	sailTLE= TLE(name="sail",line1="line1",line2="line2")

	mis1=Mission(priority=2)
	mis2=Mission(priority=2)
	mis3=Mission(priority=2)
	mis4=Mission(priority=2)
	mis5=Mission(priority=2)
	mis6=Mission(priority=2)
	mis7=Mission(priority=2)
	mis8=Mission(priority=2)
	mis9=Mission(priority=2)

	redfernTLE = TLE(name="LEMUR-2-REDFERN-GOES",line1="line1",line2="line2")
	eyeTLE = TLE(name="EYESAT-1 (AO-27)",line1="line1",line2="line2")
	trutnaTLE= TLE(name="LEMUR-2-TRUTNA",line1="line1",line2="line2")
	techTLE= TLE(name="TECHEDSAT 5",line1="line1",line2="line2")
	seventyeightTLE= TLE(name="FLOCK 3P-78",line1="line1",line2="line2")
	seventyfourTLE= TLE(name="FLOCK 3P-74",line1="line1",line2="line2")
	primeTLE= TLE(name="M-CUBED & EXP-1 PRIME",line1="line1",line2="line2")
	ausTLE= TLE(name="LEMUR-2-AUSTINTACIOUS",line1="line1",line2="line2")
	twentyoneTLE= TLE(name="FLOCK 3P-21",line1="line1",line2="line2")

	
	CubeSatA = NextPass(riseTime=datetime(2017, 3, 27, 19, 1, 46),setTime=datetime(2017, 3, 27, 19, 10, 40),tle=twentyoneTLE, mission=mis9)
	CubeSatB = NextPass(riseTime=datetime(2017, 3, 27, 19, 33, 45),setTime=datetime(2017, 3, 27, 19, 40, 15),tle=ausTLE, mission=mis8)
	CubeSatC = NextPass(riseTime=datetime(2017, 3, 27, 18, 53, 45),setTime=datetime(2017, 3, 27, 19, 2, 14),tle=seventyfourTLE, mission=mis6)
	CubeSatD = NextPass(riseTime=datetime(2017, 3, 27, 18, 53, 36),setTime=datetime(2017, 3, 27, 19, 2, 5),tle=seventyeightTLE, mission=mis5)
	CubeSatE = NextPass(riseTime=datetime(2017, 3, 27, 19, 15, 21),setTime=datetime(2017, 3, 27, 19, 20),tle=techTLE, mission=mis4)
	CubeSatF = NextPass(riseTime=datetime(2017, 3, 27, 19, 32, 41),setTime=datetime(2017, 3, 27, 19, 39, 8),tle=trutnaTLE, mission=mis3)
	CubeSatG = NextPass(riseTime=datetime(2017, 3, 27, 19, 31, 16),setTime=datetime(2017, 3, 27, 19, 37, 35),tle=eyeTLE, mission=mis2)
	

	redfern = NextPass(riseTime=datetime(2017, 3, 27, 16, 24, 50),setTime=datetime(2017, 3, 27, 16, 37, 33),tle=redfernTLE, mission=mis1)	

	prime= NextPass(riseTime=datetime(2017, 3, 27, 17, 25, 57),setTime=datetime(2017, 3, 27, 17, 36, 57),tle=primeTLE, mission=mis7)
	nextPassList = [redfern,eye,trutna,tech,seventyeight,seventyfour,prime,aus,twentyone]

	def test_find_conflict_groups(self):


		#satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail]
		
		#nextPassList = [seventyeight,seventyfour]
		

		#nextPassList = [self.redfern,self.eye,self.trutna,self.tech,self.seventyeight,self.seventyfour,self.prime,self.aus,self.twentyone]
		
		conflictGroups = _Helper._findConflictingGroups(self.nextPassList)	
		mergedGroups = _Helper._mergeLists(conflictGroups)

		shouldBe = [[self.aus,self.trutna,self.eye],[self.seventyeight,self.seventyfour,self.twentyone]]
		#self.assertIs(set(shouldBe) == set(mergedGroups),True)

# 		mergedGroups = _Helper._mergeLists(conflictGroups)

	
		self.assertIs((set(shouldBe[0]) == set(mergedGroups[0])) & (set(shouldBe[1])==(set(mergedGroups[1]))),True)


		
	def test_schedule_sats(self):

		usefulTime=6
		mergedGroups = [[self.aus,self.trutna,self.eye],[self.seventyeight,self.seventyfour,self.twentyone]]

		reorderedConflictGroups=[]
		for group in mergedGroups:
			reordered= [x for x in self.nextPassList if x in group]
			reorderedConflictGroups.append(reordered)

		processedNextPassList = _Helper._findSchedulableSatellites(reorderedConflictGroups,usefulTime)
		
		shouldBe=[self.eye, self.seventyeight,self.twentyone]

		self.assertIs(set(shouldBe)==set(processedNextPassList),True)
		#print(processedNextPassList)



# 		score = len(nextPassList)-len(processedNextPassList)
# 		print(score)
# 		steepestHC = MOTSteepestHC()
# 		#shouldBe,nextPassList=MOTSteepestHC().find(satList,usefulTime)
# 		#print(order)
# 		cat = NextPass(tle="catTLE", riseTime=catAOS,setTime= catLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		sixtysevenC = NextPass(tle="sixtysevenCTLE",riseTime=sixtysevenCAOS, setTime=sixtysevenCLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		sixtysevenD = NextPass(tle="sixtysevenDTLE",riseTime=sixtysevenDAOS, setTime=sixtysevenDLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		aist = NextPass(tle="aistTLE",riseTime=aistAOS, setTime=aistLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		beesat = NextPass(tle="beesatTLE",riseTime=beesatAOS, setTime=beesatLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		brite = NextPass(tle="briteTLE",riseTime=briteAOS, setTime=briteLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		cubebug = NextPass(tle="cubebugTLE",riseTime=cubebugAOS, setTime=cubebugLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		sail = NextPass(tle="sailTLE",riseTime=sailAOS, setTime=sailLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
# 		exo = NextPass(tle="exo",riseTime=exoAOS,setTime=exoLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission(priority=2))
		
# 		# NextPass(riseTime=riseTime, setTime=setTime, duration=duration, maxElevation=details[3],
# 		# 	riseAzimuth=details[1],setAzimuth=detailsduration=[5], mission=mission, tle=tleName)
# 		# nextPassList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail,exo]
# 		# usefulTime=3
# 		# MOT = MOTSteepestHC()
# 		#shouldBe,nextPassList=MOT.find(satList,usefulTime)
		

# # sat1 = NextPass(riseTime=datetime(2017, 3, 25, 22, 39, 3), setTime=datetime(2017, 3, 25, 22, 48, 39), duration=timedelta(0, 576), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat1")
# 		# sat2 = NextPass(riseTime=datetime(2017, 3, 26, 5, 1, 12), setTime=datetime(2017, 3, 26, 5, 13, 53), duration=timedelta(0, 761), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat2")
# 		# sat3 = NextPass(riseTime=datetime(2017, 3, 26, 2, 6, 51), setTime=datetime(2017, 3, 26, 2, 19, 33), duration=timedelta(0, 762), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat3")
# 		# sat4 = NextPass(riseTime=datetime(2017, 3, 25, 23, 57, 18), setTime=datetime(2017, 3, 25, 0, 7, 10), duration=timedelta(0,608), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat4")
# 		# sat5 = NextPass(riseTime=datetime(2017, 3, 26, 4, 29, 32), setTime=datetime(2017, 3, 26, 4, 39, 40), duration=timedelta(0, 608), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat5")
# 		# sat6 = NextPass(riseTime=datetime(2017, 3, 25, 23, 24, 42), setTime=datetime(2017, 3, 25, 23, 26, 9), duration=timedelta(0, 87), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat6")
# 		# sat7 = NextPass(riseTime=datetime(2017, 3, 25, 22, 36, 45), setTime=datetime(2017, 3, 25, 22, 47, 4), duration=timedelta(0, 619), maxElevation=0,riseAzimuth=0,setAzimuth=0,tle="sat7")


		
# 		#print(nextPassList)
# 		conflictGroups = _Helper._findConflictingGroups(nextPassList)
# 		mergedGroups = _Helper._mergeLists(conflictGroups)
# 		#print(order)
# 		print("mergedgroups")
# 		print(mergedGroups)

# 		noConflictList=[]
# 		for Pass in nextPassList:
# 			notInGroup=True
# 			for group in mergedGroups:
# 				if Pass in group:
# 					notInGroup=False
# 			if notInGroup:
# 				noConflictList.append(Pass)
# 		print("noconflicts")
# 		print(noConflictList)

		
# 		score,processedNextPassList = _Helper._findSchedulableSatellites(mergedGroups,usefulTime)

# 		#willitalwaysbefour?
# 		#self.assertIs(shouldBe == 0,True)

# 		print("processed")
# 		print(processedNextPassList)
# 		print(score)




# from datetime import date,datetime
# from scheduler.models import TLE, NextPass
# from scheduler.MOT.steepestHC import MOTSteepestHC
# from scheduler.MOT._MOTHelper import _Helper
# from django.test import TestCase


# class FitnessFunctionTests(TestCase):

# 	def test_steepest_small_conflicts(self):
# 		catAOS = datetime(2017,1,25,0,52,59)
# 		catLOS = datetime(2017,1,25,1,4,28)
# 		sixtysevenCAOS = datetime(2017,1,25,0,6,52)
# 		sixtysevenCLOS = datetime(2017,1,25,0,14,42)
# 		sixtysevenDAOS = datetime(2017,1,25,0,8,37)
# 		sixtysevenDLOS = datetime(2017,1,25,0,16,18)
# 		aistAOS = datetime(2017,1,25,0,35,21)
# 		aistLOS = datetime(2017,1,25,0,48,8)
# 		beesatAOS = datetime(2017,1,25,0,46,48)
# 		beesatLOS = datetime(2017,1,25,1,0,4) 
# 		briteAOS = datetime(2017,1,25,0,19,39)
# 		briteLOS = datetime(2017,1,25,0,30,4)
# 		cubebugAOS = datetime(2017,1,25,0,41,54)
# 		cubebugLOS = datetime(2017,1,25,0,52,49)
# 		sailAOS = datetime(2017,1,25,0,41,17)
# 		sailLOS = datetime(2017,1,25,0,53,28)

# 		catTLE = TLE(0,"cat","line1","line2")
# 		sixtysevenCTLE = TLE(1,"sixtysevenC","line1","line2")
# 		sixtysevenDTLE= TLE(1,"sixtysevenD","line1","line2")
# 		aistTLE= TLE(1,"aist","line1","line2")
# 		beesatTLE= TLE(1,"beesat","line1","line2")
# 		briteTLE= TLE(1,"brite","line1","line2")
# 		cubebugTLE= TLE(1,"cubebug","line1","line2")
# 		sailTLE= TLE(1,"sail","line1","line2")

# 		date1 = datetime(2017, 1, 1, 12, 0, 0)
# 			# id, tle, riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
# 		cat = NextPass(0,catTLE, catAOS, catLOS, 0,0,0,0)
# 		sixtysevenC = NextPass(1,sixtysevenCTLE,sixtysevenCAOS, sixtysevenCLOS,date1,date1,date1,date1)
# 		sixtysevenD = NextPass(2,sixtysevenDTLE,sixtysevenDAOS, sixtysevenDLOS,date1,date1,date1,date1)
# 		aist = NextPass(3,aistTLE, aistAOS, aistLOS,date1,date1,date1,date1)
# 		beesat = NextPass(4,beesatTLE,beesatAOS, beesatLOS,date1,date1,date1,date1)
# 		brite = NextPass(5,briteTLE,briteAOS, briteLOS,date1,date1,date1,date1)
# 		cubebug = NextPass(6,cubebugTLE,cubebugAOS, cubebugLOS,date1,date1,date1,date1)
# 		sail = NextPass(7,sailTLE,sailAOS, sailLOS,date1,date1,date1,date1)
		
# 		satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail]
# 		usefulTime=6
# 		#steepestHC = MOTSteepestHC()
# 		#shouldBe,nextPassList=MOTSteepestHC().find(satList)

# 		groups  = _Helper._findConflictingGroups(satList)
# 		print(groups)
# 		#print(order)
# 		#print(nextPassList)
# 		#willitalwaysbefour?
# 		#self.assertIs(shouldBe == 0,True)