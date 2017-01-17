import requests
from scheduler.models import TLE, AzEl
import math, ephem, datetime
from datetime import date, datetime, timedelta

class Services():
	
	def findById(id):
		try:
			tleEntryFi = TLE.objects.get(id = id)
			pass
		except TLE.DoesNotExist as e:
			print ("major error") #TODO: raisemassive error
		return tleEntryFi

	def findByName(name):
		try:
			tleEntryF = TLE.objects.get(name = name)
			pass
		except TLE.DoesNotExist as e:
			print ("major error") #TODO: raisemassive error
		return tleEntryF

	def save(TLEw):
	
		#splits text into one list with format:
		#name, line1, line2, name, line1, line2
		tleArray = TLEw.split('\r\n')

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

	def remove(id):
		try:
			tleEntryR = TLE.objects.get(id = id)
			tleEntryR.delete()
			pass
		except TLE.DoesNotExist as e:
			print ("major error") #TODO: raisemassive error

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
		observer = _Helper.getObserver(self, datetime.now());

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
		#return sat object?
		return	AzEl(0, sat.az,sat.alt)

	def makeNextPassDetails(self,tleEntry):
		#get future passes of satellite
		#List.
		#tleEntry = TLE.objects.get(name="CANX-2")
		#make list of   Az El & range, footprint, where do we have that value?   in range of rise time to set time with 35 increments
		observer = _Helper.getObserver(self, datetime.now());

		try:
			sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2) #is the try necessary?
		except ValueError as e:
			return "format of db is incorrect TLE"

		info = observer.next_pass(sat)
		#from rise time info[0]
		azelProgress = []
		#until set time info[4]
		#info object?
		#calc initial rise/set time
		#info1 = info[0].__dict__
		i=0
		print (info[0].datetime(), info[4].datetime())
		print(info[0])#round up
		print(info[4])
		#print(info[0].tuple())
		for timestamp in _Helper.datespan(info[0].datetime(),info[4].datetime() , delta=timedelta(seconds=30)):
			observer = _Helper.getObserver(self, timestamp)
			sat.compute(observer)
			i+=1
			azel = AzEl(i,sat.az,sat.alt)
			azelProgress.append(azel)
			print(timestamp)
			#new progresssion object?
			#how important is accuracy? can it be ten secs out
		return azelProgress #return object to go in db that's related to list of next passes
	
	def getNextPass(self, tleEntry)
		observer = __Helper.getObserver(datetime.now());
		sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2)
		info = observer.next_pass(sat)
					#riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
		return NextPass(0,)
		
	def makeListOfNextPasses(tleEntry, number):

		observer = __Helper.getObserver(datetime.now());
		sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2)
		#info[4]# settime
		listOfNextPasses = []

		i=0
		while i<number:
			info = observer.next_pass(sat)
			listOfNextPasses.extend(info)
			#make object and add to db?

			duration = satPass[0]-satPass[4]

			for satPass in listOfNextPasses
										#riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
				nextPasses(tleEntry,satPass[0],satPass[4],duration,setPass[3],satPass[1],satPass[5])#.save()

			observer = self.getObserver(info[4].datetime());
			i+=1

		makeNextPassDetails(self,tleEntry)

	# def getListOfNextPasses(tleObject)
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
		observer.lat = math.radians(55.8667)
		observer.long = math.radians(-4.4333)
		observer.date = ephem.Date(datetime)
		return observer
	
	def datespan(startDate, endDate, delta=timedelta(days=1)):
		currentDate = startDate
		while currentDate < endDate:
			yield currentDate
			currentDate += delta
#from stackoverflow
		


