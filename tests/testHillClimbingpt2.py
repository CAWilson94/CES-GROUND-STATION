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
		# cat = NextPass(0,catTLE, catAOS, catLOS, 0,0,0,0)
		# sixtysevenC = NextPass(1,sixtysevenCTLE,sixtysevenCAOS, sixtysevenCLOS,date1,date1,date1,date1)
		# sixtysevenD = NextPass(2,sixtysevenDTLE,sixtysevenDAOS, sixtysevenDLOS,date1,date1,date1,date1)
		# aist = NextPass(3,aistTLE,aistAOS, aistLOS,date1,date1,date1,date1)
		# beesat = NextPass(4,beesatTLE,beesatAOS, beesatLOS,date1,date1,date1,date1)
		# brite = NextPass(5,briteTLE,briteAOS, briteLOS,date1,date1,date1,date1)
		# cubebug = NextPass(6,cubebugTLE,cubebugAOS, cubebugLOS,date1,date1,date1,date1)
		# sail = NextPass(7,sailTLE,sailAOS, sailLOS,date1,date1,date1,date1)
		
		redfern = NextPass(riseTime=datetime(2017, 3, 27, 16, 24, 50),setTime=datetime(2017, 3, 27, 16, 37, 33),tle="LEMUR-2-REDFERN-GOES")	
		eye= NextPass(riseTime=datetime(2017, 3, 27, 19, 31, 16),setTime=datetime(2017, 3, 27, 19, 37, 35),tle="EYESAT-1 (AO-27)")
		trutna = NextPass(riseTime=datetime(2017, 3, 27, 19, 32, 41),setTime=datetime(2017, 3, 27, 19, 39, 8),tle="LEMUR-2-TRUTNA")
		tech= NextPass(riseTime=datetime(2017, 3, 27, 19, 15, 21),setTime=datetime(2017, 3, 27, 19, 20),tle="TECHEDSAT 5")
		seventyeight= NextPass(riseTime=datetime(2017, 3, 27, 18, 53, 36),setTime=datetime(2017, 3, 27, 19, 2, 5),tle="FLOCK 3P-78")
		seventyfour= NextPass(riseTime=datetime(2017, 3, 27, 18, 53, 45),setTime=datetime(2017, 3, 27, 19, 2, 14),tle="FLOCK 3P-74")
		prime= NextPass(riseTime=datetime(2017, 3, 27, 17, 25, 57),setTime=datetime(2017, 3, 27, 17, 36, 57),tle="M-CUBED & EXP-1 PRIME")
		aus= NextPass(riseTime=datetime(2017, 3, 27, 19, 33, 45),setTime=datetime(2017, 3, 27, 19, 40, 15),tle="LEMUR-2-AUSTINTACIOUS")
		twentyone= NextPass(riseTime=datetime(2017, 3, 27, 19, 1, 46),setTime=datetime(2017, 3, 27, 19, 10, 40),tle="FLOCK 3P-21")

# nextPasses
# '-718d-4b6e-ab15-5aa60c91dbcd'), 'duration': datetime.timedelta(0, 387), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'LEMUR-2-REDFERN-GOES', 'line1': '1 42059U 98067LA  17085.97055905  .00013820  00000-0  20634-3 0  9993', '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6be0>, 'id': UUID('0a841237-754e-47fd-8d62-bfb11f56716b'), 'line2': '2 42059  51.6415  87.9898 0009449 356.8621   3.2311 15.55306862  3206'}>, 'name': 'LEMUR-2-REDFERN-GOES', 'status': 'NEW', 'TLE_id': UUID('0a841237-754e-47fd-8d62-bfb11f56716b'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1adc18>, 'id': UUID('84690422-62cf-4f41-94c9-e93d61cd246f'), 'priority': 2}>, 'riseAzimuth': 2.975374221801758, 'setAzimuth': 1.69297456741333, 'tle': 'LEMUR-2-REDFERN-GOES'}
#  'id': UUID('e479a019-272b-4902-a6ea-40803d90e530'), 'duration': datetime.timedelta(0, 763), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'EYESAT-1 (AO-27)EYESAT-1 (AO-27)', 'line1': '1 22825U 93061C   17085.90791132 -.00000010  00000-0  13763-4 0  9997', '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6668>, 'id': UUID('4385834a-089b-4c57-9777-8992d3f8cace'), 'line2': '2 22825  98.8028  50.5208 0007828 205.2435 154.8365 14.29989843225370'}>, 'name': 'EYESAT-1 (AO-27)', 'status': 'NEW', 'TLE_id': UUID('4385834a-089b-4c57-9777-8992d3f8cace'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1ad860>, 'id': UUID('0c33080b-ffca-4038-97ee-40b1b9d760e4'), 'priority': 2}>, 'riseAzimuth': 3.8602709770202637, 'setAzimuth': 5.822636604309082, 'tle': 'EYESAT-1 (AO-27)'}
# ' 37, ), 'duration': datetime.timedelta(0, 379), '_mission_cache': <Mission: {'_TLE_cache': 											<TLE: {'name': 'LEMUR-2-TRUTNALEMUR-2-TRUTNA', 'line1': '1 42067U 98067LC  17085.90540834  .00022753  00000-0  33264-3 0  9993', '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6a20>, 'id': UUID('17a7cbdb-cb8f-4c7f-8b4e-7f1158989f58'), 'line2': '2 42067  51.6411  88.3110 0009943 356.9139   3.1776 15.55474514  3021'}>, 'name': 'LEMUR-2-TRUTNA', 'status': 'NEW', 'TLE_id': UUID('17a7cbdb-cb8f-4c7f-8b4e-7f1158989f58'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1adb38>, 'id': UUID('6d4031f2-05f0-4cae-aed4-e1408e37f2fc'), 'priority': 2}>, 'riseAzimuth': 2.956939458847046, 'setAzimuth': 1.70160973072052, 'tle': 'LEMUR-2-TRUTNA'}
#  '': UUID('56a296bf-c09e-464e-a1ee-de584bb3f1df'), 'duration': datetime.timedelta(0, 279), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': '"TECHEDSAT 5"', 'line1': '1 42066U 98067LB  17085.95916043  .00062088  00000-0  84237-3 0  9997', '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6dd8>, 'id': UUID('46acd784-af60-4b56-bdeb-77cf64e677df'), 'line2': '2 42066  51.6423  87.9198 0007723  17.2549 342.8622 15.57015912  2937'}>, 'name': 'TECHEDSAT 5', 'status': 'NEW', 'TLE_id': UUID('46acd784-af60-4b56-bdeb-77cf64e677df'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1adcf8>, 'id': UUID('c26f9570-c0ec-4acd-b5fd-7223be3f90d9'), 'priority': 2}>, 'riseAzimuth': 2.729661226272583, 'setAzimuth': 1.8242573738098145, 'tle': 'TECHEDSAT 5'}
# -f462-4811-9571-9dadf394b187'), 'duration': datetime.timedelta(0, 509), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'FLOCK 3P-78', 'line1': '1 42047U 17008DD  17085.66042848  .00001588  00000-0  73184-4 0  9991', '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6f98>, 'id': UUID('5f54eef5-da51-4adf-98e2-fea8af1ea8c2'), 'line2': '2 42047  97.5075 147.2258 0009893 119.4670 240.7564 15.21719805  5145'}>, 'name': 'FLOCK 3P-78', 'status': 'NEW', 'TLE_id': UUID('5f54eef5-da51-4adf-98e2-fea8af1ea8c2'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1addd8>, 'id': UUID('186c8585-f379-41ff-8097-20e43116353e'), 'priority': 2}>, 'riseAzimuth': 1.6376279592514038, 'setAzimuth': 0.013754494488239288, 'tle': 'FLOCK 3P-78'}
#  UUID('a808bddd-8a4d-4ca7-9811-289e69c7d768'), 'duration': datetime.timedelta(0, 509), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'FLOCK 3P-74', 'line1': '1 42048U 17008DE  17085.72628987  .00001589  00000-0  73237-4 0  9993', '_state': <django.db.models.base.ModelState object at 0x7fed28142198>, 'id': UUID('de3193a7-48a0-4c47-82df-2cb7d569dba2'), 'line2': '2 42048  97.5088 147.2935 0009819 118.8540 241.3683 15.21714361  5151'}>, 'name': 'FLOCK 3P-74', 'status': 'NEW', 'TLE_id': UUID('de3193a7-48a0-4c47-82df-2cb7d569dba2'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1adeb8>, 'id': UUID('1474257e-ebeb-4fe0-b987-281772b8a70b'), 'priority': 2}>, 'riseAzimuth': 1.639171838760376, 'setAzimuth': 0.013303876854479313, 'tle': 'FLOCK 3P-74'}
# ': UUID('1de49f4e-5051-47a5-8e69-4ae2222aca1a'), 'duration': datetime.timedelta(0, 660), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'M-CUBED & EXP-1 PRIME', 'line1': '1 37855U 11061F   17085.77465633  .00001607  00000-0  92561-4 0  9990', '_state': <django.db.models.base.ModelState object at 0x7fed28142358>, 'id': UUID('4a0d0c02-14cd-4b0a-b500-4d6534594695'), 'line2': '2 37855 101.7245 275.3134 0181622 324.8906  34.0442 15.02704337294416'}>, 'name': 'M-CUBED & EXP-1 PRIME', 'status': 'NEW', 'TLE_id': UUID('4a0d0c02-14cd-4b0a-b500-4d6534594695'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1adf98>, 'id': UUID('80c3ac7a-cef2-4af8-b205-2333b898cd8b'), 'priority': 2}>, 'riseAzimuth': 0.6304023861885071, 'setAzimuth': 2.4560627937316895, 'tle': 'M-CUBED & EXP-1 PRIME'}
# -471d-4ee4-8378-76972166b0ea'), 'duration': datetime.timedelta(0, 390), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'LEMUR-2-AUSTINTACIOUS', 'line1': '1 42068U 98067LD  17085.90703390  .00017554  00000-0  26025-3 0  9992', '_state': <django.db.models.base.ModelState object at 0x7fed28142518>, 'id': UUID('9543e15b-f6aa-40c1-b481-0c740c9017e0'), 'line2': '2 42068  51.6429  88.3096 0009817 358.9651   1.1310 15.55281952  3120'}>, 'name': 'LEMUR-2-AUSTINTACIOUS', 'status': 'NEW', 'TLE_id': UUID('9543e15b-f6aa-40c1-b481-0c740c9017e0'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1b60b8>, 'id': UUID('a627cf64-7337-453e-83dc-cf7e6a0093af'), 'priority': 2}>, 'riseAzimuth': 2.9874720573425293, 'setAzimuth': 1.6879191398620605, 'tle': 'LEMUR-2-AUSTINTACIOUS'}
# .ModelState object at 0x7fed28142908>, 'id': UUID('37a41ce1-4284-47cf-b800-10f50d37ab50'), 'duration': datetime.timedelta(0, 534), '_mission_cache': <Mission: {'_TLE_cache': <TLE: {'name': 'FLOCK 3P-21', 'line1': '1 41959U 17008M   17085.86360146  .00006528  00000-0  29173-3 0  9995', '_state': <django.db.models.base.ModelState object at 0x7fed281426d8>, 'id': UUID('b705c9a7-f15f-4e75-af66-d83ef7fe1eab'), 'line2': '2 41959  97.5062 147.3968 0011099 117.1144 243.1166 15.21621652  5858'}>, 'name': 'FLOCK 3P-21', 'status': 'NEW', 'TLE_id': UUID('b705c9a7-f15f-4e75-af66-d83ef7fe1eab'), '_state': <django.db.models.base.ModelState object at 0x7fed2a1b6198>, 'id': UUID('df7b57de-a659-4926-be97-b25b3eadd6ac'), 'priority': 2}>, 'riseAzimuth': 1.7245581150054932, 'setAzimuth': 6.277682781219482, 'tle': 'FLOCK 3P-21'}

		
		# threepAOS = datetime(2017,1,1,18,53,45)
		# threepLOS = datetime(2017,1,1,19,2,14)
		# threepsevenAOS = datetime(2017,1,1,18,53,36)
		# threepsevenLOS = datetime(2017,1,1,19,2,5)

		#threep = NextPass(tle="3p-74",riseTime=threepAOS,setTime=threepLOS)
		#threepseven=NextPass(tle="3p-78",riseTime=threepsevenAOS,setTime=threepsevenLOS)

		#satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail]
		nextPassList = [redfern,eye,trutna,tech,seventyeight,seventyfour,prime,aus,twentyone]
		usefulTime=3

		conflictGroups,nonConflictGroups = _Helper._findConflictingGroups(nextPassList)	




		mergedGroups = _Helper._mergeLists(conflictGroups)


		noConflictList=[]
		for Pass in nextPassList:
			notInGroup=True
			for group in mergedGroups:
				if Pass in group:
					notInGroup=False
			if notInGroup:
				noConflictList.append(Pass)

		print("No")
		print(noConflictList)

		score,processedNextPassList = _Helper._findSchedulableSatellites(mergedGroups,usefulTime)
		print("conf")
		print(processedNextPassList)



		score = len(nextPassList)-len(processedNextPassList)
		print(score)
		steepestHC = MOTSteepestHC()
		#shouldBe,nextPassList=MOTSteepestHC().find(satList,usefulTime)
		#print(order)
		#print(nextPassList)
		#willitalwaysbefour?
		#self.assertIs(shouldBe == 0,True)