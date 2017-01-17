from .services import Services, _Helper
from .models import TLE, AzEl
from django.test import TestCase
from datetime import date, datetime, timedelta
# Create your tests here. 


class pyephemTests(TestCase):

	def test_getazeldata_is_correct1(self):
		#test needs to be updated to a newer time if datetime is too far from
		#the current time
		tleEntry = TLE('0','EYESAT-1 (AO-27)',
		'1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991',
		'2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061',)
		azel = Services.getAzElTLE(self, tleEntry ,datetime(2017,1,1,12,0,0))
		shouldBe = AzEl(0,'249:34:07.1','-80:14:12.0')
		self.assertIs(shouldBe == azel,True)

	def test_getazeldata_is_correct2(self):
		#test needs to be updated to a newer time if datetime is too far from
		#the current time
		tleEntry = TLE('0', 'PROMETHEUS 2-3',     
		'1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
		'2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917',)
		azel = Services.getAzElTLE(self, tleEntry ,datetime(2017,6,6,12,0,0))
		print(azel.azimuth)
		print(azel.elevation)
		shouldBe = AzEl(0,'182:36:56.5','-86:15:49.4',)
		self.assertIs(shouldBe == azel,True)

	def test_getAzElForPeriod_is_correct(self):
		tleEntry = TLE('0', 'PROMETHEUS 2-3',     
		'1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
		'2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917',)
				#tleEntry, riseTime, setTime, period in seconds
		azelList = Services.getAzElForPeriod(self, tleEntry ,datetime(2017,6,6,12,2,42),datetime(2017,6,6,12,9,2),30)
		#print(azelList)
		#print(azelList[2].azimuth)
		shouldBe = []
		shouldBe.append(AzEl(0,0.8919017910957336,-1.534958004951477))
		shouldBe.append(AzEl(0,0.7173821926116943,-1.5194507837295532))
		shouldBe.append(AzEl(0,0.6259355545043945,-1.5030969381332397))
		shouldBe.append(AzEl(0,0.570842981338501,-1.4863852262496948))
		shouldBe.append(AzEl(0,0.5344333648681641,-1.4694904088974))
		shouldBe.append(AzEl(0,0.5087897181510925,-1.4524891376495361))
		shouldBe.append(AzEl(0,0.4898819625377655,-1.4354195594787598))
		shouldBe.append(AzEl(0,0.4754546880722046,-1.4183026552200317))
		shouldBe.append(AzEl(0,0.46415090560913086,-1.4011510610580444))
		shouldBe.append(AzEl(0,0.4551066756248474,-1.383972406387329))
		shouldBe.append(AzEl(0,0.4477463364601135,-1.3667718172073364))
		shouldBe.append(AzEl(0,0.4416716694831848,-1.3495526313781738))
		shouldBe.append(AzEl(0,0.4365985989570617,-1.3323169946670532))
		self.assertIs(shouldBe == azelList,True)

	def test_makeNextPassDetails_is_correct(self):
		pass

	def test_getNextPass_is_correct(self):
		#stub
		pass

class HelperMethodsTests(TestCase):

	def test_datespan_is_correct(self):
		pass

	def test_roundMicrosecond_is_correct(self):
		pass 

class UpdateTLETests(TestCase): 	
#data gets pulled in from website, check first few entries are sane? requests job? 	
#gets parsed 	
#put in db 	#gets taken out 	

	def test_data_from_celestrak_is_valid(self):

		tleArray = [
		'EYESAT-1 (AO-27)',
		'1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991', 
		'2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061', 
		'CUTE-1 (CO-55)', 
		'1 27844U 03031E   17012.57520683  .00000056  00000-0  44979-4 0  9997',
		'2 27844  98.6913  23.8380 0010757  79.0163 281.2224 14.22008047702203', 
		'CUBESAT XI-IV (CO-57)', 	
		'1 27848U 03031J   17011.75882937  .00000044  00000-0  39844-4 0  9995', 	
		'2 27848  98.7007  23.2239 0010701  89.1852 271.0552 14.21626517701976',
		'mostwrong',
		'1 wowsowrong1231',
		'2 couldi34v beanym34orew2 3rong',
		'M-CUBED & EXP-1 PRIME',   
		'1 37855U 11061F   17011.86088514  .00001922  00000-0  10927-3 0  9993',
		'2 37855 101.7157 163.8757 0183039 182.8914 177.1254 15.02379487283316',
		'SWISSCUBE',     
		'1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
		'2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640',
		'TIANWANG 1A (TW-1A)',     
		'1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
		'2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858',
		'madeupsat',
		'1 41895U 98067KR   7012.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
		'madeupsat1',
		'1 41895U 98067KR    012.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
		'madeupsat2',
		'1 41895U 98067KR     12.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
		'madeupsat3',
		'1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
		'madeupsat4',
		'1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  04.4040 0005661  96.0874 264.0617 15.55009568  3716',
		'madeupsat5',
		'1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
		'2 41895  51.6434  4.4040 0005661  96.0874 264.0617 15.55009568  3716',]

		checkedArray = _Helper.checkTLEFormat(tleArray)
		#print(checkedArray)
		shouldBe = [
		'EYESAT-1 (AO-27)',
		'1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991', 
		'2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061', 
		'CUTE-1 (CO-55)', 
		'1 27844U 03031E   17012.57520683  .00000056  00000-0  44979-4 0  9997',
		'2 27844  98.6913  23.8380 0010757  79.0163 281.2224 14.22008047702203', 
		'CUBESAT XI-IV (CO-57)', 	
		'1 27848U 03031J   17011.75882937  .00000044  00000-0  39844-4 0  9995', 	
		'2 27848  98.7007  23.2239 0010701  89.1852 271.0552 14.21626517701976',
		'M-CUBED & EXP-1 PRIME',   
		'1 37855U 11061F   17011.86088514  .00001922  00000-0  10927-3 0  9993',
		'2 37855 101.7157 163.8757 0183039 182.8914 177.1254 15.02379487283316',
		'SWISSCUBE',            
		'1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
		'2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640',
		'TIANWANG 1A (TW-1A)',     
		'1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
		'2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858',
		]

		self.assertIs(shouldBe==checkedArray,True)

