import requests
from scheduler.models import TLE, AzEl
import math, ephem, datetime

class Services():
	
	def updateTLE():
		"""
		Retrieves TLE data from external source, checks format and places in db 
		"""
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle=requestsObject.text
	
		#splits text into one list with format:
		#name, line1, line2, name, line1, line2
		tleArray = tle.split('\r\n')

		#remove errant empty entry
		if tleArray[len(tleArray)-1]=='':
		 	del tleArray[len(tleArray)-1]
		if len(tleArray)%3 !=0:
			print ("major error") #TODO: raisemassive error


		checkedTLEArray = _Helper.checkTLEFormat(tleArray)

		i=0
		while i <= (len(checkedTLEArray)-3):
			name = _Helper.adder(checkedTLEArray[i]).strip()
			try: 
				tleEntry = TLE.objects.get(name=name)
				pass #what does pass do?
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name=name, line1=checkedTLEArray[i+1], line2=checkedTLEArray[i+2])
				newTLE.save()
			else:
				#update existing
				tleEntry.line1 = checkedTLEArray[i+1]
				tleEntry.line2 = checkedTLEArray[i+2]
				tleEntry.save()
			i+=3	

	def getAzElTLENow(self, tleEntry):

		#getObserver from where?
		observer = _Helper.getObserver(self,datetime.datetime.now());

		# try: 
		# 	tleEntry = TLE.objects.get(name=tleName)
		# except TLE.DoesNotExist:
		# 	return "Error" 

		try:
			sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2) #necessary?
		except ValueError as e:
			return "format of db is incorrect TLE"

		sat.compute(observer)
		#AzEl = [sat.az,sat.alt]

		return	AzEl(0,sat.az,sat.alt)

	def getNextPass(tleObject):

		observer = self.getObserver(datetime.datetime.now());

		try:
			sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2) #is the try necessary?
		except ValueError as e:
			return "format of db is incorrect TLE"

		info = observer.next_pass(sat)
		#info object?
		
	#def getListOfNextPasses(tleObject)
		#limit to ten

	#def getAzElTLEOnDate(tleName, date)

class _Helper():
	#Helper Functions
	def adder(stringsep):  #nicer way?
		"""
		Adds up the split strings of the satellite name
		"""
		string=""
		for x in stringsep:
			string = string+x
		return (string)


	def checkTLEFormat(tleArray):
		"""
		Checks the format of the each TLE line to make sure it is in the correct format
		"""
		i=0
		badEntriesArray = []# needs an iterator
		while i <= (len(tleArray)-3):
			try: 
				ephem.readtle(tleArray[i],tleArray[i+1],tleArray[i+2])
			except ValueError as e:
				badEntriesArray.append(tleArray[i])
				badEntriesArray.append(tleArray[i+1])
				badEntriesArray.append(tleArray[i+2])
			i+=3

		goodEntriesArray = [entry for entry in tleArray if entry not in badEntriesArray]
		return goodEntriesArray

	def getObserver(self,datetime):

		observer = ephem.Observer();
		observer.lat = math.radians(55.8)
		observer.long = math.radians(-4.43)
		observer.date = ephem.Date(datetime)
		return observer
	

		


