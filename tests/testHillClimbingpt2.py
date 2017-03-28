from datetime import date,datetime
from scheduler.models import TLE, NextPass,Mission
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT._MOTHelper import _Helper
from django.test import TestCase


class FitnessFunctionTests(TestCase):

	def test_steepest_small_conflicts(self):
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

		catTLE = TLE(0,"cat","line1","line2")
		sixtysevenCTLE = TLE(1,"sixtysevenC","line1","line2")
		sixtysevenDTLE= TLE(1,"sixtysevenD","line1","line2")
		aistTLE= TLE(1,"aist","line1","line2")
		beesatTLE= TLE(1,"beesat","line1","line2")
		briteTLE= TLE(1,"brite","line1","line2")
		cubebugTLE= TLE(1,"cubebug","line1","line2")
		sailTLE= TLE(1,"sail","line1","line2")

		Mission()
		date1 = datetime(2017, 1, 1, 12, 0, 0)
			# id, tle, riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
		cat = NextPass(tle="catTLE", riseTime=catAOS,setTime= catLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		sixtysevenC = NextPass(tle="sixtysevenCTLE",riseTime=sixtysevenCAOS, setTime=sixtysevenCLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		sixtysevenD = NextPass(tle="sixtysevenDTLE",riseTime=sixtysevenDAOS, setTime=sixtysevenDLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		aist = NextPass(tle="aistTLE",riseTime=aistAOS, setTime=aistLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		beesat = NextPass(tle="beesatTLE",riseTime=beesatAOS, setTime=beesatLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		brite = NextPass(tle="briteTLE",riseTime=briteAOS, setTime=briteLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		cubebug = NextPass(tle="cubebugTLE",riseTime=cubebugAOS, setTime=cubebugLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		sail = NextPass(tle="sailTLE",riseTime=sailAOS, setTime=sailLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		exo = NextPass(tle="exo",riseTime=exoAOS,setTime=exoLOS,duration=0,riseAzimuth=0,setAzimuth=0,mission=Mission())
		
		# NextPass(riseTime=riseTime, setTime=setTime, duration=duration, maxElevation=details[3],
		# 	riseAzimuth=details[1],setAzimuth=detailsduration=[5], mission=mission, tle=tleName)
		nextPassList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail,exo]
		usefulTime=3
		MOT = MOTSteepestHC()
		#shouldBe,nextPassList=MOT.find(satList,usefulTime)
		
		#print(nextPassList)
		conflictGroups = _Helper._findConflictingGroups(nextPassList)
		mergedGroups = _Helper._mergeLists(conflictGroups)
		#print(order)
		print("mergedgroups")
		print(mergedGroups)

		noConflictList=[]
		for Pass in nextPassList:
			notInGroup=True
			for group in mergedGroups:
				if Pass in group:
					notInGroup=False
			if notInGroup:
				noConflictList.append(Pass)
		print("noconflicts")
		print(noConflictList)

		
		score,processedNextPassList = _Helper._findSchedulableSatellites(mergedGroups,usefulTime)

		#willitalwaysbefour?
		#self.assertIs(shouldBe == 0,True)

		print("processed")
		print(processedNextPassList)
		print(score)