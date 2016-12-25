import requests
import math
from scheduler.models import TLE
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
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
			i+=3
		return (final)
		

	#add up name or line array to single space delimited string
	def adder(stringsep):  #nicer way?
		string=""
		for x in stringsep:
			string = string+x
		return (string)


	#predict passes of first sat
	def predictFirst():
		gx = 3582.54659375369
		gy = -277.548936198169
		gz = 5251.95793245245
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

		p, v = sat.propagate(2016, 12, 24, 20, 41, 0)

		#azimuth = math.degrees(math.atan2((gx-p[0]),(gy-p[1])))
		azimuth = math.degrees(math.atan2((p[0]-gx),(p[1]-gy)))

		return sat.satnum