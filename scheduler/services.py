import requests
import math
from scheduler.models import TLE
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import ephem
import datetime

class services():

	#Retrieving TLE data from external source and placing in the db 
	def updateTLE():
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle=requestsObject.text
		
		#check format is as expected?

		#split leaves one list with format
		#name, line1, line2, name, line1, line2
		final = tle.split('\r\n')
	
		#remove errant empty entry
		if final[len(final)-1]=='':
		 	del final[len(final)-1] 

		i=0
		while i != (len(final)-3):
			name = services.adder(final[i]).strip()
			try: 
				tleentry = TLE.objects.get(name=name)
				pass
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name =name, line1 = final[i+1], line2 = final[i+2])
				newTLE.save()
			else:
				#update existing
				tleentry.line1 = final[i+1]
				tleentry.line2 = final[i+2]
				tleentry.save()
			i+=3
		return (final)
		

	#add up name or line array to single space delimited string
	def adder(stringsep):  #nicer way?
		string=""
		for x in stringsep:
			string = string+x
		return (string)

	def ephem():
		glasgow = ephem.Observer()
		glasgow.lat = math.radians(55.8)
		glasgow.long = math.radians(-4.43)
		glasgow.date = ephem.Date('2017/01/05 13:55:40.12')
		#elevation?

		n1="EYESAT-1 (AO-27)"
		n2="CANX-2"
		n3="COMPASS-1"
		n4="CUTE-1.7+APD II (CO-65)"
		n5="DELFI-C3 (DO-64)"
		n6="AAUSAT-II"
		try:
			satTLE = TLE.objects.get(name=n4)
			pass
		except TLE.DoesNotExist as e:
			raise e
		
		if(satTLE==None):
			return "null"
		
		#wgs72 seems to be the mostly commonly used gravtiy model
		#sat = twoline2rv(satTLE.line1,satTLE.line2, wgs72)
		try:
			canx = ephem.readtle(satTLE.name,satTLE.line1, satTLE.line2)
			pass
			#, TLE.DoesNotExist
		except ValueError as e:
			return "format of db is in correct TLE"

		canx.compute(glasgow)	
		sat_alt, sat_az = [], []
		#angles are in degrees:minutes:seconds
		#215°45'12.3"=215:45:12.3

		#All angles returned by PyEphem are actually measured in radians
		info = glasgow.next_pass(canx)
		return info[0]

		
	#predict passes of first sat
	def predictFirst():
		gsx = 3582.54659375369
		gsy = -277.548936198169
		gsz = 5251.95793245245
		# z (north) z=Re sin (phi (latitude))
		# R (x?) z = Re cos (phi)   
		# Re is earth's equatorial radius
		#brawhalah
		n1="EYESAT-1 (AO-27)"
		n2="CANX-2"
		n3="COMPASS-1"
		n4="CUTE-1.7+APD II (CO-65)"
		n5="DELFI-C3 (DO-64)"
		n6="AAUSAT-II"
		try:
			satTLE = TLE.objects.get(name=n2)
			pass
		except TLE.DoesNotExist as e:
			raise e
		
		if(satTLE==None):
			return "null"
		
		#wgs72 seems to be the mostly commonly used gravtiy model
		#sat = twoline2rv(satTLE.line1,satTLE.line2, wgs72)
		try:
			sat = twoline2rv(satTLE.line1, satTLE.line2, wgs72)
			pass
			#, TLE.DoesNotExist
		except ValueError as e:
			return "format of db is in correct TLE"


		# 	top_e = -sin_theta * range.x
		# + cos_theta * range.y;
		#https://sourceforge.net/p/gpredict/code/ci/master/tree/src/sgpsdp/sgp_obs.c

		#azim = atan(-top_e/top_s);

		p, v = sat.propagate(2016, 12, 29, 19, 41, 0)
		#zyx	p[0]=z, p[1]=y, p[2]=x


		rangex = p[2] - gsx
		rangey = p[1] - gsy

		#sin_theta

		#tope = 

		az = ()

		# azimuth = [None] * 32
		# azimuth[0] = math.degrees(math.atan2((gsx-p[0]),(gsy-p[1])))
		# azimuth[1] = 360 - math.degrees(math.atan2((gsx-p[0]),(gsy-p[1])))
		# azimuth[2] = math.degrees(math.atan2((p[0]-gsx),(p[1]-gsy)))
		# azimuth[3] = 360 - math.degrees(math.atan2((p[0]-gsx),(p[1]-gsy)))
		# azimuth[4] = math.radians(math.atan2((gsx-p[0]),(gsy-p[1])))
		# azimuth[5] = 360 - math.radians(math.atan2((gsx-p[0]),(gsy-p[1])))
		# azimuth[6] = math.radians(math.atan2((p[0]-gsx),(p[1]-gsy)))
		# azimuth[7] = 360 - math.radians(math.atan2((p[0]-gsx),(p[1]-gsy)))

		# azimuth[8] = math.degrees(math.atan2((gsx-p[2]),(gsy-p[1])))
		# azimuth[9] = 360 - math.degrees(math.atan2((gsx-p[2]),(gsy-p[1])))
		# azimuth[10] = math.degrees(math.atan2((p[2]-gsx),(p[1]-gsy)))
		# azimuth[11] = 360 - math.degrees(math.atan2((p[2]-gsx),(p[1]-gsy)))
		# azimuth[12] = math.radians(math.atan2((gsx-p[2]),(gsy-p[1])))
		# azimuth[13] = 360 - math.radians(math.atan2((gsx-p[2]),(gsy-p[1])))
		# azimuth[14] = math.radians(math.atan2((p[2]-gsx),(p[1]-gsy)))
		# azimuth[15] = 360 - math.radians(math.atan2((p[2]-gsx),(p[1]-gsy)))

		# azimuth[16] = math.atan2((gsx-p[2]),(gsy-p[1]))
		# azimuth[17] = 360 - math.atan2((gsx-p[2]),(gsy-p[1]))
		# azimuth[18] = math.atan2((p[2]-gsx),(p[1]-gsy))
		# azimuth[19] = 360 - math.atan2((p[2]-gsx),(p[1]-gsy))
		# azimuth[20] = math.atan2((gsx-p[2]),(gsy-p[1]))
		# azimuth[21] = 360 - math.atan2((gsx-p[2]),(gsy-p[1]))
		# azimuth[22] = math.atan2((p[2]-gsx),(p[1]-gsy))
		# azimuth[23] = 360 - math.atan2((p[2]-gsx),(p[1]-gsy))

		# azimuth[24] = math.atan2((gsx-p[0]),(gsy-p[1]))
		# azimuth[25] = 360 - math.atan2((gsx-p[0]),(gsy-p[1]))
		# azimuth[26] = math.atan2((p[0]-gsx),(p[1]-gsy))
		# azimuth[27] = 360 - math.atan2((p[0]-gsx),(p[1]-gsy))
		# azimuth[28] = math.atan2((gsx-p[0]),(gsy-p[1]))
		# azimuth[29] = 360 - math.atan2((gsx-p[0]),(gsy-p[1]))
		# azimuth[30] = math.atan2((p[0]-gsx),(p[1]-gsy))
		# azimuth[31] = 360 - math.atan2((p[0]-gsx),(p[1]-gsy))

		u = ephem.Uranus()
		u.compute('1781/3/13')
		#sat.__dict__

		return ephem.constellation(u)