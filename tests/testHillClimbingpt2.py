from datetime import date,datetime
from scheduler.models import TLE, NextPass
from scheduler.MOT.steepestHC import MOTSteepestHC
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

		catTLE = TLE(0,"cat","line1","line2")
		sixtysevenCTLE = TLE(1,"sixtysevenC","line1","line2")
		sixtysevenDTLE= TLE(1,"sixtysevenD","line1","line2")
		aistTLE= TLE(1,"aist","line1","line2")
		beesatTLE= TLE(1,"beesat","line1","line2")
		briteTLE= TLE(1,"brite","line1","line2")
		cubebugTLE= TLE(1,"cubebug","line1","line2")
		sailTLE= TLE(1,"sail","line1","line2")

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
		
		satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail]
		usefulTime=3
		steepestHC = MOTSteepestHC()
		shouldBe,nextPassList=MOTSteepestHC().find(satList,usefulTime)
		#print(order)
		#print(nextPassList)
		#willitalwaysbefour?
		self.assertIs(shouldBe == 0,True)